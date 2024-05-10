import tkinter as tkk
from tkinter import messagebox, font, simpledialog, WORD
from Patient_Data import *
import csv
import datetime
import os


class MyWindow:
    def __init__(self):

        self.window = tkk.Tk()
        self.window.title('Patient Data Management')
        self.window.geometry('700x500')

        self.center_window()

        self.role_frame = tkk.Frame(self.window)
        self.role_label = tkk.Label(self.role_frame, text='Role')

        custom_font = font.Font(family='Helvetica', size=16, weight='bold')
        self.role_label.config(font=custom_font)

        self.role_label.grid(row=0, column=0, columnspan=1, sticky='news')

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

        self.buttons_list = []

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
            commands = [self.generate_key_statistics, self.exit]
        else:
            button_texts = ['Retrieve_patient', 'Add_patient', 'Remove_patient', 'Count_visits', 'Exit']
            commands = [self.retrieve_patient, self.add_patient, self.remove_patient, self.count_visit, self.exit]

        self.buttons = []
        for i, text in enumerate(button_texts):
            button = tkk.Button(self.button_frame, text=text, width=17, command=commands[i])
            button.grid(row=0, column=i, padx=10, pady=10)
            self.buttons.append(button)

        self.button_frame.pack(side='bottom', pady=50)

    def insert_tb(self, result):

        self.tb.configure(state='normal')
        self.tb.insert(tkk.END, result)
        self.tb.configure(state='disabled')

    def login(self):

        current_datetime = datetime.datetime.now()
        self.formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        username = self.username_entry.get()
        password = self.password_entry.get()

        # Read in credential file
        credential_file = r'../data/Project_credentials.csv'
        self.patient_file = r'../data/Project_patient_information.csv'

        credentials = read_credential_file(credential_file)

        if username in credentials.keys() and credentials[username]['password'] == password:

            self.buttons_list.append('Successful Login')

            existing_data = read_file(self.patient_file)
            self.all_data = Data_Functions(existing_data)

            user = Users(credentials, username)

            self.role = user.find_user_role().title()

            self.login_frame.pack_forget()
            self.role_label.config(text=f'Role: {self.role}')
            self.role_frame.pack(pady=10)

            self.tb = tkk.Text(self.window, height=10, width=62, wrap=WORD)
            self.tb.pack()
            self.tb.configure(state='disabled')

            self.generate_buttons(credentials[username]["role"])
        else:
            self.buttons_list.append('Failed Login')
            self.write_usage_stats_to_csv()
            messagebox.showerror('Login Error', 'Invalid username or password. Please try again.')

    def temporal_trend(self):

        output = ''
        output += 'Temporal Trend of the number of patients who visited the hospital yearly\n'
        output += '\n'
        months_translated = {'1': 'January', '2': 'February', '3': 'March',
                             '4': 'April', '5': 'May', '6': 'June',
                             '7': 'July', '8': 'August', '9': 'September',
                             '10': 'October', '11': 'November', '12': 'December'}
        years = {}

        for patient, value in self.all_data.data.items():
            for visit, value1 in value.items():
                year_string = value1['Visit_time']
                year = year_string.split('-')[0]
                month = year_string.split('-')[1]

                if year in years:
                    years[year][str(month)] += 1
                else:
                    months = {'1': 0, '2': 0, '3': 0,
                              '4': 0, '5': 0, '6': 0,
                              '7': 0, '8': 0, '9': 0,
                              '10': 0, '11': 0, '12': 0}

                    years[year] = months
                    years[year][str(month)] = 1

        years = dict(sorted(years.items()))

        for year in years:
            output += f'Year: {year}\n'
            output += '\n'

            data = years[year]

            for mo in data.keys():
                output += f'{months_translated[mo]}: {data[mo]}\n'

            output += '--------------------\n'
            output += '\n'

        return output

    def generate_key_statistics(self):

        self.buttons_list.append('Generate key statistics')

        self.tb.configure(state='normal')
        self.tb.delete('1.0', tkk.END)

        if self.role == "Admin":
            visit_date = simpledialog.askstring("Patient Visit Information",
                                                "For Patient(s) visit information, Please enter Visit Date (yyyy-mm-dd): ")
            result = self.all_data.count_visits(visit_date)
            self.insert_tb(result)

        elif self.role == "Management":
            result = self.temporal_trend()
            self.insert_tb(result)

    def retrieve_patient(self):

        self.buttons_list.append('Retrieve patient')

        self.tb.configure(state='normal')
        self.tb.delete('1.0', tkk.END)

        patient_id = simpledialog.askstring("Retrieve Patient",
                                            "For Retrieval, Please enter Patient ID: ")

        output = self.all_data.retrieve_patient(patient_id)

        if output == f"Visit ID does not exist for Patient {patient_id}":
            messagebox.showerror('Visit ID Error', 'Visit ID does not exist!')
            self.insert_tb(output)
        elif output == '':
            pass
        else:
            messagebox.showinfo('Patient Retrieved', f'Patient {patient_id} has been found!')
            self.insert_tb(output)

    def add_patient(self):

        self.buttons_list.append('Add patient')

        hi = 0

    def remove_patient(self):

        self.buttons_list.append('Remove patient')

        patient_id = simpledialog.askstring("Remove Patient",
                                            "For Removal, Please enter Patient ID: ")
        output = self.all_data.remove_patient(patient_id)

        if output == "Patient ID does not exist.":
            messagebox.showerror('Patient ID Error', 'Patient ID does not exist!')
        else:
            messagebox.showinfo('Patient ID Removed', output)
            self.write_back_to_csv()

    def count_visit(self):

        self.buttons_list.append('Count visits')

        self.tb.configure(state='normal')
        self.tb.delete('1.0', tkk.END)

        visit_date = simpledialog.askstring("Patient Visit Information",
                                            "For Patient(s) visit information, Please enter Visit Date (yyyy-mm-dd): ")

        result = self.all_data.count_visits(visit_date)
        self.insert_tb(result)

    def run(self):
        self.window.mainloop()

    def write_back_to_csv(self):

        with open(self.patient_file, 'w', newline='') as csvfile:
            headers = ['', 'Patient_ID', 'Visit_ID', 'Visit_time', 'Visit_department', 'Race', 'Gender',
                       'Ethnicity', 'Age', 'Zip_code', 'Insurance', 'Chief_complaint', 'Note_ID', 'Note_type']

            writer = csv.writer(csvfile)
            writer.writerow(headers)

            count = 0
            for pt_id in self.all_data.data:
                for key in self.all_data.data[pt_id]:
                    tmp_list = []
                    for key1, value1 in self.all_data.data[pt_id][key].items():
                        tmp_list.append(value1)
                    row_to_write = [str(count), pt_id, key] + tmp_list
                    writer.writerow(row_to_write)
                    count += 1

    def write_usage_stats_to_csv(self):

        data_file = r'..\data\Project_usage_information.csv'

        file_empty = os.stat(data_file).st_size == 0

        with open(data_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write headers only if the file is empty
            if file_empty:
                headers = ['Username', 'Role', 'Actions Performed', 'Time of Log-in']
                writer.writerow(headers)

            if 'Failed Login' in self.buttons_list:
                tmp_list = [self.username_entry.get(), 'None', self.buttons_list, self.formatted_datetime]
            else:
                tmp_list = [self.username_entry.get(), self.role, self.buttons_list, self.formatted_datetime]
            writer.writerow(tmp_list)

    def exit(self):
        self.buttons_list.append('Exit')
        self.write_usage_stats_to_csv()
        self.window.quit()


if __name__ == "__main__":

    window = MyWindow()
    window.run()
