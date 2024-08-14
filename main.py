import tkinter as tk
from tkinter import messagebox, Scrollbar, Listbox, RIGHT, Y, LEFT, BOTH, StringVar, DoubleVar, IntVar, ttk
from tkinter import Canvas, filedialog, simpledialog
import os
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import locale

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
        self.theme = 'light'
        self.languages = ['English', 'Spanish', 'French', 'German']
        self.current_language = 'English'
        self.translation_dict = {
            'English': {
                'weight': 'Weight:',
                'height': 'Height:',
                'weight_unit': 'Weight Unit:',
                'height_unit': 'Height Unit:',
                'calculate': 'Calculate BMI',
                'result': 'BMI: ',
                'history': 'Calculation History:',
                'clear_history': 'Clear History',
                'settings': 'Settings:',
                'bmi_categories': 'Custom Categories (comma separated):',
                'save_settings': 'Save Settings',
                'plot': 'Plot BMI Distribution',
                'profile': 'User Profile:',
                'name': 'Name:',
                'age': 'Age:',
                'gender': 'Gender:',
                'save_profile': 'Save Profile',
                'load_profile': 'Load Profile',
                'settings_dialog': 'Settings Dialog',
                'export_data': 'Export Data',
                'feedback': 'Feedback:',
                'submit_feedback': 'Submit Feedback',
                'toggle_theme': 'Toggle Theme',
                'help': 'Help',
                'import_data': 'Import Data',
                'language': 'Language:'
            },
            'Spanish': {
                'weight': 'Peso:',
                'height': 'Altura:',
                'weight_unit': 'Unidad de Peso:',
                'height_unit': 'Unidad de Altura:',
                'calculate': 'Calcular IMC',
                'result': 'IMC: ',
                'history': 'Historial de Cálculos:',
                'clear_history': 'Borrar Historial',
                'settings': 'Configuraciones:',
                'bmi_categories': 'Categorías Personalizadas (separadas por comas):',
                'save_settings': 'Guardar Configuraciones',
                'plot': 'Graficar Distribución de IMC',
                'profile': 'Perfil del Usuario:',
                'name': 'Nombre:',
                'age': 'Edad:',
                'gender': 'Género:',
                'save_profile': 'Guardar Perfil',
                'load_profile': 'Cargar Perfil',
                'settings_dialog': 'Diálogo de Configuraciones',
                'export_data': 'Exportar Datos',
                'feedback': 'Comentarios:',
                'submit_feedback': 'Enviar Comentarios',
                'toggle_theme': 'Cambiar Tema',
                'help': 'Ayuda',
                'import_data': 'Importar Datos',
                'language': 'Idioma:'
            },
            'French': {
                'weight': 'Poids:',
                'height': 'Hauteur:',
                'weight_unit': 'Unité de Poids:',
                'height_unit': 'Unité de Hauteur:',
                'calculate': 'Calculer l\'IMC',
                'result': 'IMC: ',
                'history': 'Historique des Calculs:',
                'clear_history': 'Effacer l\'Historique',
                'settings': 'Paramètres:',
                'bmi_categories': 'Catégories Personnalisées (séparées par des virgules):',
                'save_settings': 'Enregistrer les Paramètres',
                'plot': 'Tracer la Distribution de l\'IMC',
                'profile': 'Profil Utilisateur:',
                'name': 'Nom:',
                'age': 'Âge:',
                'gender': 'Genre:',
                'save_profile': 'Enregistrer le Profil',
                'load_profile': 'Charger le Profil',
                'settings_dialog': 'Dialogue des Paramètres',
                'export_data': 'Exporter les Données',
                'feedback': 'Commentaires:',
                'submit_feedback': 'Soumettre les Commentaires',
                'toggle_theme': 'Changer le Thème',
                'help': 'Aide',
                'import_data': 'Importer les Données',
                'language': 'Langue:'
            },
            'German': {
                'weight': 'Gewicht:',
                'height': 'Größe:',
                'weight_unit': 'Gewichtseinheit:',
                'height_unit': 'Größeneinheit:',
                'calculate': 'BMI Berechnen',
                'result': 'BMI: ',
                'history': 'Berechnungshistorie:',
                'clear_history': 'Historie Löschen',
                'settings': 'Einstellungen:',
                'bmi_categories': 'Benutzerdefinierte Kategorien (durch Kommas getrennt):',
                'save_settings': 'Einstellungen Speichern',
                'plot': 'BMI-Verteilung Diagramm',
                'profile': 'Benutzerprofil:',
                'name': 'Name:',
                'age': 'Alter:',
                'gender': 'Geschlecht:',
                'save_profile': 'Profil Speichern',
                'load_profile': 'Profil Laden',
                'settings_dialog': 'Einstellungsdialog',
                'export_data': 'Daten Exportieren',
                'feedback': 'Rückmeldung:',
                'submit_feedback': 'Feedback Einreichen',
                'toggle_theme': 'Thema Umschalten',
                'help': 'Hilfe',
                'import_data': 'Daten Importieren',
                'language': 'Sprache:'
            }
        }
        
        self.load_user_preferences()
        self.create_widgets()
        self.load_history()
        self.load_settings()
        self.apply_theme()
        self.update_language()

    def create_widgets(self):
        self.label_weight = tk.Label(self.root, text=self.translation_dict[self.current_language]['weight'])
        self.label_weight.grid(row=0, column=0, padx=10, pady=10)

        self.entry_weight = tk.Entry(self.root)
        self.entry_weight.grid(row=0, column=1, padx=10, pady=10)

        self.label_height = tk.Label(self.root, text=self.translation_dict[self.current_language]['height'])
        self.label_height.grid(row=1, column=0, padx=10, pady=10)

        self.entry_height = tk.Entry(self.root)
        self.entry_height.grid(row=1, column=1, padx=10, pady=10)

        self.unit_frame = tk.Frame(self.root)
        self.unit_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.unit_weight_var = StringVar(value='kg')
        self.unit_height_var = StringVar(value='m')

        self.label_weight_units = tk.Label(self.unit_frame, text=self.translation_dict[self.current_language]['weight_unit'])
        self.label_weight_units.grid(row=0, column=0, padx=5, pady=5)

        self.weight_units = ttk.Combobox(self.unit_frame, textvariable=self.unit_weight_var, values=['kg', 'lb'])
        self.weight_units.grid(row=0, column=1, padx=5, pady=5)

        self.label_height_units = tk.Label(self.unit_frame, text=self.translation_dict[self.current_language]['height_unit'])
        self.label_height_units.grid(row=1, column=0, padx=5, pady=5)

        self.height_units = ttk.Combobox(self.unit_frame, textvariable=self.unit_height_var, values=['m', 'ft'])
        self.height_units.grid(row=1, column=1, padx=5, pady=5)

        self.button_calculate = tk.Button(self.root, text=self.translation_dict[self.current_language]['calculate'], command=self.calculate_bmi)
        self.button_calculate.grid(row=3, column=0, columnspan=2, pady=20)

        self.label_result = tk.Label(self.root, text="")
        self.label_result.grid(row=4, column=0, columnspan=2, pady=10)

        self.history_label = tk.Label(self.root, text=self.translation_dict[self.current_language]['history'])
        self.history_label.grid(row=5, column=0, padx=10, pady=10)

        self.history_listbox = Listbox(self.root, height=10, width=60)
        self.history_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10, rowspan=2)

        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.grid(row=6, column=2, rowspan=2, sticky=Y)

        self.history_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.history_listbox.yview)

        self.button_clear_history = tk.Button(self.root, text=self.translation_dict[self.current_language]['clear_history'], command=self.clear_history)
        self.button_clear_history.grid(row=8, column=0, columnspan=2, pady=10)

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
        self.theme_button.grid(row=17, column=0, padx=10, pady=10)

        self.help_button = tk.Button(self.root, text=self.translation_dict[self.current_language]['help'], command=self.open_help_dialog)
        self.help_button.grid(row=17, column=1, padx=10, pady=10)

        self.import_button = tk.Button(self.root, text=self.translation_dict[self.current_language]['import_data'], command=self.import_data)
        self.import_button.grid(row=18, column=0, columnspan=2, pady=10)

        self.language_var = StringVar(value=self.current_language)
        self.language_menu = ttk.Combobox(self.root, textvariable=self.language_var, values=self.languages, state='readonly')
        self.language_menu.grid(row=19, column=0, padx=10, pady=10)
        self.language_menu.bind('<<ComboboxSelected>>', self.change_language)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.grid(row=20, column=0, columnspan=2, pady=10)

        self.figure_canvas = None

    def calculate_bmi(self):
        weight = self.entry_weight.get()
        height = self.entry_height.get()
        weight_unit = self.unit_weight_var.get()
        height_unit = self.unit_height_var.get()

        if not weight or not height:
            messagebox.showerror(self.translation_dict[self.current_language]['weight'], "Please enter both weight and height.")
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

            result_text = f"{self.translation_dict[self.current_language]['result']} {bmi:.2f} ({bmi_category})"
            self.label_result.config(text=result_text)
            self.add_to_history(result_text)
            self.save_to_history(result_text)
        except ValueError:
            messagebox.showerror(self.translation_dict[self.current_language]['weight'], "Please enter valid numbers.")

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
            messagebox.showinfo(self.translation_dict[self.current_language]['plot'], "No data available to plot.")
            return

        bmi_values = []
        for entry in self.history:
            try:
                bmi_value = float(entry.split(':')[1].split(' ')[1])
                bmi_values.append(bmi_value)
            except:
                continue

        if not bmi_values:
            messagebox.showinfo(self.translation_dict[self.current_language]['plot'], "No valid BMI values found.")
            return

        fig = Figure()
        ax = fig.add_subplot(111)
        ax.hist(bmi_values, bins=10, edgecolor='black')
        ax.set_title(self.translation_dict[self.current_language]['plot'])
        ax.set_xlabel('BMI')
        ax.set_ylabel('Frequency')

        if self.figure_canvas:
            self.figure_canvas.get_tk_widget().destroy()

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

    def open_help_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.translation_dict[self.current_language]['help'])
        tk.Label(dialog, text="Help information goes here.").pack(pady=10)

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.history.extend(data)
                self.history_listbox.delete(0, tk.END)
                for entry in data:
                    self.history_listbox.insert(tk.END, entry)

    def change_language(self, event):
        self.current_language = self.language_var.get()
        self.update_language()

    def update_language(self):
        if self.current_language in self.translation_dict:
            self.label_weight.config(text=self.translation_dict[self.current_language]['weight'])
            self.label_height.config(text=self.translation_dict[self.current_language]['height'])
            self.label_weight_units.config(text=self.translation_dict[self.current_language]['weight_unit'])
            self.label_height_units.config(text=self.translation_dict[self.current_language]['height_unit'])
            self.button_calculate.config(text=self.translation_dict[self.current_language]['calculate'])
            self.history_label.config(text=self.translation_dict[self.current_language]['history'])
            self.button_clear_history.config(text=self.translation_dict[self.current_language]['clear_history'])
            self.settings_label.config(text=self.translation_dict[self.current_language]['settings'])
            self.plot_button.config(text=self.translation_dict[self.current_language]['plot'])
            self.label_name.config(text=self.translation_dict[self.current_language]['name'])
            self.label_age.config(text=self.translation_dict[self.current_language]['age'])
            self.label_gender.config(text=self.translation_dict[self.current_language]['gender'])
            self.button_save_profile.config(text=self.translation_dict[self.current_language]['save_profile'])
            self.button_load_profile.config(text=self.translation_dict[self.current_language]['load_profile'])
            self.dialog_button.config(text=self.translation_dict[self.current_language]['settings_dialog'])
            self.export_button.config(text=self.translation_dict[self.current_language]['export_data'])
            self.button_submit_feedback.config(text=self.translation_dict[self.current_language]['submit_feedback'])
            self.theme_button.config(text=self.translation_dict[self.current_language]['toggle_theme'])
            self.help_button.config(text=self.translation_dict[self.current_language]['help'])
            self.import_button.config(text=self.translation_dict[self.current_language]['import_data'])
            self.language_menu.set(self.current_language)

    def load_user_preferences(self):
        if os.path.exists(self.user_preferences_file):
            with open(self.user_preferences_file, 'r') as file:
                preferences = json.load(file)
                self.theme = preferences.get('theme', 'light')
                self.current_language = preferences.get('language', 'English')

root = tk.Tk()
app = BMICalculator(root)
root.mainloop()
