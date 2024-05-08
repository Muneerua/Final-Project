import tkinter as tkk
from tkinter import messagebox, font
from Patient_Data import *


class MyWindow:
    def __init__(self):

        self.window = tkk.Tk()
        self.window.title('Patient Data Management')
        self.window.geometry('700x500')
        # self.window.configure(bg='#333333')

        self.center_window()

        self.role_frame = tkk.Frame(self.window)
        self.role_label = tkk.Label(self.role_frame, text='Role')
        # Change font size of role label
        custom_font = font.Font(family='Helvetica', size=16, weight='bold')  # Define custom font
        self.role_label.config(font=custom_font)

        self.role_label.grid(row=0, column=0, columnspan=1, sticky='news')

        # self.role_frame.pack(pady=10)

        self.login_frame = tkk.Frame(self.window)

        login_label = tkk.Label(self.login_frame, text='Login')
        login_label.grid(row=0, column=0, columnspan=2, sticky='news')

        username_label = tkk.Label(self.login_frame, text='Username')
        username_label.grid(row=1, column=0)

        self.username_entry = tkk.Entry(self.login_frame)
        self.username_entry.grid(row=1, column=1)

        password_label = tkk.Label(self.login_frame, text='Password')
        password_label.grid(row=2, column=0)

        self.password_entry = tkk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=2, column=1)

        login_button = tkk.Button(self.login_frame, text='Login', command=self.login)
        login_button.grid(row=3, column=0, columnspan=2)

        self.login_frame.pack(pady=50)

        self.button_frame = tkk.Frame(self.window)

        self.window.mainloop()

    def center_window(self):
        # Calculate the position to center the window on the screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        window_width = 750
        window_height = 500

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def generate_buttons(self, role):

        if role == "admin" or role == "management":
            button_texts = ['Generate key statistics', 'Exit']
            commands = [self.generate_key_statistics, self.window.quit]
        else:
            button_texts = ['Retrieve_patient', 'Add_patient', 'Remove_patient', 'Count_visits', 'Exit']
            commands = [self.retrieve_patient, self.add_patient, self.remove_patient, self.count_visit, self.window.quit]

        self.buttons = []
        for i, text in enumerate(button_texts):
            button = tkk.Button(self.button_frame, text=text, width=17, command=commands[i])
            button.grid(row=0, column=i, padx=10, pady=10)
            self.buttons.append(button)

        self.button_frame.pack(side='bottom', pady=50)

    def login(self):

        username = self.username_entry.get()
        password = self.password_entry.get()

        # Read in credential file
        credential_file = r'../data/Project_credentials.csv'
        patient_file = r'../data/Project_patient_information.csv'

        credentials = read_credential_file(credential_file)

        if username in credentials.keys() and credentials[username]['password'] == password:

            existing_data = read_file(patient_file)
            self.all_data = Data_Functions(existing_data)

            self.login_frame.pack_forget()
            self.role_label.config(text=f'Role: {credentials[username]["role"].title()}')
            self.role_frame.pack(pady=10)
            self.generate_buttons(credentials[username]["role"])
        else:
            messagebox.showerror('Login Error', 'Invalid username or password. Please try again.')

    def generate_key_statistics(self):
        self.all_data.count_visits()

    def retrieve_patient(self):
        hi = 0

    def add_patient(self):
        hi = 0

    def remove_patient(self):
        hi = 0

    def count_visit(self):
        self.all_data.count_visits()


if __name__ == "__main__":

    window = MyWindow()
