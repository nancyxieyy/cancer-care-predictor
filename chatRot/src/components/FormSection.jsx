import React, { useState } from 'react';

const FormSection = ({ sendMessage }) => {
    const [newQuestion, setNewQuestion] = useState('');

    const handleSubmit = () => {
        sendMessage(newQuestion);
        setNewQuestion(''); // 清空输入框
    };

    return (
        <div className="chat-input">
            <input
                type="text"
                id="message-input"
                placeholder="Ask me anything..."
                value={newQuestion}
                onChange={(e) => setNewQuestion(e.target.value)}
            />
            <button id="submit-btn" onClick={handleSubmit}>
                Send 🤖
            </button>
        </div>
    );
};

export default FormSection