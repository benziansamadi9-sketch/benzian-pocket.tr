import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class PocketApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.label = Label(text="توقع اليوم: جاري التحميل...", font_size='20sp')
        btn = Button(text="تحديث التوقع", font_size='18sp', on_press=self.update_prediction)

        layout.add_widget(self.label)
        layout.add_widget(btn)
        return layout

    def update_prediction(self, instance):
        # هنا لاحقًا سنضيف كود لجلب التوقع من موقع التداول
        self.label.text = "توقع اليوم: صعود زوج EUR/USD 🔼"

if __name__ == "__main__":
    PocketApp().run()
    
