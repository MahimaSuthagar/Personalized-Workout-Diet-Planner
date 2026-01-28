def calculate_bmr(weight_kg, height_cm, age, gender):
    """
    Mifflin-St Jeor Equation to calculate Basal Metabolic Rate (BMR)
    """
    if gender.lower() == "male":
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

def calculate_tdee(bmr, activity_level):
    """
    Calculate Total Daily Energy Expenditure (TDEE) based on activity level
    """
    multipliers = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly active (light exercise/sports 1-3 days/week)": 1.375,
        "Moderately active (moderate exercise/sports 3-5 days/week)": 1.55,
        "Very active (hard exercise/sports 6-7 days a week)": 1.725,
        "Super active (very hard exercise/physical job)": 1.9
    }
    return bmr * multipliers.get(activity_level, 1.2)

def calculate_macros(tdee, goal, weight_kg):
    """
    Calculate macronutrients based on goal
    Returns a dictionary with grams of Protein, Carbs, Fats
    """
    if goal == "Lose Weight":
        target_calories = tdee - 500
        protein_g = 2.2 * weight_kg
        fats_g = 0.8 * weight_kg
        protein_cals = protein_g * 4
        fats_cals = fats_g * 9
        carbs_cals = target_calories - (protein_cals + fats_cals)
        carbs_g = carbs_cals / 4
        
    elif goal == "Gain Muscle":
        target_calories = tdee + 300
        protein_g = 2.0 * weight_kg
        fats_g = 1.0 * weight_kg 
        protein_cals = protein_g * 4
        fats_cals = fats_g * 9
        carbs_cals = target_calories - (protein_cals + fats_cals)
        carbs_g = carbs_cals / 4

    else:
        target_calories = tdee
        protein_g = 1.6 * weight_kg
        fats_g = 1.0 * weight_kg
        protein_cals = protein_g * 4
        fats_cals = fats_g * 9
        carbs_cals = target_calories - (protein_cals + fats_cals)
        carbs_g = carbs_cals / 4
    
    return {
        "calories": int(target_calories),
        "protein": int(protein_g),
        "fats": int(fats_g),
        "carbs": int(carbs_g)
    }
