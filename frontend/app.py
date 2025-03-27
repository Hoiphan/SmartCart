import itertools
import time
import streamlit as st
from backend.service.product_searching_service import ProductSearching
from backend.service.func_prompt import res_gemini

def main():
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Chọn trang:", ["Trang chủ", "Sản phẩm", "Trợ lý", "Liên hệ"])
    
    if page == "Trang chủ":
        home_page()
    if page == "Sản phẩm":
        searching_page()
    elif page == "Trợ lý":
        about_page()
    elif page == "Liên hệ":
        contact_page()

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
    st.title("Trợ lý")
    user_input = st.text_input("Nhập gì đó:")
    if user_input:
        response = res_gemini(user_input)
        st.write(response)

def contact_page():
    st.title("Liên hệ")
    st.write("Bạn có thể liên hệ chúng tôi qua email: contact@example.com")

if __name__ == "__main__":
    main()