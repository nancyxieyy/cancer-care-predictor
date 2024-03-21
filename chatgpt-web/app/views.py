from flask import Blueprint, app, request, jsonify, render_template, redirect, url_for, session, current_app
import pandas as pd
import requests
import joblib
import os

main = Blueprint('main', __name__)

# 全局变量用于存储模型
model = None

def load_model():
    global model
    model_path = os.path.join(current_app.root_path, 'models', 'model.pkl')
    model = joblib.load(model_path)

@main.before_app_first_request
def before_first_request():
    load_model()

# 假设的用户名和密码
USERNAME = 'admin'
PASSWORD = '123456'

@main.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('main.home'))  # 如果已登录，则重定向到主页

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['username'] = username
            return redirect(url_for('main.home'))  # 登录成功，重定向到主页
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('username', None)  # 登出用户
    return redirect(url_for('main.login'))  # 重定向到登录页面

@main.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')  # 展示主页
    return redirect(url_for('main.login'))  # 未登录则重定向到登录页面

@main.route('/chat')
def chat():
    if 'username' in session:
        return render_template('index.html')  # 确保用户已登录才能访问聊天页面
    return redirect(url_for('main.login'))  # 未登录用户重定向到登录页面

@main.route('/')
def index():
    return redirect(url_for('main.login'))  # 根路径重定向到登录页面

@main.route('/ask', methods=['POST'])
def ask():
    if 'username' not in session:
        return jsonify({'answer': 'You are not logged in.'}), 401  # 如果用户未登录，则返回错误

    # 如果用户已登录，则调用 ChatGPT API
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
            'rfs_event': int(request.form.get('relapse', 0)),
            'rfs_months': int(request.form.get('relapse_months', 0)),
            'os_months': int(request.form.get('death_months', 0))
        }

        input_df = pd.DataFrame([form_data])
        global model
        if model is not None:
            prediction = predict_death_probability(model, input_df)
            return jsonify({'prediction': str(prediction)})
        else:
            return jsonify({'error': 'Model could not be loaded'}), 500

    return render_template('survival.html', prediction=prediction)

def predict_death_probability(model, input_features):
    prediction = model.predict_proba(input_features)[0][1]
    return prediction