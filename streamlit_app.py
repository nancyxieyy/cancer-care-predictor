# streamlit_app.py
import streamlit as st
import pandas as pd
import joblib

st.title('Cancer Prediction Application')

# Loading Models
clf = joblib.load("survival_rate_model.pkl")

# Getting user input
sex = st.selectbox("Sex", ("Male", "Female"))
rfs_event = st.number_input("Relapse or not (0=No, 1=Yes)", min_value=0, max_value=1, step=1)

# Adding conditional logic for input
if rfs_event == 0:
    rfs_months = st.number_input("Duration before relapse occurs(month) - will be set equal to duration before death", min_value=0)
    os_months = rfs_months  # Set os_months equal to rfs_months if no relapse
elif rfs_event == 1:
    rfs_months = st.number_input("Duration before relapse occurs(month)", min_value=0)
    os_months = st.number_input("Duration before death(month) - must be greater than duration before relapse", min_value=rfs_months+1)

# When the user clicks the submit button
if st.button("Submit"):
    # Check if inputs satisfy the conditions
    if rfs_event == 1 and rfs_months >= os_months:
        st.error("Duration before death must be greater than duration before relapse when relapse occurs.")
    else:
        # Convert inputs to the format required by the model
        input_df = pd.DataFrame([[rfs_event, rfs_months, os_months]], columns=['rfs_event', 'rfs_months', 'os_months'])

        # Probabilistic prediction using the predict_proba method
        prediction_probabilities = clf.predict_proba(input_df)
        # Probability of acquiring a death
        death_probability = prediction_probabilities[0][1]

        # Probability of output death
        st.write(f"The probability of death is {death_probability:.2f}")
