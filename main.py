import kivy
from kivy.app import App
from kivy.uix.label import Label

class PocketApp(App):
    def build(self):
        return Label(text="مرحباً بك في تطبيق التوقعات 🎯")

if __name__ == "__main__":
    PocketApp().run()
  
