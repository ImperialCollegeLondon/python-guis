from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


def on_button_clicked(label):
    label.text = "Hello Pythoners!"


class MainWindow(BoxLayout):
    pass


# Create main application.
class HelloApp(App):
    def build(self):
        return MainWindow()


# Run the main window loop, which starts the program.
if __name__ == "__main__":
    from kivy.config import Config

    # We don't want a fullscreen App here.
    Config.set("graphics", "fullscreen", "0")

    HelloApp().run()
