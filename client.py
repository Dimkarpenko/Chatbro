import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import ttk

msg = tkinter.Tk()
msg.iconbitmap(default='favicon.ico')
msg.resizable(0,0)
msg.withdraw()

addr = simpledialog.askstring('Host', 'Please, choose a host')

if addr is None:
    quit()
addr = addr.split(':')
HOST = addr[0]
try:
    PORT = int(addr[1])
except:
    messagebox.showerror('Unknown port','Unknown port.\nPlease, chek correcting of the\nport and try again.')
class Client:

    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host, port))
        except:
            messagebox.showerror('Unknown host','Unknown host.\nPlease, chek correcting of the\nhostname and try again.')
            quit()
        
        self.nickname = simpledialog.askstring('Nickname', 'Please, choose a nickname',parent=msg)

        if self.nickname is None:
            quit()

        elif ' ' in self.nickname or self.nickname == '':
            messagebox.showerror('Incorrect nickname','Incorrect nickname.\nPlease, chek correcting of the\nnickname and try again.')
            quit()

        self.gui_done = False
        self.running = True
        
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title(f"ChatBro - {self.nickname} - {HOST}:{PORT}")
        self.win.configure(bg="lightgray")
        self.win.resizable(0,0)
        self.win.iconbitmap('favicon.ico')

        self.chat_label = tkinter.Label(self.win, text="Chat:",bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message:",bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send",command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol('WM_DELETE_WINDOW',self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        try:
            self.sock.send(message.encode('utf-8'))
            self.input_area.delete('1.0', 'end')
        except:
            messagebox.showerror('Connection error','Connection error\nPlease, check your connection or change your nickname.')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                #elif message == 'stop':
                    #self.running = False
                    #messagebox.showerror('Nickname is already in use','This nickname is already in use.\nPlease, try again with a different nickname')
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                self.sock.close()
                break

client = Client(HOST,PORT)