import requests
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock

class PocketApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.pair_spinner = Spinner(
            text='BTCUSDT',
            values=('BTCUSDT', 'ETHUSDT', 'EUR/USD', 'USD/JPY'),
            size_hint=(1, None),
            height='48dp'
        )
        self.layout.add_widget(self.pair_spinner)

        self.label_price = Label(text='السعر سيظهر هنا', font_size='20sp')
        self.layout.add_widget(self.label_price)

        self.label_prediction = Label(text='توقع الاتجاه سيظهر هنا', font_size='20sp', color=(0,1,0,1))
        self.layout.add_widget(self.label_prediction)

        btn = Button(text='تحديث السعر والتوقع', size_hint=(1, None), height='48dp')
        btn.bind(on_press=self.update_data)
        self.layout.add_widget(btn)

        Clock.schedule_interval(self.update_data, 30)

        return self.layout

    def update_data(self, *args):
        pair = self.pair_spinner.text.strip()
        price = self.get_price(pair)
        if price:
            self.label_price.text = f'السعر الحالي لـ {pair}: {price:.6f}'
            prediction = self.get_prediction(price)
            self.label_prediction.text = f'🔮 التوقع: {prediction}'
        else:
            self.label_price.text = 'خطأ في جلب السعر.'
            self.label_prediction.text = ''

    def get_price(self, pair):
        try:
            if '/' in pair:
                base, target = pair.split('/')
                url = f'https://api.exchangerate.host/convert?from={base}&to={target}'
                r = requests.get(url, timeout=10)
                data = r.json()
                return data.get('result', None)
            else:
                url = f'https://api.binance.com/api/v3/ticker/price?symbol={pair.upper()}'
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    return float(r.json()['price'])
        except:
            return None

    def get_prediction(self, price):
        """
        نموذج توقع بسيط — مؤقت للتجربة
        """
        # نحاكي نموذج صغير يتوقع الصعود أو الهبوط بشكل عشوائي
        change = random.choice(['⬆️ سيرتفع', '⬇️ سينخفض'])
        confidence = random.uniform(60, 95)  # نسبة ثقة افتراضية
        return f'{change} (ثقة {confidence:.1f}%)'

if __name__ == "__main__":
    PocketApp().run()
        
