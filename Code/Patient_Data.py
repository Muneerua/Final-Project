import sys
import random


def read_file(filename):
    with open(filename, 'r') as f:
        data_element_names = f.readline()
        data_element_names = data_element_names.strip().split(',')

        data = {}
        for line in f.readlines():
            line = line.strip().split(',')
            data_visitid = {}
            data_tmp = {}
            for i in range(len(line)):
                if i > 2:
                    data_tmp[data_element_names[i]] = line[i]
            data_visitid[line[2]] = data_tmp
            data[line[1]] = data_visitid

        return data


def read_credential_file(filename):
    with open(filename, 'r') as f:
        data_element_names = f.readline()
        data_element_names = data_element_names.strip().split(',')

        data = {}
        for line in f.readlines():
            line = line.strip().split(',')
            user_dict = {}
            for i in range(len(line)):
                user_dict['password'] = line[2]
                user_dict['role'] = line[3]
            data[line[1]] = user_dict

    return data


def generate_visit_ID():
    n = 6
    Visit_ID = "".join(["{}".format(random.randint(0, 9)) for num in range(0, n)])
    return Visit_ID


def patient_data_to_dict(patient_data_obj):
    return {"Visit_time": patient_data_obj.Visit_time,
            "Gender": patient_data_obj.Gender,
            "Race": patient_data_obj.Race,
            "Visit_department": patient_data_obj.Visit_department,
            "Age": patient_data_obj.Age,
            "Ethnicity": patient_data_obj.Ethnicity,
            "Insurance": patient_data_obj.Insurance,
            "Zip_code": patient_data_obj.Zip_code,
            "Chief_complaint": patient_data_obj.Chief_complaint,
            "Note_ID": patient_data_obj.Note_ID,
            "Note_type": patient_data_obj.Note_type
            }


class Patient_data():
    def __init__(self, Visit_time, Gender, Race, Visit_department, Age, Ethnicity, Insurance, Zip_code, Chief_complaint,
                 Note_ID, Note_type):
        self.Visit_time = Visit_time
        self.Visit_department = Visit_department
        self.Gender = Gender
        self.Race = Race
        self.Age = Age
        self.Ethnicity = Ethnicity
        self.Insurance = Insurance
        self.Zip_code = Zip_code
        self.Chief_complaint = Chief_complaint
        self.Note_ID = Note_ID
        self.Note_type = Note_type


