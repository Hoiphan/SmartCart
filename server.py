import socket
import threading
import cv2
import mysql.connector

TCP_IP = "0.0.0.0"
TCP_PORT = 5005

UDP_URL = "udp://192.168.0.103:1234"

# Kết nối MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="000000",
        database="SmartCart"
    )


def save_to_mysql(weight, voltage):
    try:
        db = connect_db()
        cursor = db.cursor()
        sql = "INSERT INTO Cart (weight, voltage) VALUES (%s, %s)"
        cursor.execute(sql, (weight, voltage))
        db.commit()
        cursor.close()
        db.close()
        print(f"Lưu thành công: {weight} g | {voltage} V")
    except Exception as e:
        print("Lỗi lưu MySQL:", e)

def receive_tcp_data():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_IP, TCP_PORT))
    server_socket.listen(1)

    print(f"Listen IP/PORT {TCP_IP}:{TCP_PORT}...")

    conn, addr = server_socket.accept()
    print(f"addr {addr}")

    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            print(f"data: {data}")
            weight, voltage = map(float, data.split(","))
            save_to_mysql(weight, voltage)
        except Exception as e:
            print("Lỗi:", e)
            break

    conn.close()
    server_socket.close()
    print("đóng kết nối TCP.")


def stream_video():
    cap = cv2.VideoCapture(UDP_URL, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        print("Không video!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không frame!")
            break

        cv2.imshow("Stream Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


thread_tcp = threading.Thread(target=receive_tcp_data)
thread_udp = threading.Thread(target=stream_video)

thread_tcp.start()
thread_udp.start()

thread_tcp.join()
thread_udp.join()


