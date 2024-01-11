import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';  // 引入全局样式
import App from './App';  // 引入 App 组件

// 获取页面中的根元素
const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);

// 渲染 App 组件到根元素
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);


