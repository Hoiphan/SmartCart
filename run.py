from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from backend.service.product_searching_service import ProductSearching
from kivy.uix.screenmanager import ScreenManager, Screen

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
        self.add_widget(layout)

    def search(self, instance):
        keyword = self.search_input.text
        result_screen = self.sm.get_screen('result')
        result_screen.show_results(self.searching_service.search(keyword))
        self.sm.current = 'result'  # Chuyển sang màn hình kết quả

class ResultScreen(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Kết quả tìm kiếm sẽ hiển thị ở đây.")
        self.back_button = Button(text="Quay lại", on_press=self.go_back)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)

    def show_results(self, results):
        self.label.text = "\n".join(results)  # Hiển thị danh sách sản phẩm

    def go_back(self, instance):
        self.sm.current = 'search'  # Quay lại trang tìm kiếm

# Ứng dụng chính
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SearchScreen(name='search', sm=sm))
        sm.add_widget(ResultScreen(name='result', sm=sm))
        return sm

if __name__ == "__main__":
    MyApp().run()
