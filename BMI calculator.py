import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import pandas as pd
import os

# File to store user data
FILE_NAME = "bmi_data.csv"

# Create a class for the Enhanced BMI Calculator Application
class EnhancedBMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced BMI Calculator")
        self.root.geometry("450x550")
        self.root.configure(bg='#cd94d1')

        # Load existing data
        self.user_data = self.load_data()

        # Create GUI Components
        self.create_widgets()

    def create_widgets(self):
        # Label for Height
        self.label_height = tk.Label(self.root, text="Enter Height (cm):", bg='#f0f8ff', fg='#000080', font=("Arial", 10, "bold"))
        self.label_height.grid(row=0, column=0, padx=10, pady=10)
        self.entry_height = tk.Entry(self.root, bg='#ffffff', fg='#000000', font=("Arial", 10))
        self.entry_height.grid(row=0, column=1)

        # Label for Weight
        self.label_weight = tk.Label(self.root, text="Enter Weight (kg):", bg='#f0f8ff', fg='#000080', font=("Arial", 10, "bold"))
        self.label_weight.grid(row=1, column=0, padx=10, pady=10)
        self.entry_weight = tk.Entry(self.root, bg='#ffffff', fg='#000000', font=("Arial", 10))
        self.entry_weight.grid(row=1, column=1)

        # Label for Gender
        self.label_gender = tk.Label(self.root, text="Select Gender:", bg='#f0f8ff', fg='#000080', font=("Arial", 10, "bold"))
        self.label_gender.grid(row=2, column=0, padx=10, pady=10)

        # Dropdown for Gender Selection
        self.gender_var = tk.StringVar()
        self.gender_combobox = ttk.Combobox(self.root, textvariable=self.gender_var, values=["Male", "Female", "Other"], state="readonly", font=("Arial", 10))
        self.gender_combobox.grid(row=2, column=1)
        self.gender_combobox.current(0)

        # Button to Calculate BMI
        self.btn_calculate = tk.Button(self.root, text="Calculate BMI", command=self.calculate_bmi, bg='#4682b4', fg='#ffffff', font=("Arial", 10, "bold"), width=20, pady=5)
        self.btn_calculate.grid(row=3, column=0, columnspan=2, pady=10)

        # Label to Display Result
        self.label_result = tk.Label(self.root, text="", font=("Arial", 12, "bold"), bg='#f0f8ff', fg='#ff4500')
        self.label_result.grid(row=4, column=0, columnspan=2, pady=10)

        # Button to Show History
        self.btn_show_history = tk.Button(self.root, text="View History", command=self.show_history, bg='#6a5acd', fg='#ffffff', font=("Arial", 10, "bold"), width=20, pady=5)
        self.btn_show_history.grid(row=5, column=0, columnspan=2, pady=5)

        # Button to View Trends
        self.btn_view_trends = tk.Button(self.root, text="View BMI Trends", command=self.view_trends, bg='#32cd32', fg='#ffffff', font=("Arial", 10, "bold"), width=20, pady=5)
        self.btn_view_trends.grid(row=6, column=0, columnspan=2, pady=5)

        # Button to View BMI Distribution (Histogram)
        self.btn_view_distribution = tk.Button(self.root, text="View BMI Distribution", command=self.view_distribution, bg='#ff69b4', fg='#ffffff', font=("Arial", 10, "bold"), width=20, pady=5)
        self.btn_view_distribution.grid(row=7, column=0, columnspan=2, pady=5)

        # Button to View BMI Category Pie Chart
        self.btn_view_pie_chart = tk.Button(self.root, text="View Category Pie Chart", command=self.view_pie_chart, bg='#ff8c00', fg='#ffffff', font=("Arial", 10, "bold"), width=20, pady=5)
        self.btn_view_pie_chart.grid(row=8, column=0, columnspan=2, pady=5)

    def load_data(self):
        if os.path.exists(FILE_NAME):
            return pd.read_csv(FILE_NAME).to_dict('records')
        return []

    def save_data(self):
        pd.DataFrame(self.user_data).to_csv(FILE_NAME, index=False)

    def calculate_bmi(self):
        try:
            height = float(self.entry_height.get()) / 100  # Convert to meters
            weight = float(self.entry_weight.get())
            gender = self.gender_var.get()
            bmi = weight / (height ** 2)

            # Determine BMI category (slightly different interpretations based on gender)
            if gender == "Male":
                if bmi < 18.5:
                    category = "Underweight"
                elif 18.5 <= bmi < 24.9:
                    category = "Normal weight"
                elif 25 <= bmi < 29.9:
                    category = "Overweight"
                else:
                    category = "Obese"
            elif gender == "Female":
                if bmi < 18.5:
                    category = "Underweight"
                elif 18.5 <= bmi < 24.9:
                    category = "Normal weight"
                elif 24 <= bmi < 29.9:
                    category = "Overweight"
                else:
                    category = "Obese"
            else:  # For "Other" or unspecified
                if bmi < 18.5:
                    category = "Underweight"
                elif 18.5 <= bmi < 25:
                    category = "Normal weight"
                elif 25 <= bmi < 30:
                    category = "Overweight"
                else:
                    category = "Obese"

            # Show result
            self.label_result.config(text=f"BMI: {bmi:.2f} ({category})")

            # Store in history and save to file
            entry = {"Height": height, "Weight": weight, "Gender": gender, "BMI": bmi, "Category": category}
            self.user_data.append(entry)
            self.save_data()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for height and weight.")

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("BMI History")
        history_window.configure(bg='#f0f8ff')

        # Create Treeview Table
        tree = ttk.Treeview(history_window, columns=("Height", "Weight", "Gender", "BMI", "Category"), show='headings')
        tree.heading("Height", text="Height (m)")
        tree.heading("Weight", text="Weight (kg)")
        tree.heading("Gender", text="Gender")
        tree.heading("BMI", text="BMI")
        tree.heading("Category", text="Category")

        # Insert historical data
        for entry in self.user_data:
            tree.insert("", "end", values=(entry["Height"], entry["Weight"], entry["Gender"], f"{entry['BMI']:.2f}", entry["Category"]))

        tree.pack(fill="both", expand=True)

    def view_trends(self):
        if not self.user_data:
            messagebox.showinfo("No Data", "No data available for trend analysis.")
            return

        df = pd.DataFrame(self.user_data)
        df["Index"] = range(1, len(df) + 1)

        plt.figure(figsize=(10, 6))
        plt.plot(df["Index"], df["BMI"], marker='o', linestyle='-', color='#4682b4', label="BMI Over Time")
        plt.axhline(y=24.9, color='g', linestyle='--', label="Normal BMI Threshold")
        plt.title("BMI Trend Over Time")
        plt.xlabel("Record Number")
        plt.ylabel("BMI")
        plt.legend()
        plt.grid(True)
        plt.show()

    def view_distribution(self):
        if not self.user_data:
            messagebox.showinfo("No Data", "No data available for distribution analysis.")
            return

        df = pd.DataFrame(self.user_data)

        # Histogram for BMI Distribution
        plt.figure(figsize=(10, 6))
        plt.hist(df["BMI"], bins=10, color='#6a5acd', edgecolor='black')
        plt.title("BMI Distribution")
        plt.xlabel("BMI")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.show()

    def view_pie_chart(self):
        if not self.user_data:
            messagebox.showinfo("No Data", "No data available for pie chart analysis.")
            return

        df = pd.DataFrame(self.user_data)
        category_counts = df["Category"].value_counts()

        # Pie chart for BMI Category
        plt.figure(figsize=(8, 6))
        category_counts.plot.pie(autopct='%1.1f%%', colors=['#32cd32', '#ff4500', '#ff8c00', '#4682b4'])
        plt.title("BMI Category Distribution")
        plt.ylabel("")
        plt.show()

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedBMICalculatorApp(root)
    root.mainloop()
