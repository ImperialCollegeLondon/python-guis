from __future__ import annotations

import weakref
from enum import Flag, auto
from functools import partial
from time import time
from typing import Callable, Dict, List, NamedTuple, Optional, Text, Type

import numpy as np
from matplotlib.backend_bases import Event
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import CirclePolygon
from scipy import interpolate


class Location(Flag):
    N = auto()
    S = auto()
    E = auto()
    W = auto()
    NW = auto()
    NE = auto()
    SW = auto()
    SE = auto()
    CENTRE = auto()
    EDGE = N | S | E | W | NW | NE | SW | SE
    ANY = CENTRE | EDGE
    OUTSIDE = ~ANY


class Button(Flag):
    NONE = auto()
    LEFT = auto()
    RIGHT = auto()
    CENTRE = auto()


class MouseAction(Flag):
    MOVE = auto()
    DRAG = auto()
    CLICK = auto()
    DCLICK = auto()
    SCROLL = auto()
    PICK = auto()
    DPICK = auto()
    PICKDRAG = auto()
    ENTERAXES = auto()
    LEAVEAXES = auto()


class TriggerSignature(NamedTuple):
    """ Contains the signature triad needed to trigger an event.

    - location (Location): The location where the pointer must be
    - button (Button): The button that must be pressed
    - action (MouseAction): The action that is carried
    """

    location: Location
    button: Button
    mouse_action: MouseAction

    @property
    def locations_contained(self):
        """Provides all the locations that are contained by this one.

        For example, if a signature has Location.EDGE, a click event that takes
        place at Location.N and another that takes place at Location.S should both
        trigger the same action, as N and S are contained by EDGE.
        """
        return [loc for loc in Location if self.location & loc == loc]

    def __contains__(self, other) -> bool:
        if not isinstance(other, TriggerSignature):
            raise TypeError("Only a TriggerSignature can be assert equal with another.")

        return (
            other.location in self.locations_contained
            and other.button == self.button
            and other.mouse_action == self.mouse_action
        )


class ActionBase(object):
    """Base class for the actions.

    It ensures that all actions will have a signatures attribute containing all triggers
    relevant for the action.
    """

    def __init__(self, **kwargs):
        self._signatures: Dict[
            TriggerSignature, Callable[[Event, Event], Optional[Event]]
        ] = dict()

    @property
    def signatures(
        self
    ) -> Dict[TriggerSignature, Callable[[Event, Event], Optional[Event]]]:
        return self._signatures


