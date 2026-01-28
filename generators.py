import json
import random
import os

def load_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    meals_path = os.path.join(base_path, "data", "meals.json")
    exercises_path = os.path.join(base_path, "data", "exercises.json")
    
    with open(meals_path, 'r') as f:
        meals = json.load(f)
    with open(exercises_path, 'r') as f:
        exercises = json.load(f)
    return meals, exercises

def generate_diet_plan(target_calories, diet_preference="Any"):
    meals, _ = load_data()
    
    if diet_preference != "Any":
        pref = diet_preference.lower()
        if pref == "vegetarian":
             meals = [m for m in meals if "vegetarian" in m.get("tags", []) or "vegan" in m.get("tags", [])]
        elif pref == "vegan":
             meals = [m for m in meals if "vegan" in m.get("tags", [])]
    
    breakfasts = [m for m in meals if m['type'] == 'breakfast']
    lunches = [m for m in meals if m['type'] == 'lunch']
    dinners = [m for m in meals if m['type'] == 'dinner']
    snacks = [m for m in meals if m['type'] == 'snack']
    
    plan = []
    current_cals = 0
    
    if breakfasts:
        b = random.choice(breakfasts)
        plan.append(b)
        current_cals += b['calories']
        
    if lunches:
        l = random.choice(lunches)
        plan.append(l)
        current_cals += l['calories']
        
    if dinners:
        d = random.choice(dinners)
        plan.append(d)
        current_cals += d['calories']
        
    attempts = 0
    while current_cals < target_calories - 100 and attempts < 20:
        if not snacks: break
        s = random.choice(snacks)
        plan.append(s)
        current_cals += s['calories']
        attempts += 1
        
    return plan, current_cals

def generate_workout_plan(goal, fitness_level):
    _, exercises = load_data()
    
    
    valid_exercises = []
    level_hierarchy = ["beginner", "intermediate", "advanced"]
    user_level_idx = level_hierarchy.index(fitness_level.lower()) if fitness_level.lower() in level_hierarchy else 1
    
    for ex in exercises:
        ex_level = ex.get('difficulty', 'beginner')
        ex_level_idx = level_hierarchy.index(ex_level) if ex_level in level_hierarchy else 0
        
        if ex_level_idx <= user_level_idx:
            valid_exercises.append(ex)
    
    workout_plan = {
        "Warmup": "5-10 mins light cardio",
        "Exercises": []
    }
    
    categories = {"chest": [], "back": [], "legs": [], "abs": [], "shoulders": [], "full_body": []}
    
    for ex in valid_exercises:
        cat = ex.get('muscle_group', 'full_body').split('/')[0]
        if cat in categories:
            categories[cat].append(ex)
        else:
            categories['full_body'].append(ex)
            
    selected_exercises = []
    
    for cat in ["chest", "back", "legs", "shoulders", "abs"]:
        if categories.get(cat):
            selected_exercises.append(random.choice(categories[cat]))
            
    if goal == "Lose Weight" and categories['full_body']:
         cardio = [ex for ex in valid_exercises if ex['type'] == 'cardio']
         if cardio:
             selected_exercises.append(random.choice(cardio))
             
    final_plan = []
    for ex in selected_exercises:
        if goal == "Lose Weight":
            sets, reps = "3", "12-15"
        elif goal == "Gain Muscle":
            sets, reps = "4", "8-12"
        else:
            sets, reps = "3", "10"
            
        if ex['type'] == 'cardio':
            sets, reps = "1", "20-30 mins"
            
        final_plan.append({
            "Exercise": ex['name'],
            "Sets": sets,
            "Reps": reps,
            "Equipment": ex.get('equipment', 'None')
        })
        
    workout_plan["Exercises"] = final_plan
    return workout_plan
