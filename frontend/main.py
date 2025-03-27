from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from backend.service.product_searching_service import ProductSearching
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from backend.service.func_prompt import ask_gemini, res_gemini 

Builder.load_string('''
<ProductList>:
    viewclass: 'ProductItem'
    RecycleBoxLayout:
        default_size: None, dp(100)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

<ProductItem>:
    orientation: 'horizontal'
    spacing: dp(10)
    padding: dp(10)
    Image:
        source: root.image_source
        size_hint_x: None
        width: dp(80)
    Label:
        text: root.text
        valign: 'middle'
        halign: 'left'
        text_size: self.size
                    
<ChatList>:
    viewclass: 'ChatItem'
    RecycleBoxLayout:
        default_size: None, dp(100)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

<ChatItem>:
    orientation: 'horizontal'
    spacing: dp(10)
    padding: dp(10)
    Label:
        text: root.text
        valign: 'top'
        halign: 'left'
        text_size: self.width, None  # Đặt text_size chỉ theo chiều ngang
        size_hint_y: None
        height: self.texture_size[1] + dp(10)  # Tự động co giãn chiều cao    
''')

class ProductItem(RecycleDataViewBehavior, BoxLayout):
    """Custom widget for displaying a product with an image and text."""
    image_source = StringProperty("")
    text = StringProperty("")

class ProductList(RecycleView):
    def __init__(self, **kwargs):
        super(ProductList, self).__init__(**kwargs)
        self.data = []

    def update_data(self, results):
        print("Updating data:", results)
        print(results[0]['image'])
        self.data = [
            {
                'image_source': prod['image'],
                'text': f"Product: {prod['product_name']}\nPrice: {prod['price']}"
            }
            for prod in results
        ]
        self.refresh_from_data()

class SearchScreen(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.searching_service = ProductSearching()

        layout = BoxLayout(orientation='vertical')

        search_layout = BoxLayout(size_hint_y=None, height=50)
        self.search_input = TextInput(hint_text="Nhập từ khóa tìm kiếm...")
        self.search_button = Button(text="Tìm", on_press=self.search)

        search_layout.add_widget(self.search_input)
        search_layout.add_widget(self.search_button)

        layout.add_widget(search_layout)

        self.content_layout = BoxLayout()
        layout.add_widget(self.content_layout)

        self.add_widget(layout)

    def search(self, instance):
        keyword = self.search_input.text
        result_screen = self.sm.get_screen('result')
        result_screen.show_results(self.searching_service.search(keyword))
        self.sm.current = 'result'

class ResultScreen(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm

        layout = BoxLayout(orientation='vertical')

        self.product_list = ProductList()
        back_button = Button(text="Quay lại", size_hint_y=None, height=50, on_press=self.go_back)

        layout.add_widget(self.product_list)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def show_results(self, results):
        self.product_list.update_data(results)

    def go_back(self, instance):
        self.sm.current = 'search'

class ChatList(RecycleView):
    """ Chat message list using RecycleView """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewclass = 'Label'  # Each message is displayed in a Label
        self.data = []  # Chat history

    def add_message(self, text, sender="User"):
        """ Add a new message to the chat """
        self.data.append({'text': f"{sender}: {text}"})
        self.refresh_from_data()

class ChatItem(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty("")

class ChatScreen(Screen):
    """ Main chat screen where user interacts with the bot """
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        layout = BoxLayout(orientation='vertical')

        self.chat_list = ChatList()

        self.user_input = TextInput(size_hint_y=None, height=50, multiline=False)
        send_button = Button(text="Send", size_hint_y=None, height=50)
        send_button.bind(on_press=self.send_message)

        input_layout = BoxLayout(size_hint_y=None, height=50)
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(send_button)

        layout.add_widget(self.chat_list)
        layout.add_widget(input_layout)
        self.add_widget(layout)

    def send_message(self, instance):
        """ Send user message and receive bot response """
        user_text = self.user_input.text.strip()
        if user_text:
            self.chat_list.add_message(user_text, sender="User")
            self.user_input.text = ""  # Clear input field

            # Simulate bot response
            bot_response = self.bot_reply(user_text)
            self.chat_list.add_message(bot_response, sender="Bot")

    def bot_reply(self, user_message):
        """ Simple bot response logic """
        response = res_gemini(user_message)
        # return responses.get(user_message.lower(), "I'm not sure how to respond to that. 🤔")
        return response

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SearchScreen(name='search', sm=sm))
        sm.add_widget(ResultScreen(name='result', sm=sm))
        sm.add_widget(ChatScreen(name="chat", sm=sm))
        return sm

if __name__ == "__main__":
    MyApp().run()
