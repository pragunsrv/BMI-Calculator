import tkinter as tk
from tkinter import messagebox

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        self.create_widgets()

    def create_widgets(self):
        self.label_weight = tk.Label(self.root, text="Weight (kg):")
        self.label_weight.grid(row=0, column=0, padx=10, pady=10)

        self.entry_weight = tk.Entry(self.root)
        self.entry_weight.grid(row=0, column=1, padx=10, pady=10)

        self.label_height = tk.Label(self.root, text="Height (m):")
        self.label_height.grid(row=1, column=0, padx=10, pady=10)

        self.entry_height = tk.Entry(self.root)
        self.entry_height.grid(row=1, column=1, padx=10, pady=10)

        self.button_calculate = tk.Button(self.root, text="Calculate BMI", command=self.calculate_bmi)
        self.button_calculate.grid(row=2, column=0, columnspan=2, pady=20)

        self.label_result = tk.Label(self.root, text="")
        self.label_result.grid(row=3, column=0, columnspan=2, pady=10)

    def calculate_bmi(self):
        weight = self.entry_weight.get()
        height = self.entry_height.get()

        if not weight or not height:
            messagebox.showerror("Input Error", "Please enter both weight and height.")
            return

        try:
            weight = float(weight)
            height = float(height)
            if height <= 0:
                raise ValueError("Height must be greater than zero.")

            bmi = weight / (height * height)
            bmi_category = self.get_bmi_category(bmi)

            self.label_result.config(text=f"BMI: {bmi:.2f} ({bmi_category})")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()
