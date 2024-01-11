import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder

file_path = 'gse39582_n469_clinical_data.xlsx'
df = pd.read_excel(file_path)

# Data preprocessing
df = df.dropna(subset=['sex', 'rfs_event', 'rfs_months', 'os_event'])

# 将分类数据转换为数值
le = LabelEncoder()
df['sex'] = le.fit_transform(df['sex'])  # 假设性别为二分类（例如，男性和女性）
df['rfs_event'] = le.fit_transform(df['rfs_event'])  # 假设复发事件为二分类（例如，是或否）

# 分割数据集
X = df[['sex', 'rfs_event', 'rfs_months']]
y = df['os_event']

# 标准化特征
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 分割训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 选择随机森林模型
model = RandomForestClassifier(random_state=42)

# 训练模型
model.fit(X_train, y_train)

# 预测
predictions = model.predict(X_test)

# 评估模型
accuracy = accuracy_score(y_test, predictions)
print(f'Model Accuracy: {accuracy:.2f}')
