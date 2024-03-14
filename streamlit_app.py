# streamlit_app.py
import streamlit as st
import pandas as pd
import joblib

st.title('Cancer Prediction Application')

# Loading Models
clf = joblib.load("survival_rate_model.pkl")

# name
name = st.text_input("Name")
# Getting user input
# sex
sex = st.selectbox("Sex", ("Male", "Female"))

# age_at_diagnosis_in_years
age_at_diagnosis_in_years = st.number_input("Age", min_value=0)

# tnm_stage
tnm_stage = st.selectbox("Cancer stage of the patient",("2", "3"))

# chemotherapy_adjuvant
chemotherapy_adjuvant = st.selectbox("Did the patient receieved chemotherapy after surgery?", ("Yes", "No"))

# chemotherapy_adjuvant_type
if chemotherapy_adjuvant == "Yes":
    chemotherapy_adjuvant_type = st.selectbox("What sort of chemotherapy did the patient recieved?", ("5FU", "FOLFIRI", "FOLFOX", "FUFOL", "other"))
else:
    chemotherapy_adjuvant_type = "N/A"

# rfs_event
rfs_event = st.number_input("Relapse or not (0=No, 1=Yes)", min_value=0, max_value=1, step=1)

# rfs_months and os_months
if rfs_event == 0:
    rfs_months = st.number_input("Duration before relapse occurs(month) - will be set equal to duration before death", min_value=0)
    os_months = rfs_months  # Set os_months equal to rfs_months if no relapse
elif rfs_event == 1:
    rfs_months = st.number_input("Duration before relapse occurs(month)", min_value=0)
    os_months = st.number_input("Duration before death(month) - must be greater than duration before relapse", min_value=rfs_months+1)

# CMS
CMS = st.selectbox("Consensus Molecular Subtypes", ("CMS1", "CMS2", "CMS3", "CMS4", "UNK"))

# PDS
PDS_call = st.selectbox("Pathway-derived Subtypes", ("PDS1", "PDS2", "PSD3", "Mixed"))

# When the user clicks the submit button
if st.button("Submit"):
    # Check if inputs satisfy the conditions
    if rfs_event == 1 and rfs_months >= os_months:
        st.error("Duration before death must be greater than duration before relapse when relapse occurs.")
    else:
        # 假设这是从Streamlit获取的新数据（例如，通过表单提交）
        new_data = {'sex': [sex], 
                    'age_at_diagnosis_in_years': [age_at_diagnosis_in_years], 
                    'tnm_stage': [tnm_stage], 
                    'chemotherapy_adjuvant': [chemotherapy_adjuvant], 
                    'chemotherapy_adjuvant_type': [chemotherapy_adjuvant_type], 
                    'rfs_event': [rfs_event],
                    'rfs_months': [rfs_months], 
                    'os_months': [os_months], 
                    'CMS': [CMS], 
                    'PDS_call': [PDS_call]}

        # 转换为pandas DataFrame
        new_data_df = pd.DataFrame(new_data)

        # 读取现有数据集
        existing_data_df = pd.read_excel('gse39582_n469_clinical_data.xlsx', sheet_name='Sheet1')

        # 将新数据添加到现有数据集
        updated_data_df = pd.concat([existing_data_df, new_data_df], ignore_index=True)

        # 保存更新后的数据集
        updated_data_df.to_excel('gse39582_n469_clinical_data.xlsx', index=False, engine='openpyxl')

        # Convert inputs to the format required by the model
        input_df = pd.DataFrame([[rfs_event, rfs_months, os_months]], columns=['rfs_event', 'rfs_months', 'os_months'])

        # Probabilistic prediction using the predict_proba method
        prediction_probabilities = clf.predict_proba(input_df)
        # Probability of acquiring a death
        death_probability = prediction_probabilities[0][1]

        # Probability of output death
        st.write(f"The probability of death is {death_probability:.2f}")