class FigureActionsManager(object):
    """Adds some interactivity functionality to a Matplotlib figure.

    This class adds interactive functionality to a standard figure, replacing
    the actions toolbar, by using only different mouse gestures happening in different
    areas of the axes (indeed, using it in combination with the toolbar might have
    strange results).

    The figure updated with the interactive functionality can be used normally as with
    any other figure. If the figure is to be used embedded in a GUI framework (e.g.
    Tkinter, Kivy, QT...), adding the interactive functionality must be done AFTER the
    figure has been added to the GUI.

    By default, the FigureActionsManager does not add any extra functionality. This
    can be included later on with the self.add_action method or during creation by
    providing the Actions as extra positional arguments. Arguments to the Actions
    can be passed as kwargs dictionaries using: options_ActionName = {}.

    For example, to add ZoomAndPan functionality to figure 'fig' and the ability to
    draw contours with certain options, one could do:

    fam = FigureActionsManager( fig, ZoomAndPan, DrawContours,
                                options_DrawContours=dict(num_contours=2 )
                                )
    """

    def __init__(self, figure: Figure, *args, axis_fraction=0.2, delay=0.2, **kwargs):
        """An existing Matplotlib figure is the only input needed by the Manager.

        Args:
            figure: An instance of a Matplotlib Figure.
            *args: Actions that need to be added.
            axis_fraction: Fraction of the axes that define the edge on each side.
            delay: Time delay used to differentiate clicks from drag events.
            **kwargs: Parameters to be passed during to the creation of the Actions.
        """
        self.axis_fraction = np.clip(axis_fraction, 0, 0.5)
        self.delay = max(delay, 0)

        self._figure = weakref.ref(figure)
        self._time_init = 0
        self._event: List = []
        self._last_event = None
        self._current_action = None
        self._actions: Dict = dict()

        self._connect_events()

        for action in args:
            self.add_action(action, **kwargs)

        figure.actions_manager = self

    @property
    def canvas(self):
        """The canvas this interaction is connected to."""
        return self._figure().canvas

    def draw(self):
        """Convenience method for re-drawing the canvas."""
        self.canvas.draw()

    def _connect_events(self):
        """Connects the relevant events to the canvas."""
        self.canvas.mpl_connect("button_press_event", self._on_mouse_clicked)
        self.canvas.mpl_connect("button_release_event", self._on_mouse_released)
        self.canvas.mpl_connect("motion_notify_event", self._on_mouse_moved)
        self.canvas.mpl_connect("scroll_event", self._on_mouse_scrolled)
        self.canvas.mpl_connect("axes_enter_event", self._on_entering_axes)
        self.canvas.mpl_connect("axes_leave_event", self._on_leaving_axes)
        self.canvas.mpl_connect("pick_event", self._on_mouse_clicked)

    def clean_events(self):
        """Removes all information related to previous events."""
        self._event = []
        self._last_event = None
        self._current_action = None

    def _on_mouse_clicked(self, event):
        """Initial response to the click events by triggering the timer.

        After clicking a mouse button, several things might happen:

        1- The button is released in a time defined by self.delay. In this case,
            it is recorded as a clicked event and some action happens, which might be
            a single click, a double click or a pick action.
        2- The button is released but it takes longer. The clicked event is lost and
            nothing happens.
        3- The mouse is dragged while clicked. After self.delay, the action
            associated with that dragging is executed.
        """
        self._event.append(event)
        self._time_init = time()

    def _on_mouse_moved(self, event):
        """Runs actions related to moving the mouse over the figure."""
        if time() - self._time_init < self.delay:
            return

        elif self._current_action is None:
            self._last_event, mouse_action, mouse_event = self.select_movement_type(
                event
            )
            # print(self._last_event, self._event[-1])
            button = MOUSE_BUTTONS.get(mouse_event.button, Button.NONE)
            location = self.select_location(mouse_event)

            self._current_action = self.select_action(location, button, mouse_action)

        if self._current_action is not None:
            self._last_event = self._current_action(event, self._last_event)

            self.draw()

    def _on_mouse_released(self, event):
        """Stops the timer and executes the original click event, if necessary."""
        if time() - self._time_init > self.delay:
            self.clean_events()
            return

        ev, mouse_action, mouse_event = self.select_click_type()
        button = MOUSE_BUTTONS.get(mouse_event.button, Button.NONE)
        location = self.select_location(mouse_event)

        self._current_action = self.select_action(location, button, mouse_action)

        if self._current_action is not None:
            self._current_action(event, ev)

        self.clean_events()
        self.draw()

    def _on_mouse_scrolled(self, event):
        """Executes scroll events."""
        mouse_action = MouseAction.SCROLL
        button = Button.CENTRE
        location = self.select_location(event)

        action = self.select_action(location, button, mouse_action)

        if action is not None:
            action(event, None)

        self.draw()

    def _on_entering_axes(self, event):
        """Executes the actions related to entering a new axes."""
        mouse_action = MouseAction.ENTERAXES
        button = Button.NONE
        location = self.select_location(event)

        action = self.select_action(location, button, mouse_action)

        if action is not None:
            action(event, None)

        self.clean_events()
        self.draw()

    def _on_leaving_axes(self, event):
        """Executes the actions related to leaving an axes."""
        mouse_action = MouseAction.LEAVEAXES
        button = Button.NONE
        location = self.select_location(event)

        action = self.select_action(location, button, mouse_action)

        if action is not None:
            action(event, None)

        self.clean_events()
        self.draw()

    def select_click_type(self):
        """Select the type of click.

        Here we need to discriminate between single clicks, double clicks and pick
        events (which might also generate a single click).
        """
        if len([p for p in self._event if p.name == "pick_event"]) > 0:
            ev = [p for p in self._event if p.name == "pick_event"][-1]
            if ev.mouseevent.dblclick:
                mouse_action = MouseAction.DPICK
            else:
                mouse_action = MouseAction.PICK
            mouse_event = ev.mouseevent

        elif self._event[0].dblclick:
            mouse_event = ev = self._event[0]
            mouse_action = MouseAction.DCLICK

        else:
            mouse_event = ev = self._event[0]
            mouse_action = MouseAction.CLICK

        return ev, mouse_action, mouse_event

    def select_movement_type(self, event):
        """Select the type of movement.

        Here we need to discriminate between just  move, drag and pickdrag.
        """
        if len(self._event) == 0:
            mouse_action = MouseAction.MOVE
            mouse_event = event
            ev = None
        elif len([p for p in self._event if p.name == "pick_event"]) > 0:
            ev = [p for p in self._event if p.name == "pick_event"][-1]
            mouse_action = MouseAction.PICKDRAG
            mouse_event = ev.mouseevent
        else:
            mouse_action = MouseAction.DRAG
            mouse_event = ev = self._event[-1]

        return ev, mouse_action, mouse_event

    def select_location(self, event) -> Location:
        """Select the type of location."""
        if event.inaxes is None:
            location = Location.OUTSIDE
        else:
            x, y = event.xdata, event.ydata
            xmin, xmax = sorted(event.inaxes.get_xlim())
            ymin, ymax = sorted(event.inaxes.get_ylim())
            location = get_mouse_location(
                x, y, xmin, xmax, ymin, ymax, self.axis_fraction
            )

        return location

    def select_action(self, location, button, mouse_action):
        """Select the action to execute based on the received trigger signature."""
        trigger = TriggerSignature(location, button, mouse_action)

        options = [
            action
            for signature, action in self._actions.items()
            if trigger in signature
        ]

        if len(options) > 1:
            msg = f"Multiple actions for signature {trigger}. Actions: {options}"
            raise RuntimeError(msg)
        elif len(options) == 0:
            action = None
        else:
            action = options[0]

        return action

    def add_action(self, action: Type[ActionBase], **kwargs):
        """Adds an action to the Manager."""
        options = kwargs.get("options_" + action.__name__, {})
        acc = action(**options)
        self._actions.update(acc.signatures)
        self.__dict__[action.__name__] = acc

    def remove_action(self, action_name: Text):
        """Removes an action from the Manager."""
        action = self.__dict__[action_name]
        for k in action.signatures:
            del self._actions[k]
        del self.__dict__[action_name]