class Data_Functions():
    def __init__(self, data):
        self.data = data

    def add_patient(self):
        pt_id = input("Enter the Patient ID: ")
        if pt_id not in self.data.keys():
            Visit_ID = input("Enter the visit ID: ")
        else:
            Visit_ID = generate_visit_ID()

        Visit_time = input("Enter the visit time (yyyy-mm-dd): ")
        Gender = input("Enter the Gender of the patient (Male, Female or Non-Binary): ")
        Race = input(
            "Enter the Race of the patient (White, Black, Asian, Pacific islanders, Native Americans or Unknown): ")
        Visit_department = input("Enter the department: ")
        Age = input("Enter Patient Age: ")
        Ethnicity = input("Enter the Patient's ethnicity (Hispanic, Non-Hispanic, Other, Unknown): ")
        Insurance = input("Enter Patient Insurance(Medicare, Medicaid, None, Unknown): ")
        Zip_code = input("Enter Patient Zip Code: ")
        Chief_complaint = input("Enter Patient Complaint: ")
        Note_ID = input("Enter Patient Note ID: ")
        Note_type = input("Enter Patient Note Type: ")

        pt_data = Patient_data(Visit_time, Gender, Race, Visit_department, Age, Ethnicity, Insurance, Zip_code,
                               Chief_complaint, Note_ID, Note_type)
        pt_data_dict = patient_data_to_dict(pt_data)

        if pt_id not in self.data.keys():
            self.data[pt_id] = {Visit_ID: pt_data_dict}
        else:
            self.data[pt_id].update({Visit_ID: pt_data_dict})
        print(self.data)

    def remove_patient(self):
        pt_id = input("For Removal, Please Enter Patient ID: ")
        if pt_id not in self.data.keys():
            print("Patient ID does not exist.")
        else:
            del self.data[pt_id]
            print(f"Patient {pt_id} has been removed.")
        print(self.data)

    def retrieve_patient(self):
        pt_id = input("For Retrieval, Please Enter Patient ID: ")
        if pt_id not in self.data.keys():
            print("Patient ID does not exist.")
        else:
            Visit_ID = input("Enter the visit ID: ")
            pt_id_dict = self.data[pt_id]
            if Visit_ID in pt_id_dict.keys():
                print(pt_id_dict[Visit_ID])
            else:
                print(f"Visit ID does not exist for Patient {pt_id}")

    def count_visits(self):
        visit_date = input("For Patient(s) visit information, Please enter Visit Date (yyyy-mm-dd): ")

        visit_dates = []

        for key1, value1 in self.data.items():
            for key2, value2 in value1.items():
                visit_dates.append(value2['Visit_time'])

        if visit_date not in visit_dates:
            print('Date not found!')
        else:
            total_patient_count = 0
            for key1, value1 in self.data.items():
                ind_patient_count = 0
                for key2, value2 in value1.items():
                    if value2['Visit_time'] == visit_date:
                        total_patient_count += 1
                        ind_patient_count += 1

                if ind_patient_count > 0:
                    print(f'On {visit_date}, Patient {key1} came {ind_patient_count} time(s)')

            print(f'On {visit_date}, there were a total of {total_patient_count} patients that came')


class Users():
    def __init__(self, data, username):
        self.data = data
        self.username = username

    def find_user_role(self):

        role = self.data[self.username]['role']
        return role


if __name__ == "__main__":

    credential_file = sys.argv[1]
    patient_file = sys.argv[-1]

    credential_data = read_credential_file(credential_file)
    existing_data = read_file(patient_file)

    all_data = Data_Functions(existing_data)

    while True:
        user_name = input("Enter your username: ")

        if user_name == 'Stop':
            print('Program has stopped')
            break
        elif user_name in credential_data.keys():
            user_data = Users(credential_data, user_name)

            password = input("Enter your password: ")
            if password == credential_data[user_name]['password']:

                if user_data.find_user_role() == 'management':

                    print('Temporal Trend of the number of patients who visited the hospital yearly')

                    months_translated = {'1': 'January', '2': 'February', '3': 'March',
                                         '4': 'April', '5': 'May', '6': 'June',
                                         '7': 'July', '8': 'August', '9': 'September',
                                         '10': 'October', '11': 'November', '12': 'December'}
                    years = {}

                    for patient, value in existing_data.items():
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
                        print(f'Year: {year}\n')

                        data = years[year]

                        for mo in data.keys():
                            print(f'{months_translated[mo]}: {data[mo]}')

                        print('--------------------')
                    break
                elif user_data.find_user_role()  == 'admin':
                    all_data.count_visits()
                    print('Program has stopped')
                    break
                elif user_data.find_user_role()  == 'nurse' or user_data.find_user_role()  == 'clinician':
                    while True:
                        user_input = input("What do you want to do? [Add_patient, Remove_patient, Retrieve_patient, Count_visits] ")

                        if user_input == 'Stop':
                            print('Program has stopped')
                            break
                        elif user_input == "Add_patient":
                            all_data.add_patient()
                        elif user_input == "Remove_patient":
                            all_data.remove_patient()
                        elif user_input == "Retrieve_patient":
                            all_data.retrieve_patient()
                        elif user_input == "Count_visits":
                            all_data.count_visits()
                        else:
                            print('Invalid option. Select from [Add_patient, Remove_patient, Retrieve_patient, Count_visits] ')

            else:
                print("Incorrect password. Try Again!")
                break
        else:
            print('No match found')
            break


