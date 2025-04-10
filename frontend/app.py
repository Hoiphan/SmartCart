
import itertools
import time
import streamlit as st
from backend.service.product_searching_service import ProductSearching
from backend.service.func_prompt import res_gemini
from backend.service.voice_speech_to_text import speech_to_text
from streamlit_float import *
import pandas as pd
import numpy as np
import time
from datetime import datetime




def main():
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Chọn trang:", ["Trang chủ", "Sản phẩm", "Trợ lý","Thiết bị", "Liên hệ"])
    
    if page == "Trang chủ":
        home_page()
    if page == "Sản phẩm":
        searching_page()
    elif page == "Trợ lý":
        about_page()
    elif page == "Liên hệ":
        contact_page()
    elif page == "Thiết bị":
        Device()


def home_page():
    st.title("Trang chủ")
    image_paths = ["assets/1.jpg", "assets/2.jpg", "assets/3.jpg"]  # Thay thế bằng danh sách ảnh thực tế
    img_placeholder = st.empty()
    
    for img_path in itertools.cycle(image_paths):
        img_placeholder.image(img_path, use_container_width=True)
        time.sleep(2)
    

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
                        st.image(product['image'], caption=product['product_name'], use_container_width=True)
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


def Device():
    st.title("Dữ liệu Smartcart (Real-Time)")

    # Số lượng điểm dữ liệu cần hiển thị tại mỗi thời điểm
    n_points = 20
    
    # Tạo vùng trống để cập nhật lại chart
    chart_placeholder = st.empty()

    # Dữ liệu thời gian thực
    times = []

    # Sử dụng vòng lặp để cập nhật dữ liệu theo thời gian thực
    while True:
        # Giả lập dữ liệu cho 'weight' và 'voltage'
        np.random.seed(int(time.time()))  # Sử dụng thời gian hiện tại làm seed để đảm bảo dữ liệu ngẫu nhiên
        weight = np.random.normal(100, 10)  # Trọng lượng với trung bình 100kg và độ lệch chuẩn 10
        voltage = np.random.normal(5, 0.1)  # Điện áp với trung bình 5V và độ lệch chuẩn 0.1

        # Lấy thời gian hiện tại
        current_time = datetime.now()

        # Thêm thời gian và dữ liệu vào danh sách
        times.append(current_time)
        
        # Giới hạn số điểm dữ liệu hiển thị
        if len(times) > n_points:
            times.pop(0)

        # Tạo DataFrame
        chart_data = pd.DataFrame({
            'Time': times,
            'Weight (kg)': np.random.normal(100, 10, len(times)),
            'Voltage (V)': np.random.normal(5, 0.1, len(times))
        })

        # Hiển thị dữ liệu dạng bảng
        # chart_placeholder.write(chart_data)

        # Hiển thị biểu đồ line chart
        chart_placeholder.line_chart(chart_data.set_index('Time'))

        # Dừng lại 1 giây để mô phỏng cập nhật dữ liệu theo thời gian thực
        time.sleep(3)


if __name__ == "__main__":
    main()