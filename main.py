import kivy
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

class PocketApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=16, spacing=12)

        # Spinner لاختيار الزوج (base -> target)
        # القيم بصيغة "BASE/TARGET"
        self.pair_spinner = Spinner(
            text='USD/EUR',
            values=('USD/EUR', 'EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/TRY'),
            size_hint=(1, None),
            height='48dp'
        )

        self.label = Label(text="اضغط تحديث للحصول على السعر", font_size='18sp', size_hint=(1, None), height='60dp')
        btn = Button(text="تحديث التوقع", font_size='18sp', size_hint=(1, None), height='48dp')
        btn.bind(on_press=self.update_prediction)

        layout.add_widget(self.pair_spinner)
        layout.add_widget(self.label)
        layout.add_widget(btn)
        return layout

    def update_prediction(self, instance):
        # اقرأ القيمة من الSpinner (مثال "USD/EUR")
        pair = self.pair_spinner.text
        try:
            base, target = pair.split('/')
        except Exception:
            self.label.text = "اختيار الزوج غير صحيح"
            return

        try:
            # نستخدم api.exchangerate.host لأسعار العملات
            url = f"https://api.exchangerate.host/latest?base={base}&symbols={target}"
            response = requests.get(url, timeout=8)
            data = response.json()

            if 'rates' in data and target in data['rates']:
                rate = data['rates'][target]
                self.label.text = f"سعر اليوم: 1 {base} = {rate:.4f} {target}"
            else:
                self.label.text = "لم يتم استرجاع السعر."
        except requests.RequestException:
            self.label.text = "فشل الاتصال بالإنترنت أو انتهاء المهلة."
        except Exception as e:
            self.label.text = "خطأ عند جلب البيانات."

if __name__ == "__main__":
    PocketApp().run()
                
