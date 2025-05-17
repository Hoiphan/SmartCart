from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
import json
from backend.service.assistant_service import func_prompt
from backend.service.product_recommendation_service import ProductRecommendationService

class CircularButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.size_hint = (None, None)
        self.size = (50, 50)

        with self.canvas.after:
            self.color_instruction = Color(0.2, 0.6, 1, 1)
            self.circle = Ellipse(pos=self.pos, size=self.size)

        self.bind(pos=self.update_circle, size=self.update_circle)

    def update_circle(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size

class ChatWidget(FloatLayout):
    chat_open = BooleanProperty(False)
    ad_open = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.LEFT_PADDING = 60

        self.prs = ProductRecommendationService()

        with open("./backend/resources/products.json", "r", encoding="utf-8") as file:
            self.products = json.load(file)

        Clock.schedule_interval(self.change_ad, 5)

        self.product_scroll = ScrollView(
            size_hint=(None, None),
            size=(500, 700),
            pos_hint={'center_x': 0.5, 'top': 0.9}
        )

        self.product_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=0, padding=0)
        self.product_list.bind(minimum_height=self.product_list.setter('height'))

        for product in self.products:
            product_box = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=170,
                spacing=10
            )

            product_image = Image(source=product['image'], size_hint=(None, None), size=(150, 150))

            product_info_box = BoxLayout(orientation='vertical', size_hint_y=None, height=150, spacing=5)

            product_name = Label(
                text='Tên sản phẩm: ' + product['product_name'],
                halign='left', valign='middle',
                text_size=(280, None), color=(0, 0, 0, 1)
            )
            product_price = Label(
                text='Giá: ' + product['price'],
                halign='left', valign='middle',
                text_size=(280, None), color=(0, 0, 0, 1)
            )
            product_description = Label(
                text='Mô tả: ' + product['description'],
                halign='left', valign='middle',
                text_size=(280, None), color=(0, 0, 0, 1)
            )

            # Cho phép text căng đầy chiều cao của label
            for lbl in [product_name, product_price, product_description]:
                lbl.bind(texture_size=lbl.setter('size'))

            product_info_box.add_widget(product_name)
            product_info_box.add_widget(product_price)
            product_info_box.add_widget(product_description)

            product_box.add_widget(product_image)
            product_box.add_widget(product_info_box)

            self.product_list.add_widget(product_box)

        self.product_scroll.add_widget(self.product_list)
        self.add_widget(self.product_scroll)

        # Quảng cáo
        self.ads_images = [
            "D:/Ming Lu Zhuang 2024/HCMUT/HK242/Do_an/backend/resources/images/57331424_2213510005394932_5537901797483479040_o.jpg",
            "D:/Ming Lu Zhuang 2024/HCMUT/HK242/Do_an/backend/resources/images/ca-phe-trung-nguyen-g7-hoa-tan.jpg"
        ]
        self.ad_index = 0

        self.ad_image_width = 400
        self.ad_image_height = 200
        self.ad_button_width = 60
        self.ad_image = Image(source=self.ads_images[self.ad_index], size_hint=(None, None),
                              size=(self.ad_image_width, self.ad_image_height))
        self.ad_image.pos = (-self.LEFT_PADDING, 0)
        self.add_widget(self.ad_image)

        self.ad_button = Button(text="Close", size_hint=(None, None),
                                size=(self.ad_button_width, self.ad_image_height),
                                pos=(self.ad_image_width - 2 * self.LEFT_PADDING, 0))
        self.ad_button.bind(on_press=self.toggle_ad)
        self.add_widget(self.ad_button)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        self.chat_button = CircularButton(
            text="💬",
            pos_hint={'right': 1, 'y': 0}
        )

        self.chat_button.pos = (self.width - 100, 10)
        self.bind(size=self.update_chat_button_pos)

        self.chat_button.bind(on_press=self.toggle_chat)
        self.add_widget(self.chat_button)

        self.chat_box = BoxLayout(orientation='vertical',
                                  size_hint=(None, None), size=(300, 400),
                                  pos_hint={'right': 1, 'y': 0.1},
                                  padding=5, spacing=5)
        self.chat_box.canvas.opacity = 0

        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.chat_history = Label(size_hint_y=None, text_size=(280, None), halign='left', valign='top',
                                  color=(0, 0, 0, 1))
        self.chat_history.bind(texture_size=self.update_chat_height)
        self.scroll.add_widget(self.chat_history)
        self.chat_box.add_widget(self.scroll)

        input_area = BoxLayout(size_hint=(1, 0.2))
        self.chat_input = TextInput(hint_text="Nhập tin nhắn...", multiline=False, foreground_color=(0, 0, 0, 1))
        send_button = Button(text="Gửi", size_hint=(None, 1), width=60)
        send_button.bind(on_press=self.send_message)
        input_area.add_widget(self.chat_input)
        input_area.add_widget(send_button)
        self.chat_box.add_widget(input_area)

        self.add_widget(self.chat_box)

    def toggle_chat(self, instance):
        self.chat_open = not self.chat_open
        self.chat_box.canvas.opacity = 1 if self.chat_open else 0
        self.chat_box.disabled = not self.chat_open

    def send_message(self, instance):
        message = self.chat_input.text.strip()
        if message:
            res = func_prompt.res_gemini(message)
            self.chat_history.text += f"Bạn: {message}\n"
            self.chat_history.text += f"Bot: {res}\n"
            self.chat_input.text = ''

    def update_chat_height(self, instance, size):
        self.chat_history.height = size[1]
        self.scroll.scroll_y = 0

    def update_chat_button_pos(self, *args):
        self.chat_button.pos = (self.width - 60, 10)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def toggle_ad(self, instance):
        self.ad_open = not self.ad_open
        self.ad_button.text = 'Close' if self.ad_open else 'Open'

        ad_animation = Animation(x=-self.LEFT_PADDING if self.ad_open else -self.ad_image_width, duration=0.62)
        button_animation = Animation(x=self.ad_image_width - 2 * self.LEFT_PADDING if self.ad_open else 0, duration=0.5)

        ad_animation.start(self.ad_image)
        button_animation.start(self.ad_button)

        if self.ad_open:
            ad_animation.bind(on_complete=self.on_ad_open)
        else:
            ad_animation.bind(on_complete=self.on_ad_close)

    def on_ad_open(self, *args):
        self.ad_image.x = -self.LEFT_PADDING
        self.ad_button.x = self.ad_image_width - 2 * self.LEFT_PADDING

    def on_ad_close(self, *args):
        self.ad_image.x = -self.ad_image_width
        self.ad_button.x = 0

    def change_ad(self, dt):
        self.ad_index = (self.ad_index + 1) % len(self.ads_images)
        self.ad_image.source = self.ads_images[self.ad_index]

class ChatApp(App):
    def build(self):
        return ChatWidget()

if __name__ == '__main__':
    ChatApp().run()