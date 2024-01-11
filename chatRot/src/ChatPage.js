import React, { useState } from 'react';
import FormSection from './components/FormSection';
import AnswerSection from './components/AnswerSection';
import { Configuration, OpenAIApi } from 'openai';
import userAvatar from './images/User.png';
import rotAvatar from './images/Rot.jpeg';

const ChatPage = () => {
    const [storedValues, setStoredValues] = useState([]);
    const configuration = new Configuration({
        apiKey: process.env.REACT_APP_OPENAI_API_KEY,
    });

    const openai = new OpenAIApi(configuration);

    const sendMessage = async (newQuestion) => {
        if (!newQuestion.trim()) return; // 如果输入为空，则不执行任何操作

        // 首先，把用户的问题添加到消息列表
        const userMessage = {
            author: 'user',
            content: newQuestion,
            avatar: userAvatar, // 替换为用户头像的URL
        };
        setStoredValues(prevValues => [userMessage, ...prevValues]);

        try {
            const response = await openai.createChatCompletion({
                model: "gpt-3.5-turbo",
                messages: [
                    { role: "user", content: newQuestion }
                ],
            });

            if (response.data.choices) {
                const latestResponse = response.data.choices[0].message.content;
                // 然后，添加机器人的回复到消息列表
                const botMessage = {
                    author: 'bot',
                    content: latestResponse,
                    avatar: rotAvatar, // 替换为机器人头像的URL
                };
                setStoredValues(prevValues => [botMessage, ...prevValues]);
            } else {
                console.error("No response data received from OpenAI API");
            }
        } catch (error) {
            console.error("There was an error in generating a response: ", error);
            // 可以选择在此处处理错误，例如添加一条错误消息
        }
    };

    return (
        <div>
            <div class="header"></div>
            <input type="checkbox" class="openSidebarMenu" id="openSidebarMenu"></input>
            <label for="openSidebarMenu" class="sidebarIconToggle">
                <div class="spinner diagonal part-1"></div>
                <div class="spinner horizontal"></div>
                <div class="spinner diagonal part-2"></div>
            </label>
            <div id="sidebarMenu">
                <ul class="sidebarMenuInner">
                    <li>ChatRot🤖 <span>Cancer Prediction</span></li>
                    <li>HOME</li>
                    <li>GitLab</li>
                    <li>GitHub</li>
                    <li>Email</li>
                    <li>setting</li>
                </ul>
            </div>
            <div id='center' class="main center">
                <div class="mainInner">
                    <div className="chat-container">
                        <div className="chat-display">
                            <AnswerSection storedValues={storedValues} />
                        </div>
                        <div className="chat-input">
                            <FormSection sendMessage={sendMessage} />
                        </div>
                    </div>
                </div>
            </div>    
        </div>
    );
};

export default ChatPage;
