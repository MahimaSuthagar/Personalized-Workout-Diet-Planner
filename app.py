import streamlit as st
import pandas as pd
import io
from calculators import calculate_bmr, calculate_tdee, calculate_macros
from generators import generate_diet_plan, generate_workout_plan
from utils import create_pdf

st.set_page_config(page_title="Personalized Diet & Workout Planner", page_icon="💪", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        width: 100%;
    }
    .stat-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #FF4B4B;
    }
    .stat-label {
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💪 Personalized Diet & Workout Planner")
st.markdown("### Generate your personalized plan instantly without sign-ups.")

with st.sidebar:
    st.header("Your Profile")
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", 18, 100, 25)
    weight = st.number_input("Weight (kg)", 40, 150, 70)
    height = st.number_input("Height (cm)", 140, 220, 175)
    activity = st.selectbox("Activity Level", [
        "Sedentary (little or no exercise)",
        "Lightly active (light exercise/sports 1-3 days/week)",
        "Moderately active (moderate exercise/sports 3-5 days/week)",
        "Very active (hard exercise/sports 6-7 days a week)",
        "Super active (very hard exercise/physical job)"
    ])
    goal = st.selectbox("Fitness Goal", ["Lose Weight", "Maintain", "Gain Muscle"])
    diet_pref = st.selectbox("Dietary Preference", ["Any", "Vegetarian", "Vegan"])
    fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
    
    generate_btn = st.button("Generate Plan")

if "generated" not in st.session_state:
    st.session_state.generated = False

if generate_btn:
    st.session_state.generated = True
    
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity)
    macros = calculate_macros(tdee, goal, weight)
    
    st.session_state.stats = {
        "BMR": bmr,
        "TDEE": tdee,
        "Macros": macros
    }
    
    diet_plan, actual_cals = generate_diet_plan(macros["calories"], diet_pref)
    workout_plan = generate_workout_plan(goal, fitness_level)
    
    st.session_state.diet_plan = diet_plan
    st.session_state.diet_cals = actual_cals
    st.session_state.workout_plan = workout_plan

if st.session_state.generated:
    stats = st.session_state.stats
    
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='stat-card'><div class='stat-value'>{int(stats['TDEE'])}</div><div class='stat-label'>Daily Calories Target</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats['Macros']['protein']}g</div><div class='stat-label'>Protein</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats['Macros']['carbs']}g</div><div class='stat-label'>Carbs</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats['Macros']['fats']}g</div><div class='stat-label'>Fats</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🥗 Diet Plan", "🏋️ Workout Plan"])
    
    with tab1:
        st.subheader("Recommended Daily Meal Plan")
        st.info(f"Generated Plan Total: {st.session_state.diet_cals} kcal")
        
        diet_df = pd.DataFrame(st.session_state.diet_plan)
        if not diet_df.empty:
            cols = ["type", "name", "calories", "protein", "carbs", "fats"]
            st.dataframe(diet_df[cols], use_container_width=True)
        else:
            st.warning("Could not generate a full meal plan with current filters.")
            
    with tab2:
        st.subheader("Recommended Routine")
        st.write(f"**Focus**: {goal} | **Level**: {fitness_level}")
        st.write(f"**Warmup**: {st.session_state.workout_plan['Warmup']}")
        
        workout_df = pd.DataFrame(st.session_state.workout_plan['Exercises'])
        if not workout_df.empty:
            st.table(workout_df)
        else:
            st.warning("No exercises found matching criteria.")
            
    st.markdown("---")
    if st.button("Generate PDF Report"):
        pdf = create_pdf(st.session_state.stats, st.session_state.diet_plan, st.session_state.workout_plan)
        try:
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button(
                label="Download PDF Plan",
                data=pdf_output,
                file_name="my_fitness_plan.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error generating PDF: {e}")

else:
    st.info("👈 Enter your details in the sidebar and click 'Generate Plan' to get started!")
    st.image("https://images.unsplash.com/photo-1517836357463-d25dfeac3438?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", use_container_width=True, caption="Achieve your goals today.")
