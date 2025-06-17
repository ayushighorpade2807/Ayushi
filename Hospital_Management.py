from tkinter import *
from tkinter import ttk, messagebox

class Hospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1350x700+0+0")

        # Title
        self.title = Label(self.root, text="+ HOSPITAL MANAGEMENT SYSTEM", font=("times new roman", 30, "bold"), bg="white", fg="red")
        self.title.pack(side=TOP, fill=X)

        # Variables
        self.name_tablet = StringVar()
        self.ref = StringVar()
        self.dose = StringVar()
        self.no_of_tablets = StringVar()
        self.lot = StringVar()
        self.issue_date = StringVar()
        self.exp_date = StringVar()
        self.daily_dose = StringVar()
        self.storage = StringVar()
        self.nhs_number = StringVar()
        self.patient_name = StringVar()
        self.dob = StringVar()
        self.address = StringVar()

        # Info Frame
        InfoFrame = Frame(self.root, bd=10, relief=RIDGE)
        InfoFrame.place(x=0, y=60, width=1350, height=300)

        # Patient Info Frame
        PatientInfoFrame = LabelFrame(InfoFrame, text="Patient Information", font=("arial", 12, "bold"), bd=5)
        PatientInfoFrame.place(x=0, y=0, width=450, height=290)

        Label(PatientInfoFrame, text="Name Of Tablet", font=("arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky=W)
        combo_tablets = ttk.Combobox(PatientInfoFrame, font=("arial", 12), width=23, textvariable=self.name_tablet, state="readonly")
        combo_tablets["values"] = ("Paracetamol", "Panadol", "Ibuprofen", "Amoxicillin", "Cetrizine", "Dolo 650", "Aspirin", "Azithromycin")
        combo_tablets.current(0)
        combo_tablets.grid(row=0, column=1)

        fields = [
            ("Reference No.", self.ref),
            ("Dose", self.dose),
            ("No Of Tablets", self.no_of_tablets),
            ("Lot", self.lot)
        ]
        for i, (label, var) in enumerate(fields, start=1):
            Label(PatientInfoFrame, text=label, font=("arial", 12, "bold")).grid(row=i, column=0, padx=10, pady=5, sticky=W)
            Entry(PatientInfoFrame, textvariable=var, font=("arial", 12), width=25).grid(row=i, column=1)

        # Further Info Frame
        FurtherInfoFrame = LabelFrame(InfoFrame, text="Further Information", font=("arial", 12, "bold"), bd=5)
        FurtherInfoFrame.place(x=455, y=0, width=450, height=290)

        fields2 = [
            ("Issue Date", self.issue_date),
            ("Exp Date", self.exp_date),
            ("Daily Dose", self.daily_dose),
            ("Storage Advice", self.storage),
            ("NHS Number", self.nhs_number)
        ]
        for i, (label, var) in enumerate(fields2):
            Label(FurtherInfoFrame, text=label, font=("arial", 12, "bold")).grid(row=i, column=0, padx=10, pady=5, sticky=W)
            Entry(FurtherInfoFrame, textvariable=var, font=("arial", 12), width=25).grid(row=i, column=1)

        # Prescription Frame
        PrescriptionFrame = LabelFrame(InfoFrame, text="Prescription", font=("arial", 12, "bold"), bd=5)
        PrescriptionFrame.place(x=910, y=0, width=420, height=290)

        self.txtPrescription = Text(PrescriptionFrame, font=("arial", 12), width=48, height=16)
        self.txtPrescription.pack()

        # Button Frame
        ButtonFrame = Frame(self.root, bd=10, relief=RIDGE)
        ButtonFrame.place(x=0, y=360, width=1350, height=60)

        Button(ButtonFrame, text="Prescription", font=("arial", 12, "bold"), width=15, bg="green", fg="white", command=self.prescription).grid(row=0, column=0, padx=5)
        Button(ButtonFrame, text="Prescription Data", font=("arial", 12, "bold"), width=15, bg="blue", fg="white", command=self.add_data).grid(row=0, column=1, padx=5)
        Button(ButtonFrame, text="Update", font=("arial", 12, "bold"), width=15, bg="orange", fg="white", command=self.update).grid(row=0, column=2, padx=5)
        Button(ButtonFrame, text="Delete", font=("arial", 12, "bold"), width=15, bg="red", fg="white", command=self.delete).grid(row=0, column=3, padx=5)
        Button(ButtonFrame, text="Reset", font=("arial", 12, "bold"), width=15, bg="purple", fg="white", command=self.reset).grid(row=0, column=4, padx=5)
        Button(ButtonFrame, text="Exit", font=("arial", 12, "bold"), width=15, bg="black", fg="white", command=self.exit_app).grid(row=0, column=5, padx=5)

        # Details Table Frame
        DetailsFrame = Frame(self.root, bd=10, relief=RIDGE)
        DetailsFrame.place(x=0, y=420, width=1350, height=250)

        scroll_x = Scrollbar(DetailsFrame, orient=HORIZONTAL)
        scroll_y = Scrollbar(DetailsFrame, orient=VERTICAL)

        self.hospital_table = ttk.Treeview(DetailsFrame,
            columns=("tablet", "ref", "dose", "nooftablets", "lot", "issuedate", "expdate", "dailydose",
                     "storage", "nhsnumber"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.hospital_table.xview)
        scroll_y.config(command=self.hospital_table.yview)

        for col in self.hospital_table["columns"]:
            self.hospital_table.heading(col, text=col.title())
            self.hospital_table.column(col, width=100)

        self.hospital_table["show"] = "headings"
        self.hospital_table.pack(fill=BOTH, expand=1)
        self.hospital_table.bind("<ButtonRelease-1>", self.get_cursor)

    # Button Functionalities
    def prescription(self):
        self.txtPrescription.delete("1.0", END)
        self.txtPrescription.insert(END, f"Tablet: {self.name_tablet.get()}\nRef: {self.ref.get()}\nDose: {self.dose.get()}\n"
                                         f"Tablets: {self.no_of_tablets.get()}\nLot: {self.lot.get()}\nIssue: {self.issue_date.get()}\n"
                                         f"Exp: {self.exp_date.get()}\nDaily Dose: {self.daily_dose.get()}\nStorage: {self.storage.get()}\n"
                                         f"NHS No.: {self.nhs_number.get()}")

    def add_data(self):
        if self.ref.get() == "":
            messagebox.showerror("Error", "Reference Number is required")
            return
        self.hospital_table.insert("", END, values=(
            self.name_tablet.get(), self.ref.get(), self.dose.get(), self.no_of_tablets.get(),
            self.lot.get(), self.issue_date.get(), self.exp_date.get(), self.daily_dose.get(),
            self.storage.get(), self.nhs_number.get()
        ))
        self.reset()

    def get_cursor(self, event):
        row = self.hospital_table.focus()
        content = self.hospital_table.item(row)
        data = content["values"]
        if data:
            self.name_tablet.set(data[0])
            self.ref.set(data[1])
            self.dose.set(data[2])
            self.no_of_tablets.set(data[3])
            self.lot.set(data[4])
            self.issue_date.set(data[5])
            self.exp_date.set(data[6])
            self.daily_dose.set(data[7])
            self.storage.set(data[8])
            self.nhs_number.set(data[9])

    def update(self):
        selected = self.hospital_table.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a record to update.")
            return
        self.hospital_table.item(selected, values=(
            self.name_tablet.get(), self.ref.get(), self.dose.get(), self.no_of_tablets.get(),
            self.lot.get(), self.issue_date.get(), self.exp_date.get(), self.daily_dose.get(),
            self.storage.get(), self.nhs_number.get()
        ))
        self.reset()

    def delete(self):
        selected = self.hospital_table.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a record to delete.")
            return
        self.hospital_table.delete(selected)
        self.reset()

    def reset(self):
        for var in [self.name_tablet, self.ref, self.dose, self.no_of_tablets, self.lot,
                    self.issue_date, self.exp_date, self.daily_dose, self.storage, self.nhs_number]:
            var.set("")
        self.txtPrescription.delete("1.0", END)

    def exit_app(self):
        confirm = messagebox.askyesno("Hospital Management System", "Do you really want to exit?")
        if confirm:
            self.root.destroy()

# Launch App
if __name__ == "__main__":
    root = Tk()
    app = Hospital(root)
    root.mainloop()
