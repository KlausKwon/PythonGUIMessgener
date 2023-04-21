#1~6 필요한 모듈 불러오기
import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk

#포트, 서버주소, 주소(서버주소, 포트),  인코딩, 디코딩 형식 -> utf-8
PORT = 8000
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

#클라이언트 소켓 생성하고 서버에 연결
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


#채팅 프로그램 GUI
class GUI:
    #생산자 메서드
    def __init__(self):
        
        #윈도우 기반 채팅창 화면 가려져 있는 상태임
        self.Window = Tk()
        self.Window.withdraw()
        
        #로그인 창 생성
        self.login = Toplevel()
        # 윈도우 창 제목 설정 
        self.login.title("Login")
        #윈도우 창 너비, 높이 설정 False -> 크기 조절 불가능
        self.login.resizable(width=False,height=False)
        #너비 400 높이 300 설정
        self.login.configure(width=400, height=300)
        
        #Label 생성
        #Please login to continue 문구 생성
        self.pls = Label(self.login, text = "Please login to continue",
                         justify = CENTER, 
                         font = "Helvetica 14 bold")
        
        #Label 위치 지정
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)
        
        #create a Label
        #Name: 문구 생성
        self.labelName = Label(self.login, text="Name: ", 
                               font = "Helvetica 12")
        #label 위치 지정 relx, rely -> x,y 좌표 배치 비율 relheight -> 위젯의 높이 비율 
        self.labelName.place(relheight=0.2, relx=0.1, rely=0.22)
        
        
        #닉네임 입력할 입력칸 생성
        self.entryName = Entry(self.login,
                               font="Helvetica 14")
        #입력칸 위치 지정 # relx, rely -> x,y 좌표 배치 비율 relwidth, relheight -> 위젯의 너비, 높이 비율 
        self.entryName.place(relwidth=0.4, relheight=0.1, relx=0.3, rely=0.26)
        
        #커서 설정(커서 깜빡거림)
        self.entryName.focus()
        
        #Continue(계속) 버튼 생성 누르면 입력받은 Name으로 goAhead 함수 실행
        #계속 버튼 누르면 기존화면 사라짐
        self.go = Button(self.login, text="계속", font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.4, rely=0.55)
        self.Window.mainloop()
    
    #    
    def goAhead(self, name):
        #위젯 사라짐
        self.login.destroy()
        #새로운 창 실행하는 함수 name->닉네임
        self.layout(name)
        
        #메세지 수신받을 스레드 
        rcv = threading.Thread(target=self.receive)
        rcv.start()
        
    #채팅 메인 레이아웃
    def layout(self, name):
        self.name = name
        #윈도우 창 나타나기 deiconify -> 윈도우창을 정상상태로 복원
        self.Window.deiconify()
        #윈도우 창 왼쪽 위 CHATROOM이라고 뜸
        self.Window.title("CHATROOM")
        #크기 조정 불가
        self.Window.resizable(width=False,height=False)
        #너비 470 높이 550, #17202A -> 색상 16진수
        self.Window.configure(width=470,height=550,bg="#17202A")
        #CHATROOM title 바로 및 설정한 닉네임(하얀색) 표현
        self.labelHead = Label(self.Window, 
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)
        #labelhead 상대너비 1설정
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window, width=450, bg="#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        self.textCons = Text(self.Window, width=20, height=2, 
                             bg="#17202A", fg="#EAECEE",
                             font="Helvetica 14", padx=5, pady=5)
        
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)
        
        self.labelBottom = Label(self.Window, bg="#ABB2B9", height=80)
        
        self.labelBottom.place(relwidth=1, rely=0.825)
        
        self.entryMsg = Entry(self.labelBottom, bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")
        
        #지정된 위젯을 윈도우 gui에 배치
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        
        self.entryMsg.focus()
        
        #보내기 버튼 생성
        self.buttonMsg = Button(self.labelBottom, text="보내기",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendbutton(self.entryMsg.get()))
        
        self.buttonMsg.place(relx=0.77, rely=0.008,
                             relheight=0.06, relwidth=0.22)
        
        self.textCons.config(cursor="arrow")
        
        #스크롤 바 생성
        scrollbar = Scrollbar(self.textCons)
        
        #윈도우 gui에 스크롤 바 지정
        scrollbar.place(relheight=1, relx=0.974)
        
        scrollbar.config(command=self.textCons.yview)
        
        self.textCons.config(state=DISABLED)
        
    #기본적으로 메세지를 보내기 위한 스레드를 시작하는 기능
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
        
    #메세지를 수신받는 기능
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)

                #서버의 메세지가 NAME인경우 클라이언트 이름 전송
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    #문자 박스에 메세지 삽입
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, message+'\n\n')
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                #에러 발생시 명령어줄 또는 콘솔에 에러 출력
                print("An error occurred!")
                client.close()
                break
            
    #메세지 송신기능
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))
            break
        
        
#GUI 클래스 객체 생성
g = GUI()        
                 
        
        
        
        
        