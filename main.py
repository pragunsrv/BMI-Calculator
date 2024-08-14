import tkinter as tk
from tkinter import messagebox, Scrollbar, Listbox, RIGHT, Y, LEFT, BOTH, StringVar, DoubleVar, IntVar, ttk
from tkinter import Canvas
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog
import json

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        
        self.units = {'weight': 'kg', 'height': 'm'}
        self.history_file = 'bmi_history.json'
        self.user_preferences_file = 'user_preferences.json'
        self.bmi_categories = {
            'Underweight': (0, 18.5),
            'Normal weight': (18.5, 24.9),
            'Overweight': (25, 29.9),
            'Obesity': (30, float('inf'))
        }
        self.history = []

        self.load_user_preferences()
        self.create_widgets()
        self.load_history()
        self.load_settings()

    def create_widgets(self):
        self.label_weight = tk.Label(self.root, text="Weight:")
        self.label_weight.grid(row=0, column=0, padx=10, pady=10)

        self.entry_weight = tk.Entry(self.root)
        self.entry_weight.grid(row=0, column=1, padx=10, pady=10)

        self.label_height = tk.Label(self.root, text="Height:")
        self.label_height.grid(row=1, column=0, padx=10, pady=10)

        self.entry_height = tk.Entry(self.root)
        self.entry_height.grid(row=1, column=1, padx=10, pady=10)

        self.unit_frame = tk.Frame(self.root)
        self.unit_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.unit_weight_var = StringVar(value='kg')
        self.unit_height_var = StringVar(value='m')

        self.label_weight_units = tk.Label(self.unit_frame, text="Weight Unit:")
        self.label_weight_units.grid(row=0, column=0, padx=5, pady=5)

        self.weight_units = ttk.Combobox(self.unit_frame, textvariable=self.unit_weight_var, values=['kg', 'lb'])
        self.weight_units.grid(row=0, column=1, padx=5, pady=5)

        self.label_height_units = tk.Label(self.unit_frame, text="Height Unit:")
        self.label_height_units.grid(row=1, column=0, padx=5, pady=5)

        self.height_units = ttk.Combobox(self.unit_frame, textvariable=self.unit_height_var, values=['m', 'ft'])
        self.height_units.grid(row=1, column=1, padx=5, pady=5)

        self.button_calculate = tk.Button(self.root, text="Calculate BMI", command=self.calculate_bmi)
        self.button_calculate.grid(row=3, column=0, columnspan=2, pady=20)

        self.label_result = tk.Label(self.root, text="")
        self.label_result.grid(row=4, column=0, columnspan=2, pady=10)

        self.history_label = tk.Label(self.root, text="Calculation History:")
        self.history_label.grid(row=5, column=0, padx=10, pady=10)

        self.history_listbox = Listbox(self.root, height=10, width=60)
        self.history_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10, rowspan=2)

        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.grid(row=6, column=2, rowspan=2, sticky=Y)

        self.history_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.history_listbox.yview)

        self.button_clear_history = tk.Button(self.root, text="Clear History", command=self.clear_history)
        self.button_clear_history.grid(row=8, column=0, columnspan=2, pady=10)

        self.settings_frame = tk.Frame(self.root)
        self.settings_frame.grid(row=9, column=0, columnspan=2, pady=10)

        self.settings_label = tk.Label(self.settings_frame, text="Settings:")
        self.settings_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.label_bmi_category = tk.Label(self.settings_frame, text="Custom Categories (comma separated):")
        self.label_bmi_category.grid(row=1, column=0, padx=5, pady=5)

        self.entry_bmi_categories = tk.Entry(self.settings_frame, width=50)
        self.entry_bmi_categories.grid(row=1, column=1, padx=5, pady=5)

        self.button_save_settings = tk.Button(self.settings_frame, text="Save Settings", command=self.save_settings)
        self.button_save_settings.grid(row=2, column=0, columnspan=2, pady=10)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.grid(row=10, column=0, columnspan=2, pady=10)

        self.canvas = Canvas(self.canvas_frame, width=400, height=300)
        self.canvas.pack()

        self.plot_button = tk.Button(self.root, text="Plot BMI Distribution", command=self.plot_bmi_distribution)
        self.plot_button.grid(row=11, column=0, columnspan=2, pady=10)

        self.profile_frame = tk.Frame(self.root)
        self.profile_frame.grid(row=12, column=0, columnspan=2, pady=10)

        self.label_profile = tk.Label(self.profile_frame, text="User Profile:")
        self.label_profile.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.label_name = tk.Label(self.profile_frame, text="Name:")
        self.label_name.grid(row=1, column=0, padx=5, pady=5)

        self.entry_name = tk.Entry(self.profile_frame)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5)

        self.label_age = tk.Label(self.profile_frame, text="Age:")
        self.label_age.grid(row=2, column=0, padx=5, pady=5)

        self.entry_age = tk.Entry(self.profile_frame)
        self.entry_age.grid(row=2, column=1, padx=5, pady=5)

        self.label_gender = tk.Label(self.profile_frame, text="Gender:")
        self.label_gender.grid(row=3, column=0, padx=5, pady=5)

        self.gender_var = StringVar(value='Other')
        self.male_rb = tk.Radiobutton(self.profile_frame, text="Male", variable=self.gender_var, value='Male')
        self.male_rb.grid(row=3, column=1, padx=5, pady=5, sticky=LEFT)

        self.female_rb = tk.Radiobutton(self.profile_frame, text="Female", variable=self.gender_var, value='Female')
        self.female_rb.grid(row=3, column=1, padx=65, pady=5, sticky=LEFT)

        self.other_rb = tk.Radiobutton(self.profile_frame, text="Other", variable=self.gender_var, value='Other')
        self.other_rb.grid(row=3, column=1, padx=120, pady=5, sticky=LEFT)

        self.button_save_profile = tk.Button(self.profile_frame, text="Save Profile", command=self.save_profile)
        self.button_save_profile.grid(row=4, column=0, columnspan=2, pady=10)

        self.button_load_profile = tk.Button(self.profile_frame, text="Load Profile", command=self.load_profile)
        self.button_load_profile.grid(row=5, column=0, columnspan=2, pady=10)

        self.dialog_button = tk.Button(self.root, text="Settings Dialog", command=self.open_settings_dialog)
        self.dialog_button.grid(row=13, column=0, columnspan=2, pady=10)

    def calculate_bmi(self):
        weight = self.entry_weight.get()
        height = self.entry_height.get()

        weight_unit = self.unit_weight_var.get()
        height_unit = self.unit_height_var.get()

        if not weight or not height:
            messagebox.showerror("Input Error", "Please enter both weight and height.")
            return

        try:
            weight = float(weight)
            height = float(height)

            if weight_unit == 'lb':
                weight *= 0.453592

            if height_unit == 'ft':
                height *= 0.3048

            if height <= 0:
                raise ValueError("Height must be greater than zero.")

            bmi = weight / (height * height)
            bmi_category = self.get_bmi_category(bmi)

            result_text = f"BMI: {bmi:.2f} ({bmi_category})"
            self.label_result.config(text=result_text)
            self.add_to_history(result_text)
            self.save_to_history(result_text)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")

    def get_bmi_category(self, bmi):
        for category, (lower, upper) in self.bmi_categories.items():
            if lower <= bmi < upper:
                return category
        return "Unknown"

    def add_to_history(self, result_text):
        self.history_listbox.insert(tk.END, result_text)
        self.history.append(result_text)

    def save_to_history(self, result_text):
        with open(self.history_file, 'a') as file:
            file.write(json.dumps({'result': result_text}) + '\n')

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    try:
                        entry = json.loads(line)
                        result_text = entry.get('result', '')
                        self.history_listbox.insert(tk.END, result_text)
                        self.history.append(result_text)
                    except:
                        continue

    def clear_history(self):
        self.history_listbox.delete(0, tk.END)
        self.history = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)

    def save_settings(self):
        categories_text = self.entry_bmi_categories.get()
        categories = categories_text.split(',')

        self.bmi_categories = {}
        for category in categories:
            category = category.strip()
            if category:
                self.bmi_categories[category] = (0, float('inf'))

        self.load_settings()

    def load_settings(self):
        settings_text = ', '.join(self.bmi_categories.keys())
        self.entry_bmi_categories.delete(0, tk.END)
        self.entry_bmi_categories.insert(0, settings_text)

    def plot_bmi_distribution(self):
        if not self.history:
            messagebox.showinfo("Plot Error", "No data available to plot.")
            return

        bmi_values = []
        for entry in self.history:
            try:
                bmi_value = float(entry.split(':')[1].split(' ')[1])
                bmi_values.append(bmi_value)
            except:
                continue

        if not bmi_values:
            messagebox.showinfo("Plot Error", "No valid BMI values found.")
            return

        fig, ax = plt.subplots()
        ax.hist(bmi_values, bins=10, edgecolor='black')
        ax.set_title('BMI Distribution')
        ax.set_xlabel('BMI')
        ax.set_ylabel('Frequency')

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        self.figure_canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def save_profile(self):
        profile = {
            'name': self.entry_name.get(),
            'age': self.entry_age.get(),
            'gender': self.gender_var.get()
        }
        with open(self.user_preferences_file, 'w') as file:
            json.dump(profile, file)

    def load_profile(self):
        if os.path.exists(self.user_preferences_file):
            with open(self.user_preferences_file, 'r') as file:
                profile = json.load(file)
                self.entry_name.delete(0, tk.END)
                self.entry_name.insert(0, profile.get('name', ''))
                self.entry_age.delete(0, tk.END)
                self.entry_age.insert(0, profile.get('age', ''))
                self.gender_var.set(profile.get('gender', 'Other'))

    def open_settings_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Settings Dialog")

        label_dialog = tk.Label(dialog, text="Settings Dialog Placeholder")
        label_dialog.pack(padx=20, pady=20)

        button_close = tk.Button(dialog, text="Close", command=dialog.destroy)
        button_close.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()
