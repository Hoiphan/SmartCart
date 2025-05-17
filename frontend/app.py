import itertools
import time
import streamlit as st
from backend.service.product_searching_service import ProductSearching
from backend.service.func_prompt import res_gemini
from backend.service.product_recommendation_service import ProductRecommendationService
import json
from streamlit_autorefresh import st_autorefresh
from multiprocessing import Queue, Process
import queue as queue_module
from icecream import ic
from backend.service.voice_speech_to_text import speech_to_text
from streamlit_float import *

if 'cart' not in st.session_state:
    st.session_state.cart = set()

position = {
    1: 1,
    2: 1,
    3: 2,
    0: 2,
    4: 3,
    5: 3
}

def main():
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Chọn trang:", ["Trang chủ", "Sản phẩm", "Giỏ hàng", "Quảng cáo", "Trợ lý", "Liên hệ"])

    if 'queue' not in st.session_state:
        st.session_state.queue = Queue()
        st.session_state.p = Process(target=run_turtle, args=(st.session_state.queue,))
        st.session_state.p.start()

    # if st.button("Vẽ hình tròn"):
    #     st.session_state.queue.put("circle")

    if page == "Trang chủ":
        home_page()
    elif page == "Sản phẩm":
        searching_page()
    elif page == "Giỏ hàng":
        cart_page()
    elif page == "Quảng cáo":
        advertising_page()
    elif page == "Trợ lý":
        about_page()
    elif page == "Liên hệ":
        contact_page()


