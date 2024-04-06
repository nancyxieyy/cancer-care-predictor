import streamlit as st
import pandas as pd
import joblib
import papermill as pm
import os

# 假设文件路径和名称
DATASET_PATH = 'Dataset/gse39582_n469_clinical_data.xlsx'
MODEL_PATH = 'model.pkl'
NOTEBOOK_PATH = 'survivalRate.ipynb'
OUTPUT_NOTEBOOK_PATH = 'output_survivalRate.ipynb'

st.title('Cancer Prediction Application')

# Loading the model
clf = joblib.load(MODEL_PATH)

# Function to predict the chance of death
def predict_death_probability(model, input_features):
    prediction = model.predict_proba(input_features)[0][1]
    return prediction

# Collecting user input
name = st.text_input("Name")
sex = st.selectbox("Sex", ("Male", "Female"))
age = st.number_input("Age", min_value=0)
stage = st.selectbox("Cancer stage of the patient", ("2", "3"))
chemo = st.selectbox("Did the patient receive chemotherapy after surgery?", ("Yes", "No"))
chemo_type = "N/A" if chemo == "No" else st.selectbox("Type of chemotherapy", ("5FU", "FOLFIRI", "FOLFOX", "FUFOL", "other"))
relapse = st.number_input("Relapse or not (0=No, 1=Yes)", min_value=0, max_value=1, step=1)
if relapse == 0:
    relapse_months = st.number_input("Duration before relapse occurs (month)", min_value=0)
    death_months = relapse_months
else:
    relapse_months = st.number_input("Duration before relapse occurs (month)", min_value=0)
    death_months = st.number_input("Duration before death (month)", min_value=relapse_months+1)
cms = st.selectbox("Consensus Molecular Subtypes", ("CMS1", "CMS2", "CMS3", "CMS4", "UNK"))
pds = st.selectbox("Pathway-derived Subtypes", ("PDS1", "PDS2", "PDS3", "Mixed"))

# When the user clicks the submit button
if st.button("Submit"):
    # Prepare data for the model prediction
    input_df = pd.DataFrame([[relapse, relapse_months, death_months]], columns=['rfs_event', 'rfs_months', 'os_months'])

    # Perform the model prediction
    death_probability = predict_death_probability(clf, input_df)
    st.write(f"The probability of death is {death_probability:.2f}")

    # Prepare new data for dataset update
    new_data = {'sex': [sex], 'age_at_diagnosis_in_years': [age], 'tnm_stage': [stage], 
                'chemotherapy_adjuvant': [chemo], 'chemotherapy_adjuvant_type': [chemo_type], 
                'rfs_event': [relapse], 'rfs_months': [relapse_months], 
                'os_months': [death_months], 'CMS': [cms], 'PDS_call': [pds]}

    new_data_df = pd.DataFrame(new_data)
    if os.path.exists(DATASET_PATH):
        existing_data_df = pd.read_excel(DATASET_PATH)
        updated_data_df = pd.concat([existing_data_df, new_data_df], ignore_index=True)
    else:
        updated_data_df = new_data_df
    
    # Save the updated dataset
    updated_data_df.to_excel(DATASET_PATH, index=False)

    # Trigger the Jupyter Notebook to retrain the model with the updated dataset
    pm.execute_notebook(
        NOTEBOOK_PATH,
        OUTPUT_NOTEBOOK_PATH,
        parameters={'data_path': DATASET_PATH, 'model_path': MODEL_PATH}
    )
    
    st.success("Data submitted successfully and model update initiated.")