MOUSE_BUTTONS = {
    1: Button.LEFT,
    2: Button.CENTRE,
    3: Button.RIGHT,
    "up": Button.CENTRE,
    "down": Button.CENTRE,
}
"""Translates the event.button information into an enumeration."""


def get_mouse_location(x, y, xmin, xmax, ymin, ymax, fraction):
    """Assigns a logical location based on where the mouse is."""
    deltax = abs(xmax - xmin) * fraction
    deltay = abs(ymax - ymin) * fraction

    if xmin <= x <= xmin + deltax:
        if ymin <= y <= ymin + deltay:
            location = Location.NW
        elif ymax - deltay <= y <= ymax:
            location = Location.SW
        else:
            location = Location.W
    elif xmax - deltax <= x <= xmax:
        if ymin <= y <= ymin + deltay:
            location = Location.NE
        elif ymax - deltay <= y <= ymax:
            location = Location.SE
        else:
            location = Location.E
    else:
        if ymin <= y <= ymin + deltay:
            location = Location.N
        elif ymax - deltay <= y <= ymax:
            location = Location.S
        else:
            location = Location.CENTRE

    return location


def circle(
    points: np.ndarray, resolution=360, points_per_contour=2, **kwargs
) -> Optional[np.ndarray]:
    """Calculates the points of the perimeter of a circle."""
    if points.shape[1] == 1 or points.shape[0] % points_per_circle == 1:
        return

    radius = np.linalg.norm(points[-2] - points[-1])
    circle = CirclePolygon(points[-2], radius, resolution=resolution)
    verts = circle.get_path().vertices
    trans = circle.get_patch_transform()

    return trans.transform(verts).T


def simple_closed_contour(
    points: np.ndarray, points_per_contour=6, **kwargs
) -> Optional[np.ndarray]:
    """Adds the first point to the end of the list and returns the resulting array."""
    if points.shape[1] == 1 or points.shape[0] % points_per_contour != 0:
        return

    data = np.vstack(points[-points_per_contour:], points[-points_per_contour])
    return data.T


def spline(
    points: np.ndarray, points_per_contour=6, resolution=360, order=3, **kwargs
) -> Optional[np.ndarray]:
    """Returns a spline that passes through the given points."""
    if points.shape[1] == 1 or points.shape[0] % points_per_contour != 0:
        return

    data = np.vstack((points[-points_per_contour:], points[-points_per_contour]))
    tck, u = interpolate.splprep([data[:, 0], data[:, 1]], s=0, per=True, k=order)[:2]
    data = np.array(interpolate.splev(np.linspace(0, 1, resolution), tck)).T

    return data.T