def home_page():
    # st.title("Trang chủ")
    # image_paths = ["assets/1.jpg", "assets/2.jpg", "assets/3.jpg"]  # Thay thế bằng danh sách ảnh thực tế
    # img_placeholder = st.empty()
    
    # for img_path in itertools.cycle(image_paths):
    #     img_placeholder.image(img_path, use_container_width=True)
    #     time.sleep(2)
    
    st.title('Sản phẩm:')
    # Đọc dữ liệu từ file JSON
    with open('../backend/resources/products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)

    # Hiển thị danh sách sản phẩm
    for product in products:
        col1, col2 = st.columns([1, 2])
        with col1:
            try:
                st.image(product['image'], caption=product['product_name'])
            except:
                pass
        with col2:
            st.write(f"**{product['product_name']}**")
            st.write(f"Giá: {product.get('price', 'Không có thông tin')}")
            st.write(f"Mô tả: {product.get('description', 'Không có mô tả')}")
            if st.button(f"Vị trí", key=f"vitri_{product['product_id']}"):
                st.session_state.queue.put(position[product["product_id"]])
                # ic(st.session_state.queue.get())
            if st.button(f"Thêm vào giỏ hàng - {product['product_name']}"):
                st.session_state.cart.add(product['product_id'])
                st.success(f"Đã thêm {product['product_name']} vào giỏ hàng!")
    
def cart_page():
    with open('../backend/resources/products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)

    with open("C:/Users/tam/Documents/GitHub/SmartCart/items.txt", "r") as f:
        cart = f.readlines()
        cart = list(map(lambda x: int(x.replace("\n", "")), cart))
        ic(cart)
    for product in products:
        if product['product_id'] not in cart:
            continue

        col1, col2 = st.columns([1, 2])
        with col1:
            try:
                st.image(product['image'], caption=product['product_name'])
            except Exception as e:
                st.write(e)
        with col2:
            st.write(f"**{product['product_name']}**")
            st.write(f"Giá: {product.get('price', 'Không có thông tin')}")
            st.write(f"Mô tả: {product.get('description', 'Không có mô tả')}")
            if st.button(f"Xoá khỏi giỏ hàng - {product['product_name']}"):
                st.session_state.cart.discard(product['product_id'])
                st.success(f"Đã xoá {product['product_name']} khỏi giỏ hàng!")
                st.rerun()

# def advertising_page():
#     product_recommendation_service = ProductRecommendationService()
#     next_products = product_recommendation_service.recommend_next_product(st.session_state.cart)
    
#     with open('../backend/resources/promotion.json', 'r', encoding='utf-8') as file:
#         promotions = json.load(file)

#     image_paths = list(filter(lambda x: True if x else False, [p['image'] if p['product_id'] in next_products else None for p in promotions]))
#     img_placeholder = st.empty()
    
#     for img_path in itertools.cycle(image_paths):
#         img_placeholder.image(img_path, use_container_width=True)
#         time.sleep(2)

def advertising_page():
    # Refresh mỗi 2000ms (2 giây), giới hạn 100 lần (tuỳ bạn)
    st_autorefresh(interval=2000, limit=100, key="slideshow_ad")

    product_recommendation_service = ProductRecommendationService()
    with open(r'C:\Users\tam\Documents\GitHub\SmartCart\items.txt', 'r') as f:
        items = f.readlines()
        items = list(map(lambda x: int(x.replace("\n", "")), items))

    next_products = product_recommendation_service.recommend_next_product(items)

    with open('../backend/resources/promotion.json', 'r', encoding='utf-8') as file:
        promotions = json.load(file)

    image_paths = [p['image'] for p in promotions if p['product_id'] in next_products and p.get('image')]

    # Sử dụng session_state để lưu chỉ số ảnh hiện tại
    if 'ad_index' not in st.session_state:
        st.session_state.ad_index = 0

    # Nếu có ảnh quảng cáo
    if image_paths:
        current_index = st.session_state.ad_index % len(image_paths)
        st.image(image_paths[current_index])

        # Tăng chỉ số để lần sau hiển thị ảnh kế tiếp
        st.session_state.ad_index += 1
    else:
        st.write("Không có sản phẩm quảng cáo.")

def searching_page():
    user_input = st.text_input("Nhập gì đó:")
    product_searching_service = ProductSearching()

    if st.button("Gửi"):
        products = product_searching_service.search(user_input)
        if products:
            st.write("### Kết quả tìm kiếm:")
            for product in products:
                col1, col2 = st.columns([1, 2])
                with col1:
                    try:
                        st.image(product['image'], caption=product['product_name'])
                    except:
                        pass
                with col2:
                    st.write(f"**{product['product_name']}**")
                    st.write(f"Giá: {product.get('price', 'Không có thông tin')}")
                    st.write(f"Mô tả: {product.get('description', 'Không có mô tả')}")
        else:
            st.write("Không tìm thấy sản phẩm nào.")


def about_page():
    # st.title("Trợ lý")
    # user_input = st.text_input("Nhập gì đó:")
    # if user_input:
    #     response = res_gemini(user_input)
    #     st.write(response)

    # Streamed response emulator
    def response_generator(prompt):
        response = res_gemini(prompt)
        for word in response.split():
            yield word + " "
            time.sleep(0.05)

    st.title("Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- Auto-scroll to bottom using JavaScript ---
    scroll_script = """
    <script>
        var chatContainer = window.parent.document.querySelector("section.main");
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    </script>
    """
    st.markdown(scroll_script, unsafe_allow_html=True)

    # --- Đặt input ở dưới cùng ---
    input_container = st.container()  # Tạo một container trống để giữ input ở dưới

    with input_container.container():  # Đảm bảo phần input nằm cuối
        col1, col2 = st.columns([8, 2])  # Chia layout 2 cột: input text (8 phần), voice button (2 phần)

        with col1:
            prompt = st.chat_input("Type your message...")  # Input text

        with col2:
            if st.button("🎙️ Speak"):
                prompt = speech_to_text()  # Giả sử đây là hàm nhận dạng giọng nói

    input_container.float("bottom: 3rem;")

    # Accept user input
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(prompt))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


def contact_page():
    st.title("Liên hệ")
    st.write("Bạn có thể liên hệ chúng tôi qua email: contact@example.com")

import time
import turtle
import math
import socket
import json

# while True:
#     if not queue.empty():
#         cmd = queue.get()
#         ic(cmd)

# Thiết lập socket


# def run_turtle(queue):
#     hostname = socket.gethostname()
#     UDP_IP = socket.gethostbyname(hostname)
#     ic("***Local ip:" + str(UDP_IP) + "***")
#     UDP_PORT = 80
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.bind((UDP_IP, UDP_PORT))
#     sock.listen(1)
#     ic("Waiting for connection...")
#     conn, addr = sock.accept()
#     ic(f"Connected by {addr}")
#
#     # Các thông số cố định
#     distance_a1_a2 = 1
#     distance_a1_a3 = 1  # Khoảng cách Anchor1-Anchor3
#     distance_a2_a3 = 1  # Khoảng cách Anchor2-Anchor3
#     meter2pixel = 100
#     range_offset = 1.0
#
#     def screen_init(width=1200, height=800, t=turtle):
#         t.setup(width, height)
#         t.tracer(False)
#         t.hideturtle()
#         t.speed(0)
#
#     def turtle_init(t=turtle):
#         t.hideturtle()
#         t.speed(0)
#
#     def draw_line(x0, y0, x1, y1, color="black", t=turtle):
#         t.pencolor(color)
#         t.up()
#         t.goto(x0, y0)
#         t.down()
#         t.goto(x1, y1)
#         t.up()
#
#     def draw_fastU(x, y, length, color="black", t=turtle):
#         draw_line(x, y, x, y + length, color, t)
#
#     def draw_fastV(x, y, length, color="black", t=turtle):
#         draw_line(x, y, x + length, y, color, t)
#
#     def draw_cycle(x, y, r, color="black", t=turtle):
#         t.pencolor(color)
#         t.up()
#         t.goto(x, y - r)
#         t.setheading(0)
#         t.down()
#         t.circle(r)
#         t.up()
#
#     def fill_cycle(x, y, r, color="black", t=turtle):
#         t.up()
#         t.goto(x, y)
#         t.down()
#         t.dot(r, color)
#         t.up()
#
#     def write_txt(x, y, txt, color="black", t=turtle, f=('Arial', 12, 'normal')):
#         t.pencolor(color)
#         t.up()
#         t.goto(x, y)
#         t.down()
#         t.write(txt, move=False, align='left', font=f)
#         t.up()
#
#     def draw_rect(x, y, w, h, color="black", t=turtle):
#         t.pencolor(color)
#         t.up()
#         t.goto(x, y)
#         t.down()
#         t.goto(x + w, y)
#         t.goto(x + w, y + h)
#         t.goto(x, y + h)
#         t.goto(x, y)
#         t.up()
#
#     def fill_rect(x, y, w, h, color=("black", "black"), t=turtle):
#         t.begin_fill()
#         draw_rect(x, y, w, h, color, t)
#         t.end_fill()
#
#     def clean(t=turtle):
#         t.clear()
#
#     def draw_ui(t):
#         pass  # Bỏ lưới và tiêu đề
#
#     def draw_uwb_anchor(x, y, txt, range, t):
#         r = 20
#         fill_cycle(x, y, r, "green", t)
#         write_txt(x + r, y, txt + ": " + str(range) + "M",
#                   "black", t, f=('Arial', 16, 'normal'))
#
#     def draw_uwb_tag(x, y, txt, t):
#         pos_x = -250 + int(x * meter2pixel)
#         pos_y = 150 - int(y * meter2pixel)
#         if not (-600 <= pos_x <= 600 and -400 <= pos_y <= 400):
#             ic(f"Tag out of bounds: ({pos_x}, {pos_y})")
#             return
#         r = 20
#         fill_cycle(pos_x, pos_y, r, "blue", t)
#         write_txt(pos_x, pos_y, txt + ": (" + str(x) + "," + str(y) + ")",
#                   "black", t, f=('Arial', 16, 'normal'))
#
#     def read_data(conn):
#         # global conn, addr
#         uwb_list = []
#         try:
#             line = ""
#             while True:
#                 chunk = conn.recv(1024).decode('UTF-8')
#                 if not chunk:
#                     ic("Client disconnected, waiting for new connection...")
#                     conn.close()
#                     conn, addr = sock.accept()
#                     ic(f"Reconnected by {addr}")
#                     return uwb_list
#                 line += chunk
#                 try:
#                     uwb_data = json.loads(line)
#                     break
#                 except json.JSONDecodeError:
#                     continue
#             ic(f"Raw data: {line}")
#             ic(f"Parsed data: {uwb_data}")
#             uwb_list = uwb_data.get("links", [])
#             for uwb_anchor in uwb_list:
#                 ic(f"Anchor {uwb_anchor['A']}: Range = {uwb_anchor['R']}")
#         except socket.error as e:
#             ic(f"Socket error: {e}")
#         ic("")
#         return uwb_list
#
#     def trilateration(r1, r2, r3, x1=0, y1=0, x2=1, y2=0, x3=0.5, y3=0.866):
#         A = 2 * x2 - 2 * x1
#         B = 2 * y2 - 2 * y1
#         C = r1 ** 2 - r2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
#         D = 2 * x3 - 2 * x2
#         E = 2 * y3 - 2 * y2
#         F = r2 ** 2 - r3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2
#         x = (C * E - F * B) / (E * A - B * D)
#         y = (C * D - A * F) / (B * D - A * E)
#         return round(x, 1), round(y, 1)
#
#     def uwb_range_offset(uwb_range):
#         return uwb_range
#
#     def main_turtle():
#         t_ui = turtle.Turtle()
#         t_a1 = turtle.Turtle()
#         t_a2 = turtle.Turtle()
#         t_a3 = turtle.Turtle()
#         t_a4 = turtle.Turtle()
#         for t in [t_ui, t_a1, t_a2, t_a3, t_a4]:
#             turtle_init(t)
#
#         screen_init()
#         turtle.tracer(0)
#
#         a1_range = a2_range = a3_range = 0.0
#
#         draw_ui(t_ui)
#
#         try:
#             while True:
#                 node_count = 0
#                 uwb_list = read_data(conn)
#
#                 for one in uwb_list:
#                     anchor_id = one.get("A")
#                     range_val = uwb_range_offset(float(one.get("R", 0)))
#                     if anchor_id == "1782":
#                         clean(t_a1)
#                         a1_range = range_val
#                         draw_uwb_anchor(-250, 150, "A1782(0,0)", a1_range, t_a1)
#                         node_count += 1
#                     elif anchor_id == "1783":
#                         clean(t_a2)
#                         a2_range = range_val
#                         draw_uwb_anchor(-250 + meter2pixel * distance_a1_a2, 150,
#                                         f"A1783({distance_a1_a2},0)", a2_range, t_a2)
#                         node_count += 1
#                     elif anchor_id == "1784":
#                         clean(t_a4)
#                         a3_range = range_val
#                         draw_uwb_anchor(-250 + meter2pixel * 0.5, 150 - meter2pixel * 0.866,
#                                         "A1784(0.5,0.866)", a3_range, t_a4)
#                         node_count += 1
#
#                 if node_count == 3:
#                     try:
#                         ic(f"Ranges: A1782={a1_range}, A1783={a2_range}, A1784={a3_range}")
#                         x, y = trilateration(a1_range, a2_range, a3_range)
#                         ic(f"Tag position: ({x}, {y})")
#                         clean(t_a3)
#                         draw_uwb_tag(x, y, "TAG", t_a3)
#                     except ZeroDivisionError:
#                         ic("Trilateration failed: Invalid ranges")
#
#                 turtle.update()
#                 time.sleep(0.1)  # Giảm sleep
#         except KeyboardInterrupt:
#             ic("Shutting down...")
#         finally:
#             conn.close()
#             sock.close()
#
#     main_turtle()

def run_turtle(queue):
    import turtle
    import socket
    import json
    import time


    # while True:
    #     try:
    #         item = queue.get_nowait()
    #         ic("New item: ", item)
    #     except queue_module.Empty:
    #         pass  # Không có gì trong queue thì bỏ qua, tiếp tục loop

    hostname = socket.gethostname()
    UDP_IP = socket.gethostbyname(hostname)
    ic("***Local ip:" + str(UDP_IP) + "***")
    UDP_PORT = 80
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.listen(1)
    ic("Waiting for connection...")
    conn, addr = sock.accept()
    ic(f"Connected by {addr}")

    map_kehang_anchor_id = {
        1: "1782",
        2: "1783",
        3: "1784"
    }

    # Thông số hệ tọa độ
    distance_a1_a2 = 1
    distance_a1_a3 = 1
    distance_a2_a3 = 1
    meter2pixel = 100
    range_offset = 1.0

    # Khởi tạo Turtle
    def screen_init(width=1200, height=800):
        turtle.setup(width, height)
        turtle.tracer(False)

    def turtle_init(t):
        t.hideturtle()
        t.speed(0)

    def draw_cycle(x, y, r, color, t):
        t.up()
        t.goto(x, y - r)
        t.setheading(0)
        t.down()
        t.pencolor(color)
        t.circle(r)
        t.up()

    def fill_cycle(x, y, r, color, t):
        t.up()
        t.goto(x, y)
        t.down()
        t.dot(r, color)
        t.up()

    def write_txt(x, y, txt, color, t, f=('Arial', 12, 'normal')):
        t.up()
        t.goto(x, y)
        t.down()
        t.pencolor(color)
        t.write(txt, font=f)
        t.up()

    def clean(t):
        t.clear()

    def draw_uwb_anchor(x, y, txt, range_val, color, t):
        r = 20
        fill_cycle(x, y, r, color, t)
        write_txt(x + r, y, txt + f": {range_val:.2f}M", "black", t, f=('Arial', 16, 'normal'))

    def draw_uwb_tag(x, y, txt, t):
        pos_x = -250 + int(x * meter2pixel)
        pos_y = 150 - int(y * meter2pixel)
        if not (-600 <= pos_x <= 600 and -400 <= pos_y <= 400):
            ic(f"Tag out of bounds: ({pos_x}, {pos_y})")
            return
        r = 20
        fill_cycle(pos_x, pos_y, r, "blue", t)
        write_txt(pos_x, pos_y, txt + f": ({x},{y})", "black", t, f=('Arial', 16, 'normal'))

    def trilateration(r1, r2, r3, x1=0, y1=0, x2=1, y2=0, x3=0.5, y3=0.866):
        A = 2 * x2 - 2 * x1
        B = 2 * y2 - 2 * y1
        C = r1 ** 2 - r2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
        D = 2 * x3 - 2 * x2
        E = 2 * y3 - 2 * y2
        F = r2 ** 2 - r3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2
        x = (C * E - F * B) / (E * A - B * D)
        y = (C * D - A * F) / (B * D - A * E)
        return round(x, 1), round(y, 1)

    def read_data(conn):
        # ic('queue')
        uwb_list = []
        try:
            line = ""
            while True:
                chunk = conn.recv(1024).decode('UTF-8')
                if not chunk:
                    ic("Client disconnected.")
                    conn.close()
                    return []
                line += chunk
                try:
                    uwb_data = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue
            ic(f"Raw data: {line}")
            uwb_list = uwb_data.get("links", [])
        except socket.error as e:
            ic(f"Socket error: {e}")
        return uwb_list

    # === HÀM MỚI: đổi màu anchor theo ID ===
    def set_anchor_color(anchor_id, color):
        if anchor_id == "1782":
            clean(t_a1)
            draw_uwb_anchor(-250, 150, "A1782(0,0)", a1_range, color, t_a1)
        elif anchor_id == "1783":
            clean(t_a2)
            draw_uwb_anchor(-250 + meter2pixel * distance_a1_a2, 150,
                            f"A1783({distance_a1_a2},0)", a2_range, color, t_a2)
        elif anchor_id == "1784":
            clean(t_a4)
            draw_uwb_anchor(-250 + meter2pixel * 0.5, 150 - meter2pixel * 0.866,
                            "A1784(0.5,0.866)", a3_range, color, t_a4)

    # === Main turtle loop ===
    def main_turtle():
        global t_a1, t_a2, t_a3, t_a4
        t_a1 = turtle.Turtle()
        t_a2 = turtle.Turtle()
        t_a3 = turtle.Turtle()
        t_a4 = turtle.Turtle()
        for t in [t_a1, t_a2, t_a3, t_a4]:
            turtle_init(t)

        screen_init()
        turtle.tracer(0)

        global a1_range, a2_range, a3_range
        a1_range = a2_range = a3_range = 0.0

        color_1782 = "green"
        color_1783 = "green"
        color_1784 = "green"
        try:
            while True:
                # ic('queue')
                try:
                    kehang = queue.get_nowait()
                    ic("Ke hang: ", kehang)
                    if kehang == 1:
                        color_1782 = "red"
                        color_1783 = "green"
                        color_1784 = "green"
                    elif kehang == 2:
                        color_1782 = "green"
                        color_1783 = "red"
                        color_1784 = "green"
                    elif kehang == 3:
                        color_1782 = "green"
                        color_1783 = "green"
                        color_1784 = "red"
                except queue_module.Empty:
                    pass  # Không có gì trong queue thì bỏ qua, tiếp tục loop

                time.sleep(0.1)
                uwb_list = read_data(conn)
                ic("ALO")
                node_count = 0
                for one in uwb_list:
                    anchor_id = one.get("A")
                    range_val = float(one.get("R", 0))
                    if anchor_id == "1782":
                        a1_range = range_val
                        set_anchor_color("1782", color_1782)
                        node_count += 1
                    elif anchor_id == "1783":
                        a2_range = range_val
                        set_anchor_color("1783", color_1783)
                        node_count += 1
                    elif anchor_id == "1784":
                        a3_range = range_val
                        set_anchor_color("1784", color_1784)
                        node_count += 1

                if node_count == 3:
                    try:
                        x, y = trilateration(a1_range, a2_range, a3_range)
                        clean(t_a3)
                        draw_uwb_tag(x, y, "TAG", t_a3)
                    except ZeroDivisionError:
                        ic("Trilateration failed.")

                turtle.update()
                time.sleep(0.1)
                # ic('Queue')

        except KeyboardInterrupt:
            ic("Shutting down...")
        finally:
            conn.close()
            sock.close()


    main_turtle()


if __name__ == "__main__":
    main()


