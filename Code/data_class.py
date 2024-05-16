from tkinter import messagebox, simpledialog
import Patient_Data as pdd
import pat_data


class Data_Functions():
    def __init__(self, data):
        self.data = data

    def add_patient(self):
        pt_id = simpledialog.askstring("Patient ID", "Enter the Patient ID: ")
        if pt_id not in self.data.keys():
            Visit_ID = simpledialog.askstring("Visit ID", "Enter the visit ID: ")
        else:
            Visit_ID = pdd.generate_visit_ID()

        Visit_time = simpledialog.askstring("Visit Time", "Enter the visit time (yyyy-mm-dd): ")
        Gender = simpledialog.askstring("Gender", "Enter the Gender of the patient (Male, Female or Non-Binary): ")
        Race = simpledialog.askstring("Race",
            "Enter the Race of the patient (White, Black, Asian, Pacific islanders, Native Americans or Unknown): ")
        Visit_department = simpledialog.askstring("Visit Department", "Enter the department: ")
        Age = simpledialog.askstring("Age", "Enter Patient Age: ")
        Ethnicity = simpledialog.askstring("Ethnicity", "Enter the Patient's ethnicity (Hispanic, Non-Hispanic, Other, Unknown): ")
        Insurance = simpledialog.askstring("Insurance", "Enter Patient Insurance(Medicare, Medicaid, None, Unknown): ")
        Zip_code = simpledialog.askstring("Zip Code", "Enter Patient Zip Code: ")
        Chief_complaint = simpledialog.askstring("Chief Complaint", "Enter Patient Complaint: ")
        Note_ID = simpledialog.askstring("Note ID", "Enter Patient Note ID: ")
        Note_type = simpledialog.askstring("Note Type", "Enter Patient Note Type: ")

        pt_data = pat_data.add_patient_data(Visit_time, Gender, Race, Visit_department, Age, Ethnicity, Insurance, Zip_code,
                                            Chief_complaint, Note_ID, Note_type)
        pt_data_dict = pdd.patient_data_to_dict(pt_data)

        if pt_id not in self.data.keys():
            self.data[pt_id] = {Visit_ID: pt_data_dict}
        else:
            self.data[pt_id].update({Visit_ID: pt_data_dict})

        output = 'Patient was added!'
        return output

    def remove_patient(self, pt_id):
        output = ''
        if pt_id not in self.data.keys():
            output += "Patient ID does not exist."
        else:
            del self.data[pt_id]
            output += f"Patient {pt_id} has been removed."
        return output

    def retrieve_patient(self, pt_id):
        output = ''
        if pt_id not in self.data.keys():
            messagebox.showerror('Patient ID Error', 'Patient ID does not exist!')
        else:
            Visit_ID = simpledialog.askstring("Visit ID", "Enter the visit ID: ")
            pt_id_dict = self.data[pt_id]
            if Visit_ID in pt_id_dict.keys():
                for key, value in pt_id_dict[Visit_ID].items():
                    output += f"{key}: {value}\n"
            else:
                output += f"Visit ID does not exist for Patient {pt_id}"

        return output

    def count_visits(self, visit_date):

        visit_dates = []
        output = ''
        for key1, value1 in self.data.items():
            for key2, value2 in value1.items():
                visit_dates.append(value2['Visit_time'])

        if visit_date not in visit_dates:
            output += 'Date not found!'
        else:
            total_patient_count = 0
            for key1, value1 in self.data.items():
                ind_patient_count = 0
                for key2, value2 in value1.items():
                    if value2['Visit_time'] == visit_date:
                        total_patient_count += 1
                        ind_patient_count += 1

                if ind_patient_count > 0:
                    output += f'On {visit_date}, Patient {key1} came {ind_patient_count} time(s)\n'
            output += f'On {visit_date}, there were a total of {total_patient_count} patients that came.\n'
        return output