import csv
import tkinter as tk
from tkinter import ttk, messagebox

# Global variables for data
categories = {}
descriptions = {}
precautions = {}

# Function to load data from CSV
def load_data(file_path):
    data = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header if present
            for row in csv_reader:
                disease = row[0].strip()
                symptoms = [symptom.strip() for symptom in row[1:] if symptom.strip()]
                if disease in data:
                    data[disease].extend(symptoms)  # Aggregate symptoms for repeated diseases
                else:
                    data[disease] = symptoms
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
    return data.items()

# Function to load descriptions from CSV
def load_descriptions(file_path):
    descriptions = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header if present
            for row in csv_reader:
                disease = row[0].strip()
                description_list = [description.strip() for description in row[1:] if description.strip()]
                descriptions[disease] = description_list
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred while loading descriptions: {e}")
    return descriptions

# Function to load precautions from CSV
def load_precautions(file_path):
    precautions = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header if present
            for row in csv_reader:
                disease = row[0].strip()
                precaution_list = [precaution.strip() for precaution in row[1:] if precaution.strip()]
                precautions[disease] = precaution_list
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred while loading precautions: {e}")
    return precautions

# Function to categorize diseases into predefined categories
def categorize_diseases(data):
    categories = {
        'Respiratory System Diseases': {'Bronchial Asthma', 'Pneumonia', 'Tuberculosis', 'Common Cold'},
        'Digestive System Diseases': {'GERD', 'Chronic Cholestasis', 'Peptic Ulcer Disease', 'Alcoholic Hepatitis', 
                                      'Hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E'},
        'Cardiovascular Diseases': {'Heart Attack', 'Hypertension'},
        'Endocrine System Diseases': {'Diabetes', 'Hyperthyroidism', 'Hypothyroidism', 'Hypoglycemia'},
        'Musculoskeletal System Diseases': {'Osteoarthritis', 'Arthritis', 'Cervical Spondylosis'},
        'Neurological Diseases': {'Paralysis (Brain Hemorrhage)', 'Migraine', 'Vertigo (Paroxysmal Positional Vertigo)'},
        'Infectious Diseases': {'Fungal Infection', 'AIDS', 'Urinary Tract Infection', 'Malaria', 'Chicken Pox', 
                                'Dengue', 'Typhoid'},
        'Skin Diseases': {'Acne', 'Impetigo', 'Psoriasis'},
        'Other Diseases': {'Varicose Veins', 'Allergy', 'Drug Reaction', 'Gastroenteritis'}
    }

    categorized_diseases = {}
    for disease, symptoms in data:
        categorized = False
        for category, diseases in categories.items():
            if disease in diseases:
                categorized_diseases.setdefault(category, []).append((disease, symptoms))
                categorized = True
                break
        if not categorized:
            categorized_diseases.setdefault('Other Diseases', []).append((disease, symptoms))

    return categorized_diseases

# Function to predict disease based on selected symptoms
def predict_disease(diseases_in_category, selected_symptoms):
    matched_diseases = {}
    for disease, symptoms in diseases_in_category:
        matched_count = sum(1 for symptom in selected_symptoms if symptom in symptoms)
        if matched_count >= 2:
            matched_diseases[disease] = matched_count

    if matched_diseases:
        sorted_diseases = sorted(matched_diseases.items(), key=lambda x: x[1], reverse=True)
        return sorted_diseases
    else:
        return []

# Function to display predictions and options
def display_predictions(predictions, root, category_var, symptom_vars):
    if predictions:
        if len(predictions) > 1:
            result_text = "\nMultiple diseases match the selected symptoms:\n"
            for disease, _ in predictions:
                result_text += f"{disease}\n"
            result_text += "\nPlease select more symptoms to narrow down the diagnosis."
            
            messagebox.showinfo("Multiple Matches", result_text)
        else:
            result_text = "\nPredicted Disease:\n"
            for disease, _ in predictions:
                result_text += f"{disease}\n"
                if disease in descriptions:
                    result_text += "Description:\n"
                    for description in descriptions[disease]:
                        result_text += f"- {description}\n"
                else:
                    result_text += "No description found for this disease.\n"
                
                if disease in precautions:
                    result_text += "Precautions:\n"
                    for precaution in precautions[disease]:
                        result_text += f"- {precaution}\n"
                else:
                    result_text += "No precautions found for this disease.\n"

            messagebox.showinfo("Disease Prediction Results", result_text)
            
            # Ask user if they want to go back to the main interface or exit
            choice = messagebox.askquestion("Continue", "Do you want to go back to the main interface?")
            if choice == 'yes':
                start_application(root)
            else:
                root.destroy()
    else:
        messagebox.showinfo("Disease Prediction Results", "No diseases found matching the minimum 2 symptoms in this category.")

