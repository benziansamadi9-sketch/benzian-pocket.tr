import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class PocketApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.label = Label(text="جاري التحميل...")
        btn = Button(text="تحديث التوقع", font_size=24)

        # 🔸 هذا السطر يربط الزر بالدالة
        btn.bind(on_press=self.update_prediction)

        layout.add_widget(self.label)
        layout.add_widget(btn)
        return layout

    def update_prediction(self, instance):
        # هنا تقدر تضيف الكود لجلب التوقع من موقع التداول لاحقًا
        self.label.text = "توقع اليوم: صعود زوج EUR/USD 📈"

if __name__ == "__main__":
    PocketApp().run()
    
