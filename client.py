import socket
import tkinter
import tkinter.messagebox
import threading
import json
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText

host = ''
port = ''
user = ''
listbox1 = ''  # online users listbox
show = 1  # listbox shown or not
users = []  # online users list
chat = '------Group chat-------'

#log in
root0 = tkinter.Tk()
root0.geometry("300x150")
root0.title('Log In')
root0.resizable(0,0)
one = tkinter.Label(root0,width=300,height=150,bg="LightBlue")
one.pack()

host0 = tkinter.StringVar()
host0.set('')
USER = tkinter.StringVar()
USER.set('')

labelhost = tkinter.Label(root0,text='host address',bg="LightBlue")
labelhost.place(x=20,y=20,width=100,height=40)
entryhost = tkinter.Entry(root0, width=60, textvariable=host0)
entryhost.place(x=120,y=25,width=100,height=30)

labelUSER = tkinter.Label(root0,text='User name',bg="LightBlue")
labelUSER.place(x=20,y=70,width=100,height=40)
entryUSER = tkinter.Entry(root0, width=60, textvariable=USER)
entryUSER.place(x=120,y=75,width=100,height=30)

def Login(*args):
    global host, port, user
    host, port = entryhost.get().split(':')
    user = entryUSER.get()
    if not user:
        tkinter.messagebox.showwarning('warning', message='User name is empty')
    else:
        root0.destroy()

loginButton = tkinter.Button(root0, text ="Log in", command = Login,bg="Yellow")
loginButton.place(x=135,y=110,width=40,height=25)
root0.bind('<Return>', Login)

root0.mainloop()

# Build Connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, int(port)))
if user:
    s.send(user.encode())
else:
    s.send('User name no found'.encode())
    user = host + ':' + port

# Chatting window
root1 = tkinter.Tk()
root1.geometry("640x480")
root1.title('Group Chat')
root1.resizable(0,0)

# Message window
listbox = ScrolledText(root1)
listbox.place(x=5, y=0, width=640, height=320)
listbox.tag_config('tag1', foreground='red',backgroun="yellow")
listbox.insert(tkinter.END, 'Welcome to the group chat', 'tag1')

INPUT = tkinter.StringVar()
INPUT.set('')
entryIuput = tkinter.Entry(root1, width=120, textvariable=INPUT)
entryIuput.place(x=5,y=320,width=580,height=170)

# online user list
listbox1 = tkinter.Listbox(root1)
listbox1.place(x=510, y=0, width=130, height=320)


def send(*args):
    message = entryIuput.get() + '~' + user + '~' + chat
    s.send(message.encode())
    INPUT.set('')

sendButton = tkinter.Button(root1, text ="\nsend\n\n\nmessage",anchor = 'n',command = send,font=('Helvetica', 18),bg = 'white')
sendButton.place(x=585,y=320,width=55,height=300)
root1.bind('<Return>', send)


def receive():
    global uses
    while True:
        data = s.recv(1024)
        data = data.decode()
        print(data)
        try:
            uses = json.loads(data)
            listbox1.delete(0, tkinter.END)
            listbox1.insert(tkinter.END, "Users online")
            listbox1.insert(tkinter.END, "------Group chat-------")
            for x in range(len(uses)):
                listbox1.insert(tkinter.END, uses[x])
            users.append('------Group chat-------')
        except:
            data = data.split('~')
            message = data[0]
            userName = data[1]
            chatwith = data[2]
            message = '\n' + message
            if chatwith == '------Group chat-------':   # Group chat
                if userName == user:
                    listbox.insert(tkinter.END, message)
                else:
                    listbox.insert(tkinter.END, message)
            elif userName == user or chatwith == user:  # Private chat
                if userName == user:
                    listbox.tag_config('tag2', foreground='red')
                    listbox.insert(tkinter.END, message, 'tag2')
                else:
                    listbox.tag_config('tag3', foreground='green')
                    listbox.insert(tkinter.END, message,'tag3')

            listbox.see(tkinter.END)
r = threading.Thread(target=receive)
r.start()

root1.mainloop()
s.close()
