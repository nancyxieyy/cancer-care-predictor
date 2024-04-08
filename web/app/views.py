from flask import Blueprint, app, request, jsonify, render_template, redirect, url_for, session, current_app
import pandas as pd
import requests
import joblib
import os

main = Blueprint('main', __name__)

# Global variables are used to store the model
survival_model = None
disease_model = None
treatment_model = None

survival_scaler = None
treatment_scaler = None

def load_model():
    global survival_model, disease_model, treatment_model, survival_scaler, treatment_scaler
    
    # The paths of models
    survival_model_path = os.path.join(current_app.root_path, 'models', 'survival_model.pkl')
    disease_model_path = os.path.join(current_app.root_path, 'models', 'disease_model.pkl')
    treatment_model_path = os.path.join(current_app.root_path, 'models', 'treatment_model.pkl')
    
    # Load the models
    survival_model = joblib.load(survival_model_path)
    disease_model = joblib.load(disease_model_path)
    treatment_model = joblib.load(treatment_model_path)
    
    # The paths of scalers
    survival_scaler_path = os.path.join(current_app.root_path, 'models', 'survival_scaler.pkl')
    treatment_scaler_path = os.path.join(current_app.root_path, 'models', 'treatment_scaler.pkl')
    
    # Load the scalers
    survival_scaler = joblib.load(survival_scaler_path)
    treatment_scaler = joblib.load(treatment_scaler_path)

@main.before_app_first_request
def before_first_request():
    load_model()

# Assumed username and password
USERNAME = 'admin'
PASSWORD = '123456'

@main.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        # Redirect to homepage if logged in
        return redirect(url_for('main.home'))  

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['username'] = username
            # Login successful, redirect to homepage
            return redirect(url_for('main.home'))  
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.login'))

@main.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('main.login'))

@main.route('/chat')
def chat():
    if 'username' in session:
        # Make sure users are logged in to access the chat page
        return render_template('chat.html')
    # Unlogged-in users redirected to login page
    return redirect(url_for('main.login'))  

@main.route('/')
def index():
    # Root path redirection to login page
    return redirect(url_for('main.login'))  

@main.route('/ask', methods=['POST'])
def ask():
    if 'username' not in session:
        return jsonify({'answer': 'You are not logged in.'}), 401  # Returns an error if the user is not logged in

    # If the user is logged in, the ChatGPT API is called
    data = request.get_json()
    user_message = data['message']
    response = call_chatgpt_api(user_message)
    return jsonify({'answer': response})

def call_chatgpt_api(message):
    api_key = os.getenv('OPENAI_API_KEY')
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': message}]
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    if response.status_code == 200:
        response_json = response.json()
        return response_json.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
    else:
        print("Error response from OpenAI:", response.text)
        return 'Sorry, there was an error processing your request.'

# survival rate
@main.route('/survival', methods=['GET', 'POST'])
def survival():
    if 'username' not in session:
        return redirect(url_for('main.login'))

    prediction = None

    if request.method == 'POST':
        form_data = {
            'age_at_diagnosis_in_years': int(request.form.get('age', 0)),
            'rfs_event': int(request.form.get('relapse', 0)),
            'rfs_months': int(request.form.get('relapse_months', 0)),
            'os_months': int(request.form.get('death_months', 0))
        }
        
        global survival_model, survival_scaler
        input_df = survival_scaler.transform(pd.DataFrame([form_data]))
        if survival_model is not None:
            prediction = predict_death_probability(survival_model, input_df)
            prediction = round(prediction * 100, 2)
            return jsonify({'prediction': str(prediction)})
        else:
            return jsonify({'error': 'Model could not be loaded'}), 500

    return render_template('survival.html', prediction=prediction)

def predict_death_probability(model, input_features):
    prediction = model.predict_proba(input_features)[0][1]
    return prediction