class DrawContours(ActionBase):
    def __init__(
        self,
        num_contours: int = -1,
        num_points: int = -1,
        draw_contour: Callable = spline,
        contours_updated: Optional[Callable] = None,
        add_point=TriggerSignature(Location.CENTRE, Button.LEFT, MouseAction.CLICK),
        remove_artist=TriggerSignature(Location.CENTRE, Button.RIGHT, MouseAction.PICK),
        clear_drawing=TriggerSignature(
            Location.CENTRE, Button.RIGHT, MouseAction.DCLICK
        ),
        **kwargs,
    ):
        """Add the capability of drawing contours in a figure.

        This action enables to draw points in an axes and draw a contour out of them.
        The points (and the resulting contours) can be removed. By default, it draws
        circles every 2 points, but the user can provide a draw_contour function that
        uses the available points in a different way.

        After drawing each contour, contours_updated is called, enabling the user to
        retrieve the data. Alternatively, the data can be directly accessed from:

         - figure.actions_manager.DrawContours.contour_data

        which is a dictionary with all the contours per axes.

        Args:
            num_contours: Number of contours to add. Negative number for unlimited.
            num_points: Number of contours to add. Negative number for unlimited.
            draw_contour: Function used to create the contour. This function should take
                as first argument an array with all the points currently in the axes and
                return an array with the data to plot. Kwargs of this call will be
                passed to this function.
            contours_updated: Function called whenever the number of contours changes.
                It should take the list of contours as first argument and a list of all
                the points as a second argument. Kwargs of this call will be
                passed to this function.
            add_point: TriggerSignature for this action.
            remove_artist: TriggerSignature for this action.
            clear_drawing: TriggerSignature for this action.
            **kwargs: Arguments passed to either draw_contour or contours_updated.
        """
        super().__init__()
        self.num_contours = num_contours
        self.num_points = num_points
        self.contour_callback = partial(draw_contour, **kwargs)
        self.contours_updated = (
            partial(contours_updated, **kwargs)
            if contours_updated is not None
            else lambda *args: None
        )
        self._signatures = {
            add_point: self.add_point,
            remove_artist: self.remove_artist,
            clear_drawing: self.clear_drawing,
        }

        self.points: Dict = {}
        self.contour_data: Dict = {}
        self.marks: Dict = {}
        self.contours: Dict = {}

    def add_point(self, _, event, *args):
        """Records the position of the click and marks it on the plot.

        Args:
            _: The event associated with the button released (ignored).
            event: The event associated with the button click.
            *args: (ignored)

        Returns:
            None
        """
        if event.inaxes not in self.points:
            self.points[event.inaxes] = []
            self.contour_data[event.inaxes] = []
            self.marks[event.inaxes] = []
            self.contours[event.inaxes] = []

        elif (
            len(self.contours[event.inaxes]) == self.num_contours
            or len(self.points[event.inaxes]) == self.num_points
        ):
            return

        self.points[event.inaxes].append((event.xdata, event.ydata))

        line = Line2D([event.xdata], [event.ydata], marker="o", color="r", picker=2)
        event.inaxes.add_line(line)
        self.marks[event.inaxes].append(line)
        self.add_contour(event.inaxes)

    def remove_artist(self, _, event, *args) -> None:
        """ Removes an artist (point or contour) from the plot.

        Args:
            _: The event associated with the button released (ignored).
            event: The event associated with the button click.
            *args: (ignored)

        Returns:
            None
        """
        axes = event.mouseevent.inaxes
        if axes not in self.points:
            return

        ids_marks = [id(m) for m in self.marks[axes]]
        ids_contours = [id(m) for m in self.contours[axes]]

        if id(event.artist) in ids_marks:
            index = ids_marks.index(id(event.artist))
            self.points[axes].pop(index)
            self.marks[axes].pop(index).remove()

        elif id(event.artist) in ids_contours:
            index = ids_contours.index(id(event.artist))
            self.contour_data[axes].pop(index)
            self.contours[axes].pop(index).remove()

            self.contours_updated(self.contour_data[axes], np.array(self.points[axes]))

    def clear_drawing(self, event, *args) -> None:
        """ Clears all the data accumulated in the drawing and the axes.

        Args:
            event: The event that triggered this action.
            *args: (ignored)

        Returns:
            None
        """
        axes = event.inaxes

        self.points[axes] = []
        self.contour_data[axes] = []

        for mark in self.marks[axes]:
            mark.remove()

        for contour in self.contours[axes]:
            contour.remove()

        self.marks[axes] = []
        self.contours[axes] = []

        self.contours_updated(self.contour_data[axes], np.array(self.points[axes]))

    def add_contour(self, axes) -> None:
        """ Calls the contour callback and add a contour to the axes with the data.

        When completed, if the data is not none, contours_updated callback is called
        with all the contour data and all the points as arguments.

        Args:
            axes: Axes to add the contour to.

        Returns:
            None
        """
        data = self.contour_callback(np.array(self.points[axes]))

        if data is not None:
            self.contour_data[axes].append(data)

            line = Line2D(*data, color="r", picker=2)
            axes.add_line(line)
            self.contours[axes].append(line)

            self.contours_updated(self.contour_data[axes], np.array(self.points[axes]))
