import tkinter as tkk
from Patient_Data import *


class MyWindow:
    def __init__(self):

        # Read in credential file
        credential_file = 'PA3_credentials.txt'

        window = tkk.Tk()
        window.title('Patient Data Management')
        window.geometry('700x500')
        window.eval('tk::PlaceWindow . center')
        window.configure(bg='#333333')

        frame = tkk.Frame()

        login_label = tkk.Label(frame, text='Login')
        login_label.grid(row=0, column=0, columnspan=2, sticky='news')

        username_label = tkk.Label(frame, text='Username')
        username_label.grid(row=1, column=0)

        username_entry = tkk.Entry(frame)
        username_entry.grid(row=1, column=1)

        password_label = tkk.Label(frame, text='Password')
        password_label.grid(row=2, column=0)

        password_entry = tkk.Entry(frame, show='*')
        password_entry.grid(row=2, column=1)

        login_button = tkk.Button(frame, text='Login', command=read_credential_file(credential_file))
        login_button.grid(row=3, column=0, columnspan=2)

        frame.pack()

        window.mainloop()


if __name__ == "__main__":

    window = MyWindow()
