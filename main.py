# main.py
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock

class PocketApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Spinner لاختيار الزوج
        self.pair_spinner = Spinner(
            text='USD/EUR',
            values=('USD/EUR', 'EUR/USD', 'BTCUSDT', 'ETHUSDT', 'USD/JPY'),
            size_hint=(1, None),
            height='48dp'
        )
        self.layout.add_widget(self.pair_spinner)

        # Label لعرض النتيجة
        self.label = Label(text='اضغط تحديث أو انتظر التحديث التلقائي', font_size='20sp', halign='center')
        self.layout.add_widget(self.label)

        # زر تحديث يدوي
        btn = Button(text='تحديث التوقع / السعر', size_hint=(1, None), height='48dp')
        btn.bind(on_press=self.update_price)
        self.layout.add_widget(btn)

        # تحديث تلقائي كل 30 ثانية (تقدر تغير المدة)
        Clock.schedule_interval(self.update_price, 30)

        return self.layout

    def update_price(self, *args):
        pair = self.pair_spinner.text.strip()
        try:
            if '/' in pair:
                # زوج عملات كـ USD/EUR -> نستخدم exchangerate.host
                base, target = pair.split('/')
                url = f'https://api.exchangerate.host/convert?from={base}&to={target}'
                r = requests.get(url, timeout=10)
                data = r.json()
                if data.get('success', False) or 'result' in data:
                    rate = data.get('result')
                    if rate is None:
                        self.label.text = f'لم يتم الحصول على السعر لِ {pair}'
                    else:
                        self.label.text = f'السعر {pair} = {rate:.6f}'
                else:
                    self.label.text = f'خطأ في مصدر أسعار: {data}'
            else:
                # رموز سوق (مثال BTCUSDT) -> نحاول Binance
                symbol = pair.upper()
                url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    price = float(data.get('price', 0))
                    self.label.text = f'السعر {symbol} = {price:.6f}'
                else:
                    self.label.text = f'خطأ Binance: رمز غير معروف أو مشكلة (HTTP {r.status_code})'
        except Exception as e:
            # خطأ عام
            self.label.text = f'حدث خطأ: {e}'

if __name__ == "__main__":
    PocketApp().run()
        
