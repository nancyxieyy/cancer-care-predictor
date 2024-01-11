// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatPage from './ChatPage';
import Login from './Login'; // 假设你已经创建了 Login 组件

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/chat" element={<ChatPage />} />
    </Routes>
  </Router>
);

export default App;