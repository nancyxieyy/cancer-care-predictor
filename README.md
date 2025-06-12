# CancerCare | AI-Based Cancer Prognosis Web App ｜癌症预测与智能问诊系统

> A web app that helps doctors predict cancer patient outcomes using machine learning and ChatGPT integration.  
> 利用机器学习和 ChatGPT，辅助医生评估癌症患者生存率的智能网页应用。

## 💡 Features | 功能亮点

- 🔍 Form input for patient data | 表单输入患者信息
- 🧠 ML prediction (SVC, RandomForest) | 机器学习预测模型
- 🤖 ChatGPT API integration | 接入 ChatGPT 提供问诊建议
- 👩‍⚕️ Simple UI for clinical use | 医疗场景友好的界面设计

## 🛠 Tech Stack | 技术栈

- Backend: Python, Flask
- ML: Scikit-learn
- Frontend: HTML/CSS (Jinja2)
- API: OpenAI GPT-3.5 Turbo
- Auth: Session-based login

## 🚀 Run Locally | 本地运行方式

```bash
git clone https://github.com/nancyxieyy/cancer-care-predictor.git
cd web/
pip install -r requirements.txt
python run.py
```
Create a .env file in the /web folder:

```ini
SECRET_KEY=your_secret
OPENAI_API_KEY=sk-xxxxxxxxxxxx
```
Access: http://127.0.0.1:5000/

## 📸 Screenshot
<img width="1470" alt="截屏2025-06-11 00 27 21" src="https://github.com/user-attachments/assets/991e8bcc-a799-4369-975d-22602773a5e8" />

## 📁 Structure
```php
web/
├── app/           # Flask views and templates
├── models/        # Pre-trained ML models
├── static/        # CSS & images
├── templates/     # HTML pages
├── run.py         # App entry
```

## 📄 License
For academic and demo use only. 项目仅供学习展示使用。
