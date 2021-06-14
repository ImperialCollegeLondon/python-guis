from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


def on_button_clicked(label):
    label.text = "Hello Pythoners!"


# Create main application.
class HelloApp(App):
    def build(self):
        # Create the widgets.
        hbox = BoxLayout()
        button = Button(text="Click me")
        label = Label(text="")

        # Add them to a container. This includes setting their physical arrangement.
        hbox.add_widget(button)
        hbox.add_widget(label)

        # Add the callback of the button.
        button.bind(on_press=lambda button: on_button_clicked(label))

        # Return the top container. This can be any widget
        return hbox


# Run the main windoow loop, which starts the program.
if __name__ == "__main__":
    from kivy.config import Config

    # We don't want a fullscreen App here.
    Config.set("graphics", "fullscreen", "0")

    HelloApp().run()
