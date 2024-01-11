import React from 'react'
import userAvatar from '../images/User.png'; // 更新为正确的路径
import botAvatar from '../images/Rot.jpeg'; // 更新为正确的路径

const AnswerSection = ({ storedValues }) => {

    return (
        <div className="chat-display">
      {storedValues.slice(0).reverse().map((value, index) => (
        <div key={index} className={`message ${value.author === 'user' ? 'user-message' : 'bot-message'}`}>
          <img src={value.author === 'user' ? userAvatar : botAvatar} alt="avatar" className="avatar" />
          <div className="message-content">{value.content}</div>
        </div>
      ))}
    </div>
    );
};

export default AnswerSection