# relapse rate(treatment response)
@main.route('/treatment', methods=['GET', 'POST'])
def treatment():
    if 'username' not in session:
        return redirect(url_for('main.login'))

    prediction = None

    if request.method == 'POST':
        chemo_type = str(request.form.get('chemo_type', 'N/A'))
        cms = str(request.form.get('cms', 'UNK'))
        
        # Switching chemotherapy types according to mapping of chemotherapy types
        chemo_type_mapping = {'N/A': 0, '5FU': 1, 'FOLFIRI': 2, 'FOLFOX': 3, 'FUFOL': 4, 'other': 5}
        chemotherapy_adjuvant_type_numeric = chemo_type_mapping.get(chemo_type, 0)

        # CMS Mapping
        cms_mapping = {'CMS1': 1, 'CMS2': 2, 'CMS3': 3, 'CMS4': 4, 'UNK': 0}
        CMS_numeric = cms_mapping.get(cms, 0)
        
        form_data = {
            'age_at_diagnosis_in_years': int(request.form.get('age', 0)),
            'sex_numeric': 0 if request.form.get('sex') == 'Male' else 1,
            'tnm_stage': int(request.form.get('stage', 0)), 
            'chemotherapy_adjuvant_numeric': 0 if request.form.get('chemo') == 'No' else 1, 
            'chemotherapy_adjuvant_type_numeric':int(chemotherapy_adjuvant_type_numeric),
            'CMS_numeric': int(CMS_numeric)
        }
        
        global treatment_model, treatment_scaler
        input_df = treatment_scaler.transform(pd.DataFrame([form_data]))
        if treatment_model is not None:
            prediction = predict_relapse_probability(treatment_model, input_df)
            prediction = round(prediction * 100, 2)
            return jsonify({'prediction': str(prediction)})
        else:
            return jsonify({'error': 'Model could not be loaded'}), 500

    return render_template('treatment.html', prediction=prediction)

def predict_relapse_probability(model, input_features):
    prediction = model.predict_proba(input_features)[0][1]
    return prediction

# disease progression
@main.route('/disease', methods=['GET', 'POST'])
def disease():
    if 'username' not in session:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        try:
            chemo_type = request.form.get('chemo_type', 'N/A')
            cms = request.form.get('cms', 'UNK')
            
            chemo_type_mapping = {'N/A': 0, '5FU': 1, 'FOLFIRI': 2, 'FOLFOX': 3, 'FUFOL': 4, 'other': 5}
            chemotherapy_adjuvant_type_numeric = chemo_type_mapping.get(chemo_type, 0)
            cms_mapping = {'CMS1': 1, 'CMS2': 2, 'CMS3': 3, 'CMS4': 4, 'UNK': 0}
            CMS_numeric = cms_mapping.get(cms, 0)
            
            form_data = {
                'age_at_diagnosis_in_years': int(request.form.get('age', 0)),
                'sex_numeric': 0 if request.form.get('sex') == 'Male' else 1,
                'tnm_stage': int(request.form.get('stage', 0)), 
                'chemotherapy_adjuvant_numeric': 0 if request.form.get('chemo') == 'No' else 1, 
                'chemotherapy_adjuvant_type_numeric': chemotherapy_adjuvant_type_numeric,
                'CMS_numeric': CMS_numeric
            }
            
            print(form_data)
            
            global disease_model
            input_df = pd.DataFrame([form_data])
            if disease_model is not None:
                prediction = predict_progression_probability(disease_model, input_df)
                predictions = {
                    0: 'Stabilisation in condition',
                    1: 'Improvement in condition',
                    2: 'Worsening of the condition',
                    3: 'Pathological changes'
                }
                prediction_text = predictions.get(prediction, 'Unknown')
                return jsonify({'prediction': prediction_text})
            else:
                return jsonify({'error': 'Model could not be loaded'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('disease.html')

def predict_progression_probability(model, input_features):
    # Suppose the model returns a category label
    prediction = model.predict(input_features)[0]  
    return prediction