# CancerCare · AI-Based Cancer Prognosis Web App ｜癌症预测与医疗辅助系统

> "The greatest wealth is health."  
> 「健康，是最大的财富。」

## Overview | 项目简介

**CancerCare** is a full-stack web application designed to assist doctors in predicting cancer patient survival rates using machine learning models. The system supports doctor-patient interaction by integrating the ChatGPT API for automated consultation suggestions.  

**CancerCare** 是一个基于机器学习的癌症患者生存率预测系统，支持医生通过网页输入患者资料后，自动计算预后结果，并集成 ChatGPT API 实现智能化医疗辅助问答，提升医生工作效率与用户体验。


## Features | 项目功能

- ✅ **Patient Form Input** — User-friendly form for submitting medical info  
  友好的患者数据输入表单
- ✅ **ML-Based Prediction** — Backend predicts survival rate using trained models  
  基于机器学习模型的生存率预测
- ✅ **ChatGPT Integration** — Medical Q&A with OpenAI API  
  集成 ChatGPT API 实现智能问诊建议
- ✅ **Login System with Session** — Secure access for healthcare professionals  
  登录系统（使用 Flask Session 管理）

## Tech Stack | 技术栈

- **Frontend | 前端**：HTML/CSS, Jinja2 Templates
- **Backend | 后端**：Python, Flask
- **Machine Learning | 机器学习**：Scikit-learn, SVC, DecisionTree, RandomForest
- **API Integration | 接口集成**：OpenAI GPT-3.5 Turbo
- **Session/User Auth | 用户认证**：Flask-Login, Flask-Session
- **Data | 数据模型**：已训练模型（存于本地）

## Screenshots | 页面截图

Login Page 登录页面  
<img width="1470" alt="截屏2025-06-11 00 27 21" src="https://github.com/user-attachments/assets/991e8bcc-a799-4369-975d-22602773a5e8" />

usename|测试账户：`admin`  password|密码：`123456`

## How to Run Locally | 本地运行方式

### Step 1. Clone 仓库 & 安装依赖
```bash
git clone https://github.com/nancyxieyy/csc3002.git
cd csc3002/web
pip install -r requirements.txt
```

### Step 2. 创建 .env 文件，写入密钥
在 web/ 目录下创建 .env 文件
```
SECRET_KEY=your_secret_key_here
OPENAI_API_KEY=your_openai_key_here
```

### Step 3. 运行 Flask 应用
```
python run.py
```
浏览器访问 http://127.0.0.1:5000/

## Project Structure | 项目结构说明
```bash
web/
├── app/              # Flask 应用核心代码
│   ├── templates/    # 前端模板（HTML）
│   ├── static/       # 样式、图片等静态资源
│   └── views.py      # 路由与视图逻辑
├── models/           # 保存 ML 模型文件
├── run.py            # 程序入口
├── .env              # 环境变量（不上传）
├── requirements.txt  # 所需依赖
```
## Author | 作者信息
Nancy Xie (谢越莹)
- 2024 本科毕业设计 · 广东工业大学 & 贝尔法斯特女王大学
- 擅长 Python + Web + AI 应用开发
- GitHub: nancyxieyy

## Notes | 注意事项
- 若模型无法加载，请确认当前 scikit-learn 版本兼容模型保存版本。
- 如果你没有 OpenAI API Key，ChatGPT 功能无法使用，但其他功能仍可体验。

## License
This project is for educational use only.

本项目仅用于教学与展示用途。
