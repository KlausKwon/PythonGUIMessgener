#소켓 라이브러리 생성
import socket

#스레딩 라이브러리 생성
import threading

#포트번호 8000
PORT = 8000 

#서버 IPv4주소
#gethostbyname() 함수는 호스트의 IP주소 반환 192.168.56.1 반환
SERVER = socket.gethostbyname(socket.gethostname())

# 튜플 형식(IP(SERVER 변수넣으면 에러), 포트)
ADDRESS = ("", PORT)

#인코딩 및 디코딩이 발생하는 형식
FORMAT = "utf-8"

#리스트에는 서버 및 이름(별칭)에 연결된 클라이언트들을 포함
clients, names = [], []


#서버에 새로운 소켓 생성
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#서버 주소를 소켓에 바인드
server.bind(ADDRESS)

#연결을 시작하는 함수

def startChat():
    print("server is working on" + SERVER)
    
    #listening 통신 준비중
    server.listen()
    
    while True:
        
        #연결을 받아들임 반환 값은 (conn, address) conn는 연결에서 
        #데이터를 보내고 받을 수 있는 새로운 소켓 객체
        #address는 연결의 다른 끝에 있는 소켓에 바인드된 주소 
        conn, addr = server.accept()
        conn.send("NAME".encode(FORMAT))
        
        #데이터를 받을 수 있는 최대 양 -> 1024
        name = conn.recv(1024).decode(FORMAT)
        
        #이름(별칭)과 클라이언트를 각 리스트에 추가
        names.append(name)
        clients.append(conn)
        
        print(f"Name is: {name}")
        
        #브로드캐스트 메세지 함수 활용
        broadcastMessage(f"{name}님이 입장하셨습니다.".encode(FORMAT))
        
        conn.send('연결 성공'.encode(FORMAT))
        
        #스레드 핸들링 시작
        thread = threading.Thread(target=handle, args=(conn,addr))
        
        thread.start()
        
        #서버에 연결된 클라이언트 수 
        print(f"active connections {threading.activeCount() - 1}")
        

#들어오는 메시지 다루는 방법

def handle(conn, addr):
    print(f"new connection {addr}")
    connected = True
    
    while connected:
        #메세지 받기
        message = conn.recv(1024)
        
        #브로드캐스트 메시지
        broadcastMessage(message)
        
    #연결 끊기    
    conn.close()
    
def broadcastMessage(message):
    for client in clients:
        client.send(message)
        
        
#통신시작
startChat()