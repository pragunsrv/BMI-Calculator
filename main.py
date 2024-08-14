import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from tkinter import StringVar, BooleanVar
import json
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import random

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.history_file = 'bmi_history.json'
        self.user_preferences_file = 'user_preferences.json'
        self.theme = 'light'
        self.current_language = 'English'
        self.translation_dict = {
            'English': {
                'weight': 'Weight',
                'height': 'Height',
                'weight_unit': 'Unit (lb/kg)',
                'height_unit': 'Unit (ft/m)',
                'calculate': 'Calculate BMI',
                'result': 'Your BMI is',
                'history': 'History',
                'clear_history': 'Clear History',
                'settings': 'Settings',
                'plot': 'Plot BMI Distribution',
                'name': 'Name',
                'age': 'Age',
                'gender': 'Gender',
                'save_profile': 'Save Profile',
                'load_profile': 'Load Profile',
                'settings_dialog': 'Settings Dialog',
                'export_data': 'Export Data',
                'submit_feedback': 'Submit Feedback',
                'toggle_theme': 'Toggle Theme',
                'help': 'Help',
                'import_data': 'Import Data',
                'upload_data': 'Upload Data',
                'download_report': 'Download Report',
                'filter_history': 'Filter History',
                'reset_filters': 'Reset Filters',
                'user_profile': 'User Profile',
                'error': 'Error',
                'success': 'Success',
                'warning': 'Warning'
            }
        }
        self.bmi_categories = {
            'Underweight': (0, 18.5),
            'Normal weight': (18.5, 24.9),
            'Overweight': (25, 29.9),
            'Obesity': (30, float('inf'))
        }
        self.history = []
        self.init_ui()

    def init_ui(self):
        self.label_weight = tk.Label(self.root, text=self.translation_dict[self.current_language]['weight'])
        self.label_weight.grid(row=0, column=0, padx=10, pady=10)

        self.entry_weight = tk.Entry(self.root)
        self.entry_weight.grid(row=0, column=1, padx=10, pady=10)

        self.label_weight_units = tk.Label(self.root, text='lb')
        self.label_weight_units.grid(row=0, column=2, padx=10, pady=10)

        self.unit_weight_var = StringVar(value='lb')
        self.unit_weight_lb = tk.Radiobutton(self.root, text='lb', variable=self.unit_weight_var, value='lb')
        self.unit_weight_lb.grid(row=1, column=1, padx=10, pady=10)

        self.unit_weight_kg = tk.Radiobutton(self.root, text='kg', variable=self.unit_weight_var, value='kg')
        self.unit_weight_kg.grid(row=1, column=1, padx=10, pady=10, sticky='E')

        self.label_height = tk.Label(self.root, text=self.translation_dict[self.current_language]['height'])
        self.label_height.grid(row=2, column=0, padx=10, pady=10)

        self.entry_height = tk.Entry(self.root)
        self.entry_height.grid(row=2, column=1, padx=10, pady=10)

        self.label_height_units = tk.Label(self.root, text='ft')
        self.label_height_units.grid(row=2, column=2, padx=10, pady=10)

        self.unit_height_var = StringVar(value='ft')
        self.unit_height_ft = tk.Radiobutton(self.root, text='ft', variable=self.unit_height_var, value='ft')
        self.unit_height_ft.grid(row=3, column=1, padx=10, pady=10)

        self.unit_height_m = tk.Radiobutton(self.root, text='m', variable=self.unit_height_var, value='m')
        self.unit_height_m.grid(row=3, column=1, padx=10, pady=10, sticky='E')

        self.button_calculate = tk.Button(self.root, text=self.translation_dict[self.current_language]['calculate'], command=self.calculate_bmi)
        self.button_calculate.grid(row=4, column=0, columnspan=3, pady=10)

        self.label_result = tk.Label(self.root, text='')
        self.label_result.grid(row=5, column=0, columnspan=3, pady=10)

        self.history_label = tk.Label(self.root, text=self.translation_dict[self.current_language]['history'])
        self.history_label.grid(row=6, column=0, padx=10, pady=10)

        self.history_listbox = tk.Listbox(self.root)
        self.history_listbox.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

        self.button_clear_history = tk.Button(self.root, text=self.translation_dict[self.current_language]['clear_history'], command=self.clear_history)
        self.button_clear_history.grid(row=8, column=0, columnspan=3, pady=10)

        self.settings_label = tk.Label(self.root, text=self.translation_dict[self.current_language]['settings'])
        self.settings_label.grid(row=9, column=0, padx=10, pady=10)

        self.entry_bmi_categories = tk.Entry(self.root)
        self.entry_bmi_categories.grid(row=10, column=0, padx=10, pady=10)

        self.button_save_settings = tk.Button(self.root, text=self.translation_dict[self.current_language]['save_settings'], command=self.save_settings)
        self.button_save_settings.grid(row=10, column=1, padx=10, pady=10)

        self.plot_button = tk.Button(self.root, text=self.translation_dict[self.current_language]['plot'], command=self.plot_bmi_distribution)
        self.plot_button.grid(row=11, column=0, columnspan=2, pady=10)

        self.profile_frame = tk.Frame(self.root)
        self.profile_frame.grid(row=12, column=0, columnspan=2, pady=10)

        self.label_name = tk.Label(self.profile_frame, text=self.translation_dict[self.current_language]['name'])
        self.label_name.grid(row=0, column=0, padx=5, pady=5)

        self.entry_name = tk.Entry(self.profile_frame)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        self.label_age = tk.Label(self.profile_frame, text=self.translation_dict[self.current_language]['age'])
        self.label_age.grid(row=1, column=0, padx=5, pady=5)

        self.entry_age = tk.Entry(self.profile_frame)
        self.entry_age.grid(row=1, column=1, padx=5, pady=5)

        self.label_gender = tk.Label(self.profile_frame, text=self.translation_dict[self.current_language]['gender'])
        self.label_gender.grid(row=2, column=0, padx=5, pady=5)

        self.gender_var = StringVar(value='Other')
        self.gender_male = tk.Radiobutton(self.profile_frame, text='Male', variable=self.gender_var, value='Male')
        self.gender_male.grid(row=2, column=1, padx=5, pady=5, sticky='W')

        self.gender_female = tk.Radiobutton(self.profile_frame, text='Female', variable=self.gender_var, value='Female')
        self.gender_female.grid(row=2, column=1, padx=5, pady=5, sticky='E')

        self.gender_other = tk.Radiobutton(self.profile_frame, text='Other', variable=self.gender_var, value='Other')
        self.gender_other.grid(row=2, column=1, padx=5, pady=5)

        self.button_save_profile = tk.Button(self.root, text=self.translation_dict[self.current_language]['save_profile'], command=self.save_profile)
        self.button_save_profile.grid(row=13, column=0, padx=10, pady=10)

        self.button_load_profile = tk.Button(self.root, text=self.translation_dict[self.current_language]['load_profile'], command=self.load_profile)
        self.button_load_profile.grid(row=13, column=1, padx=10, pady=10)

        self.dialog_button = tk.Button(self.root, text=self.translation_dict[self.current_language]['settings_dialog'], command=self.open_settings_dialog)
        self.dialog_button.grid(row=14, column=0, columnspan=2, pady=10)

        self.export_button = tk.Button(self.root, text=self.translation_dict[self.current_language]['export_data'], command=self.export_data)
        self.export_button.grid(row=15, column=0, padx=10, pady=10)

        self.entry_feedback = tk.Entry(self.root)
        self.entry_feedback.grid(row=16, column=0, padx=10, pady=10)

        self.button_submit_feedback = tk.Button(self.root, text=self.translation_dict[self.current_language]['submit_feedback'], command=self.submit_feedback)
        self.button_submit_feedback.grid(row=16, column=1, padx=10, pady=10)

        self.theme_button = tk.Button(self.root, text=self.translation_dict[self.current_language]['toggle_theme'], command=self.toggle_theme)
        self.theme_button.grid(row=17, column=0, columnspan=2, pady=10)

        self.help_button = tk.Button(self.root, text=self.translation_dict[self.current_language]['help'], command=self.open_help_dialog)
        self.help_button.grid(row=18, column=0, columnspan=2, pady=10)

        self.import_button = tk.Button(self.root, text=self.translation_dict[self.current_language]['import_data'], command=self.import_data)
        self.import_button.grid(row=19, column=0, padx=10, pady=10)

        self.upload_button = tk.Button(self.root, text=self.translation_dict[self.current_language]['upload_data'], command=self.upload_data)
        self.upload_button.grid(row=19, column=1, padx=10, pady=10)

        self.download_button = tk.Button(self.root, text=self.translation_dict[self.current_language]['download_report'], command=self.download_report)
        self.download_button.grid(row=19, column=2, padx=10, pady=10)

        self.filter_entry = tk.Entry(self.root)
        self.filter_entry.grid(row=20, column=0, padx=10, pady=10)

        self.filter_button = tk.Button(self.root, text=self.translation_dict[self.current_language]['filter_history'], command=self.filter_history)
        self.filter_button.grid(row=20, column=1, padx=10, pady=10)

        self.reset_filter_button = tk.Button(self.root, text=self.translation_dict[self.current_language]['reset_filters'], command=self.reset_filters)
        self.reset_filter_button.grid(row=20, column=2, padx=10, pady=10)

        self.load_user_preferences()

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
            self.label_result.config(text=f"{self.translation_dict[self.current_language]['result']} {result} ({category})")
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

    def save_settings(self):
        with open(self.user_preferences_file, 'w') as file:
            preferences = {
                'theme': self.theme,
                'language': self.current_language
            }
            json.dump(preferences, file)

    def plot_bmi_distribution(self):
        bmi_values = [entry['bmi'] for entry in self.history]
        if bmi_values:
            fig = Figure(figsize=(8, 6), dpi=100)
            plot = fig.add_subplot(111)
            plot.hist(bmi_values, bins=15, color='green', edgecolor='black')
            plot.set_title('BMI Distribution')
            plot.set_xlabel('BMI')
            plot.set_ylabel('Frequency')
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().grid(row=21, column=0, columnspan=3)
        else:
            messagebox.showinfo("No Data", "No BMI history available for plotting.")

    def save_profile(self):
        profile = {
            'name': self.entry_name.get(),
            'age': self.entry_age.get(),
            'gender': self.gender_var.get()
        }
        with open('user_profile.json', 'w') as file:
            json.dump(profile, file)

    def load_profile(self):
        if os.path.exists('user_profile.json'):
            with open('user_profile.json', 'r') as file:
                profile = json.load(file)
                self.entry_name.delete(0, tk.END)
                self.entry_name.insert(0, profile.get('name', ''))
                self.entry_age.delete(0, tk.END)
                self.entry_age.insert(0, profile.get('age', ''))
                self.gender_var.set(profile.get('gender', 'Other'))
    def update_history_listbox_(self):
        self.history_listbox.delete(0, tk.END)
        for entry in self.history:
            self.history_listbox.insert(tk.END, f"Weight: {entry['weight']}, Height: {entry['height']}, BMI: {entry['bmi']:.2f}, Category: {entry['category']}")

    def upload_data_(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.history, file)

    def download_rep_ort(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write("BMI Report")

    def filter_histor_y(self):
        filter_text = self.filter_entry.get()
        filtered_history = [entry for entry in self.history if filter_text.lower() in str(entry).lower()]
        self.history_listbox.delete(0, tk.END)
        for entry in filtered_history:
            self.history_listbox.insert(tk.END, f"Weight: {entry['weight']}, Height: {entry['height']}, BMI: {entry['bmi']:.2f}, Category: {entry['category']}")

    def reset_filters_(self):
        self.filter_entry.delete(0, tk.END)
        self.update_history_listbox()
    def open_settings_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.translation_dict[self.current_language]['settings_dialog'])
        tk.Label(dialog, text=self.translation_dict[self.current_language]['bmi_categories']).pack(pady=10)
        categories_entry = tk.Entry(dialog)
        categories_entry.pack(padx=10, pady=10)
        categories_entry.insert(0, ', '.join(self.bmi_categories.keys()))

        def save_and_close():
            categories_text = categories_entry.get()
            categories = categories_text.split(',')
            self.bmi_categories = {}
            for category in categories:
                category = category.strip()
                if category:
                    self.bmi_categories[category] = (0, float('inf'))
            self.save_settings()
            dialog.destroy()

        tk.Button(dialog, text=self.translation_dict[self.current_language]['save_settings'], command=save_and_close).pack(pady=10)

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.history, file)

    def submit_feedback(self):
        feedback = self.entry_feedback.get()
        if feedback:
            messagebox.showinfo(self.translation_dict[self.current_language]['feedback'], "Feedback submitted.")
        else:
            messagebox.showwarning(self.translation_dict[self.current_language]['feedback'], "Please enter feedback.")

    def toggle_theme(self):
        if self.theme == 'light':
            self.theme = 'dark'
        else:
            self.theme = 'light'
        self.apply_theme()

    def apply_theme(self):
        if self.theme == 'dark':
            self.root.config(bg='black')
            self.label_weight.config(bg='black', fg='white')
            self.label_height.config(bg='black', fg='white')
            self.button_calculate.config(bg='gray', fg='black')
            self.label_result.config(bg='black', fg='white')
            self.history_label.config(bg='black', fg='white')
            self.button_clear_history.config(bg='gray', fg='black')
            self.settings_label.config(bg='black', fg='white')
            self.button_save_settings.config(bg='gray', fg='black')
            self.plot_button.config(bg='gray', fg='black')
            self.profile_frame.config(bg='black')
            self.button_save_profile.config(bg='gray', fg='black')
            self.button_load_profile.config(bg='gray', fg='black')
            self.dialog_button.config(bg='gray', fg='black')
            self.export_button.config(bg='gray', fg='black')
            self.entry_feedback.config(bg='gray', fg='black')
            self.button_submit_feedback.config(bg='gray', fg='black')
            self.theme_button.config(bg='gray', fg='black')
            self.help_button.config(bg='gray', fg='black')
            self.import_button.config(bg='gray', fg='black')
            self.language_menu.config(bg='gray', fg='black')
            self.upload_button.config(bg='gray', fg='black')
            self.download_button.config(bg='gray', fg='black')
            self.filter_button.config(bg='gray', fg='black')
            self.reset_filter_button.config(bg='gray', fg='black')
        else:
            self.root.config(bg='white')
            self.label_weight.config(bg='white', fg='black')
            self.label_height.config(bg='white', fg='black')
            self.button_calculate.config(bg='lightgray', fg='black')
            self.label_result.config(bg='white', fg='black')
            self.history_label.config(bg='white', fg='black')
            self.button_clear_history.config(bg='lightgray', fg='black')
            self.settings_label.config(bg='white', fg='black')
            self.button_save_settings.config(bg='lightgray', fg='black')
            self.plot_button.config(bg='lightgray', fg='black')
            self.profile_frame.config(bg='white')
            self.button_save_profile.config(bg='lightgray', fg='black')
            self.button_load_profile.config(bg='lightgray', fg='black')
            self.dialog_button.config(bg='lightgray', fg='black')
            self.export_button.config(bg='lightgray', fg='black')
            self.entry_feedback.config(bg='white', fg='black')
            self.button_submit_feedback.config(bg='lightgray', fg='black')
            self.theme_button.config(bg='lightgray', fg='black')
            self.help_button.config(bg='lightgray', fg='black')
            self.import_button.config(bg='lightgray', fg='black')
            self.language_menu.config(bg='white', fg='black')
            self.upload_button.config(bg='lightgray', fg='black')
            self.download_button.config(bg='lightgray', fg='black')
            self.filter_button.config(bg='lightgray', fg='black')
            self.reset_filter_button.config(bg='lightgray', fg='black')

    def open_help_dialog_(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.translation_dict[self.current_language]['help'])
        tk.Label(dialog, text="Help content goes here.").pack(padx=10, pady=10)
        tk.Button(dialog, text='Close', command=dialog.destroy).pack(pady=10)
    def get_bmi_category_(self, bmi):
        for category, (low, high) in self.bmi_categories.items():
            if low <= bmi < high:
                return category
        return 'Unknown'

    def clear_history_(self):
        self.history = []
        self.history_listbox.delete(0, tk.END)
        self.save_history()

    def save_history_(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.history, file)

    def save_settings_(self):
        with open(self.user_preferences_file, 'w') as file:
            preferences = {
                'theme': self.theme,
                'language': self.current_language
            }
            json.dump(preferences, file)

    def plot_bmi_distribution_(self):
        bmi_values = [entry['bmi'] for entry in self.history]
        if bmi_values:
            fig = Figure(figsize=(8, 6), dpi=100)
            plot = fig.add_subplot(111)
            plot.hist(bmi_values, bins=15, color='green', edgecolor='black')
            plot.set_title('BMI Distribution')
            plot.set_xlabel('BMI')
            plot.set_ylabel('Frequency')
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().grid(row=21, column=0, columnspan=3)
        else:
            messagebox.showinfo("No Data", "No BMI history available for plotting.")

    def save_profile_(self):
        profile = {
            'name': self.entry_name.get(),
            'age': self.entry_age.get(),
            'gender': self.gender_var.get()
        }
        with open('user_profile.json', 'w') as file:
            json.dump(profile, file)

    def load_profile_(self):
        if os.path.exists('user_profile.json'):
            with open('user_profile.json', 'r') as file:
                profile = json.load(file)
                self.entry_name.delete(0, tk.END)
                self.entry_name.insert(0, profile.get('name', ''))
                self.entry_age.delete(0, tk.END)
                self.entry_age.insert(0, profile.get('age', ''))
                self.gender_var.set(profile.get('gender', 'Other'))

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.history.extend(data)
                self.update_history_listbox()

    def update_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        for entry in self.history:
            self.history_listbox.insert(tk.END, f"Weight: {entry['weight']}, Height: {entry['height']}, BMI: {entry['bmi']:.2f}, Category: {entry['category']}")

    def upload_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.history, file)

    def download_report(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write("BMI Report")

    def filter_history(self):
        filter_text = self.filter_entry.get()
        filtered_history = [entry for entry in self.history if filter_text.lower() in str(entry).lower()]
        self.history_listbox.delete(0, tk.END)
        for entry in filtered_history:
            self.history_listbox.insert(tk.END, f"Weight: {entry['weight']}, Height: {entry['height']}, BMI: {entry['bmi']:.2f}, Category: {entry['category']}")

    def reset_filters(self):
        self.filter_entry.delete(0, tk.END)
        self.update_history_listbox()

    def load_user_preferences(self):
        if os.path.exists(self.user_preferences_file):
            with open(self.user_preferences_file, 'r') as file:
                preferences = json.load(file)
                self.theme = preferences.get('theme', 'light')
                self.current_language = preferences.get('language', 'English')
                self.apply_theme()
                self.language_var.set(self.current_language)

def main():
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
