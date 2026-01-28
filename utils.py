from fpdf import FPDF
import pandas as pd

def create_pdf(stats, diet_plan, workout_plan, filename="plan.pdf"):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Your Personalized Diet & Workout Plan", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Your Stats", ln=True)
    pdf.set_font("Arial", "", 10)
    
    for key, val in stats['Macros'].items():
        pdf.cell(0, 8, f"{key.capitalize()}: {val}", ln=True)
    pdf.cell(0, 8, f"Target Daily Calories: {int(stats['TDEE'])}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Diet Plan", ln=True)
    pdf.set_font("Arial", "", 10)
    
    if diet_plan:
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(30, 10, "Type", 1, 0, 'C', 1)
        pdf.cell(90, 10, "Meal", 1, 0, 'C', 1)
        pdf.cell(30, 10, "Calories", 1, 1, 'C', 1)
        
        for meal in diet_plan:
            pdf.cell(30, 10, meal['type'].capitalize(), 1)
            pdf.cell(90, 10, meal['name'][:40], 1)
            pdf.cell(30, 10, str(meal['calories']), 1, 1)
    else:
        pdf.cell(0, 10, "No diet plan generated.", ln=True)
        
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Workout Plan", ln=True)
    pdf.set_font("Arial", "", 10)
    
    pdf.cell(0, 10, f"Warmup: {workout_plan.get('Warmup', 'None')}", ln=True)
    
    exercises = workout_plan.get('Exercises', [])
    if exercises:
        pdf.set_fill_color(200, 255, 200)
        pdf.cell(60, 10, "Exercise", 1, 0, 'C', 1)
        pdf.cell(30, 10, "Sets", 1, 0, 'C', 1)
        pdf.cell(30, 10, "Reps", 1, 1, 'C', 1)
        
        for ex in exercises:
            pdf.cell(60, 10, ex['Exercise'], 1)
            pdf.cell(30, 10, str(ex['Sets']), 1)
            pdf.cell(30, 10, str(ex['Reps']), 1, 1)
            
    return pdf