# Function to handle prediction button click
def on_predict_button_click(root, category_var, symptom_vars):
    selected_category = category_var.get()
    if not selected_category:
        messagebox.showwarning("Warning", "Please select a disease category.")
        return

    selected_symptoms = [symptom for symptom, var in symptom_vars.items() if var.get()]
    if not selected_symptoms:
        messagebox.showwarning("Warning", "Please select at least one symptom.")
        return

    diseases_in_category = categories[selected_category]
    predictions = predict_disease(diseases_in_category, selected_symptoms)
    display_predictions(predictions, root, category_var, symptom_vars)

# Function to show introduction screen
def show_introduction(root):
    intro_text = ("Welcome to Medical Diagnosis Agent!\n\n"
                  "This application helps predict possible diseases based on symptoms you select.\n"
                  "Please choose a disease category and select symptoms to begin prediction.\n\n"
                  "Click 'Start' to begin.")

    intro_label = tk.Label(root, text=intro_text, justify='left', padx=20, pady=20)
    intro_label.pack()

    start_button = tk.Button(root, text="Start", command=lambda: start_application(root))
    start_button.pack(pady=10)

# Function to start the main application interface
def start_application(root):
    # Clear the introduction screen widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create a frame for the category selection
    frame_category = ttk.LabelFrame(root, text="Select Disease Category")
    frame_category.pack(fill="x", padx=10, pady=10)

    # Create a dropdown menu for disease categories
    category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(frame_category, textvariable=category_var)
    category_dropdown['values'] = list(categories.keys())
    category_dropdown.pack(fill="x", padx=10, pady=10)

    # Create a frame for symptoms selection
    frame_symptoms = ttk.LabelFrame(root, text="Select Symptoms")
    frame_symptoms.pack(fill="x", padx=10, pady=10)

    symptom_vars = {}
    checkbuttons = []

    def update_symptoms(*args):
        for cb in checkbuttons:
            cb.destroy()
        checkbuttons.clear()
        selected_category = category_var.get()
        if selected_category:
            diseases_in_category = categories[selected_category]
            all_symptoms = list(set(symptom for disease, symptoms in diseases_in_category for symptom in symptoms))
            num_columns = 3  # Number of columns for symptoms layout
            for i, symptom in enumerate(all_symptoms):
                var = tk.BooleanVar()
                cb = ttk.Checkbutton(frame_symptoms, text=symptom, variable=var)
                cb.grid(row=i // num_columns, column=i % num_columns, sticky="w", padx=5, pady=2)
                symptom_vars[symptom] = var
                checkbuttons.append(cb)

    category_var.trace('w', update_symptoms)

    # Create a button to predict the disease
    predict_button = ttk.Button(root, text="Diagnose", command=lambda: on_predict_button_click(root, category_var, symptom_vars))
    predict_button.pack(padx=10, pady=20)

# Load data
file_path_symptoms = r'dataset1.csv'  # Replace with your CSV file path for symptoms
file_path_descriptions = r'symptom_Description.csv'  # Replace with your CSV file path for descriptions
file_path_precautions = r'symptom_precaution.csv'  # Replace with your CSV file path for precautions

data = load_data(file_path_symptoms)
categories = categorize_diseases(data)
descriptions = load_descriptions(file_path_descriptions)
precautions = load_precautions(file_path_precautions)

# Create main application window
root = tk.Tk()
root.title("Medical Diagnosis Assistant")

# Show introduction screen
show_introduction(root)

# Run the main loop
root.mainloop()
