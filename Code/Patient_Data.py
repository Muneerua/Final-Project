import sys
import random
import data_class
import user_class


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


if __name__ == "__main__":

    credential_file = sys.argv[1]
    patient_file = sys.argv[-1]

    credential_data = read_credential_file(credential_file)
    existing_data = read_file(patient_file)

    all_data = data_class.Data_Functions(existing_data)

    while True:
        user_name = input("Enter your username: ")

        if user_name == 'Stop':
            print('Program has stopped')
            break
        elif user_name in credential_data.keys():
            user_data = user_class.Users(credential_data, user_name)

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
                elif user_data.find_user_role() == 'admin':
                    visit_date = input("For Patient(s) visit information, Please enter Visit Date (yyyy-mm-dd): ")

                    print(all_data.count_visits(visit_date))
                    print('Program has stopped')
                    break
                elif user_data.find_user_role() == 'nurse' or user_data.find_user_role() == 'clinician':
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
                            visit_date = input("For Patient(s) visit information, Please enter Visit Date (yyyy-mm-dd): ")

                            print(all_data.count_visits(visit_date))
                        else:
                            print('Invalid option. Select from [Add_patient, Remove_patient, Retrieve_patient, Count_visits] ')

            else:
                print("Incorrect password. Try Again!")
                break
        else:
            print('No match found')
            break


