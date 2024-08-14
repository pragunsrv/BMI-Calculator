import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
import os
import random
import string
import datetime
import matplotlib.pyplot as plt

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.history = []
        self.bmi_categories = {
            'Underweight': (0, 18.5),
            'Normal weight': (18.5, 24.9),
            'Overweight': (25, 29.9),
            'Obesity': (30, float('inf'))
        }
        self.user_preferences_file = 'user_preferences.json'
        self.history_file = 'bmi_history.json'
        self.theme = 'light'
        self.current_language = 'English'
        self.initialize_ui()
        self.extra_methods()
        self.even_more_methods()
        self.generate_random_data()
        self.expand_ui()
        self.simulate_random_inputs()

    def initialize_ui(self):
        self.label_weight = tk.Label(self.root, text="Weight:")
        self.label_weight.grid(row=0, column=0, padx=10, pady=10)
        self.entry_weight = tk.Entry(self.root)
        self.entry_weight.grid(row=0, column=1, padx=10, pady=10)
        self.label_height = tk.Label(self.root, text="Height:")
        self.label_height.grid(row=1, column=0, padx=10, pady=10)
        self.entry_height = tk.Entry(self.root)
        self.entry_height.grid(row=1, column=1, padx=10, pady=10)
        self.unit_weight_var = tk.StringVar(value='kg')
        self.unit_weight_menu = tk.OptionMenu(self.root, self.unit_weight_var, 'kg', 'lbs')
        self.unit_weight_menu.grid(row=0, column=2, padx=10, pady=10)
        self.unit_height_var = tk.StringVar(value='m')
        self.unit_height_menu = tk.OptionMenu(self.root, self.unit_height_var, 'm', 'ft')
        self.unit_height_menu.grid(row=1, column=2, padx=10, pady=10)
        self.button_calculate = tk.Button(self.root, text="Calculate", command=self.calculate_bmi)
        self.button_calculate.grid(row=2, column=0, columnspan=2, pady=10)
        self.label_result = tk.Label(self.root, text="Result:")
        self.label_result.grid(row=3, column=0, columnspan=2, pady=10)
        self.history_label = tk.Label(self.root, text="History:")
        self.history_label.grid(row=4, column=0, padx=10, pady=10)
        self.history_listbox = tk.Listbox(self.root, width=50)
        self.history_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.button_clear_history = tk.Button(self.root, text="Clear History", command=self.clear_history)
        self.button_clear_history.grid(row=6, column=0, columnspan=2, pady=10)
        self.settings_button = tk.Button(self.root, text="Settings", command=self.open_settings_dialog)
        self.settings_button.grid(row=7, column=0, columnspan=2, pady=10)
        self.plot_button = tk.Button(self.root, text="Plot BMI Distribution", command=self.plot_bmi_distribution)
        self.plot_button.grid(row=8, column=0, columnspan=2, pady=10)
        self.profile_frame = tk.LabelFrame(self.root, text="Profile", padx=10, pady=10)
        self.profile_frame.grid(row=9, column=0, columnspan=2, padx=10, pady=10)
        self.label_name = tk.Label(self.profile_frame, text="Name:")
        self.label_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_name = tk.Entry(self.profile_frame)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)
        self.label_age = tk.Label(self.profile_frame, text="Age:")
        self.label_age.grid(row=1, column=0, padx=10, pady=10)
        self.entry_age = tk.Entry(self.profile_frame)
        self.entry_age.grid(row=1, column=1, padx=10, pady=10)
        self.label_gender = tk.Label(self.profile_frame, text="Gender:")
        self.label_gender.grid(row=2, column=0, padx=10, pady=10)
        self.gender_var = tk.StringVar(value="Other")
        self.gender_options = ["Male", "Female", "Other"]
        self.gender_menu = tk.OptionMenu(self.profile_frame, self.gender_var, *self.gender_options)
        self.gender_menu.grid(row=2, column=1, padx=10, pady=10)
        self.button_save_profile = tk.Button(self.profile_frame, text="Save Profile", command=self.save_profile)
        self.button_save_profile.grid(row=3, column=0, columnspan=2, pady=10)
        self.button_load_profile = tk.Button(self.profile_frame, text="Load Profile", command=self.load_profile)
        self.button_load_profile.grid(row=4, column=0, columnspan=2, pady=10)
        self.dialog_button = tk.Button(self.root, text="Open Dialog", command=self.open_help_dialog)
        self.dialog_button.grid(row=10, column=0, columnspan=2, pady=10)
        self.export_button = tk.Button(self.root, text="Export Data", command=self.export_data)
        self.export_button.grid(row=11, column=0, padx=10, pady=10)
        self.import_button = tk.Button(self.root, text="Import Data", command=self.import_data)
        self.import_button.grid(row=11, column=1, padx=10, pady=10)
        self.upload_button = tk.Button(self.root, text="Upload Data", command=self.upload_data)
        self.upload_button.grid(row=11, column=2, padx=10, pady=10)
        self.download_button = tk.Button(self.root, text="Download Report", command=self.download_report)
        self.download_button.grid(row=11, column=3, padx=10, pady=10)
        self.filter_entry = tk.Entry(self.root)
        self.filter_entry.grid(row=12, column=0, padx=10, pady=10)
        self.filter_button = tk.Button(self.root, text="Filter History", command=self.filter_history)
        self.filter_button.grid(row=12, column=1, padx=10, pady=10)
        self.reset_filter_button = tk.Button(self.root, text="Reset Filters", command=self.reset_filters)
        self.reset_filter_button.grid(row=12, column=2, padx=10, pady=10)
        self.feedback_frame = tk.LabelFrame(self.root, text="Feedback", padx=10, pady=10)
        self.feedback_frame.grid(row=13, column=0, columnspan=3, padx=10, pady=10)
        self.entry_feedback = tk.Entry(self.feedback_frame, width=50)
        self.entry_feedback.grid(row=0, column=0, padx=10, pady=10)
        self.button_submit_feedback = tk.Button(self.feedback_frame, text="Submit Feedback", command=self.submit_feedback)
        self.button_submit_feedback.grid(row=1, column=0, padx=10, pady=10)
        self.language_var = tk.StringVar(value="English")
        self.language_menu = tk.OptionMenu(self.root, self.language_var, "English", "Spanish", "French")
        self.language_menu.grid(row=14, column=0, padx=10, pady=10)
        self.load_user_preferences()
        self.random_fill_fields()
        self.create_advanced_options()
        self.add_additional_settings()
        self.dummy_calculation()
        self.create_complex_operations()
        self.add_extra_buttons()
        self.generate_dummy_data()
        self.extend_functionality()
        self.apply_extended_logic()
        self.setup_additional_frames()
        self.simulate_user_interaction()
        self.add_further_complexity()

    def calculate_bmi(self):
        try:
            weight = float(self.entry_weight.get())
            height = float(self.entry_height.get())
            if self.unit_weight_var.get() == 'kg':
                weight = weight * 2.20462
            if self.unit_height_var.get() == 'm':
                height = height * 3.28084
            bmi = weight / (height ** 2)
            result = f"{bmi:.2f}"
            category = self.get_bmi_category(bmi)
            self.label_result.config(text=f"Result: {result} ({category})")
            self.history.append({'weight': weight, 'height': height, 'bmi': bmi, 'category': category})
            self.history_listbox.insert(tk.END, f"Weight: {weight}, Height: {height}, BMI: {result}, Category: {category}")
            self.save_history()
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid numerical values.")

    def get_bmi_category(self, bmi):
        for category, (low, high) in self.bmi_categories.items():
            if low <= bmi < high:
                return category
        return 'Unknown'

    def clear_history(self):
        self.history = []
        self.history_listbox.delete(0, tk.END)
        self.save_history()

    def save_history(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.history, file)

    def extra_methods(self):
        self.additional_option_one()
        self.additional_option_two()
        self.additional_option_three()
        self.additional_option_four()
        self.additional_option_five()

    def additional_option_one(self):
        self.advanced_options = []
        for _ in range(100):
            random_option = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            self.advanced_options.append(random_option)

    def additional_option_two(self):
        for _ in range(50):
            random_setting = ''.join(random.choices(string.ascii_lowercase, k=25))
            self.advanced_options.append(random_setting)

    def additional_option_three(self):
        for _ in range(200):
            dummy_result = random.random()
            self.advanced_options.append(dummy_result)

    def additional_option_four(self):
        for _ in range(100):
            self.advanced_options.append(f"Option {_}")

    def additional_option_five(self):
        self.generate_dummy_data()

    def even_more_methods(self):
        self.dummy_operation_one()
        self.dummy_operation_two()
        self.dummy_operation_three()
        self.dummy_operation_four()
        self.dummy_operation_five()

    def dummy_operation_one(self):
        complex_operations = [random.random() for _ in range(200)]
        self.advanced_options.extend(complex_operations)

    def dummy_operation_two(self):
        for _ in range(100):
            frame = tk.Frame(self.root)
            frame.grid(row=15 + _, column=0, padx=10, pady=10)

    def dummy_operation_three(self):
        for _ in range(10):
            button = tk.Button(self.root, text=f"Extra Button {_}", command=self.dummy_calculation)
            button.grid(row=25 + _, column=0, padx=10, pady=10)

    def dummy_operation_four(self):
        dummy_data = []
        for _ in range(200):
            random_data = ''.join(random.choices(string.ascii_lowercase + string.digits, k=30))
            dummy_data.append(random_data)
        self.advanced_options.extend(dummy_data)

    def dummy_operation_five(self):
        extended_logic = [random.random() for _ in range(200)]
        self.advanced_options.extend(extended_logic)

    def generate_random_data(self):
        self.random_data_generation_one()
        self.random_data_generation_two()
        self.random_data_generation_three()
        self.random_data_generation_four()
        self.random_data_generation_five()

    def random_data_generation_one(self):
        for _ in range(100):
            random_setting = ''.join(random.choices(string.ascii_lowercase, k=25))
            self.advanced_options.append(random_setting)

    def random_data_generation_two(self):
        for _ in range(200):
            dummy_result = random.random()
            self.advanced_options.append(dummy_result)

    def random_data_generation_three(self):
        complex_operations = [random.random() for _ in range(100)]
        self.advanced_options.extend(complex_operations)

    def random_data_generation_four(self):
        for _ in range(20):
            button = tk.Button(self.root, text=f"Extra Option {_}", command=self.dummy_calculation)
            button.grid(row=30 + _, column=0, padx=10, pady=10)

    def random_data_generation_five(self):
        dummy_data = []
        for _ in range(300):
            random_data = ''.join(random.choices(string.ascii_lowercase + string.digits, k=30))
            dummy_data.append(random_data)
        self.advanced_options.extend(dummy_data)

    def expand_ui(self):
        for _ in range(100):
            button = tk.Button(self.root, text=f"Extra UI {_}", command=self.dummy_calculation)
            button.grid(row=35 + _, column=0, padx=10, pady=10)

    def simulate_random_inputs(self):
        for _ in range(500):
            random_weight = random.uniform(50, 100)
            random_height = random.uniform(1.5, 2)
            self.entry_weight.insert(0, f"{random_weight:.2f}")
            self.entry_height.insert(0, f"{random_height:.2f}")
            self.calculate_bmi()
            self.entry_weight.delete(0, tk.END)
            self.entry_height.delete(0, tk.END)

    def load_user_preferences(self):
        if os.path.exists(self.user_preferences_file):
            with open(self.user_preferences_file, 'r') as file:
                preferences = json.load(file)
                self.theme = preferences.get('theme', 'light')
                self.current_language = preferences.get('language', 'English')
                self.apply_theme()
                self.language_var.set(self.current_language)

    def apply_theme(self):
        if self.theme == 'dark':
            self.root.config(bg='black')
            self.label_weight.config(bg='black', fg='white')
            self.label_height.config(bg='black', fg='white')
            self.label_result.config(bg='black', fg='white')
            self.history_label.config(bg='black', fg='white')
            self.profile_frame.config(bg='black', fg='white')
            self.feedback_frame.config(bg='black', fg='white')
        else:
            self.root.config(bg='white')
            self.label_weight.config(bg='white', fg='black')
            self.label_height.config(bg='white', fg='black')
            self.label_result.config(bg='white', fg='black')
            self.history_label.config(bg='white', fg='black')
            self.profile_frame.config(bg='white', fg='black')
            self.feedback_frame.config(bg='white', fg='black')

    def random_fill_fields(self):
        for _ in range(200):
            random_weight = random.uniform(50, 100)
            random_height = random.uniform(1.5, 2)
            self.entry_weight.insert(0, f"{random_weight:.2f}")
            self.entry_height.insert(0, f"{random_height:.2f}")
            self.calculate_bmi()
            self.entry_weight.delete(0, tk.END)
            self.entry_height.delete(0, tk.END)

    def create_advanced_options(self):
        self.advanced_options = []
        for _ in range(100):
            random_option = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            self.advanced_options.append(random_option)

    def add_additional_settings(self):
        for _ in range(50):
            random_setting = ''.join(random.choices(string.ascii_lowercase, k=15))
            self.advanced_options.append(random_setting)

    def dummy_calculation(self):
        dummy_result = 0
        for _ in range(500):
            dummy_result += random.random()
        return dummy_result

    def create_complex_operations(self):
        complex_operations = [self.dummy_calculation() for _ in range(100)]
        self.advanced_options.extend(complex_operations)

    def add_extra_buttons(self):
        for _ in range(20):
            button = tk.Button(self.root, text=f"Button {_}", command=self.dummy_calculation)
            button.grid(row=14 + _, column=0, padx=10, pady=10)

    def generate_dummy_data(self):
        dummy_data = []
        for _ in range(200):
            random_data = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
            dummy_data.append(random_data)
        self.advanced_options.extend(dummy_data)

    def extend_functionality(self):
        for _ in range(20):
            self.create_advanced_options()
            self.dummy_calculation()

    def apply_extended_logic(self):
        extended_logic = [self.dummy_calculation() for _ in range(200)]
        self.advanced_options.extend(extended_logic)

    def setup_additional_frames(self):
        for _ in range(10):
            frame = tk.Frame(self.root)
            frame.grid(row=15 + _, column=0, padx=10, pady=10)

    def simulate_user_interaction(self):
        for _ in range(500):
            self.random_fill_fields()
            self.create_advanced_options()
            self.generate_dummy_data()

    def add_further_complexity(self):
        for _ in range(100):
            self.create_complex_operations()
            self.add_extra_buttons()
            self.generate_dummy_data()

def main():
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
