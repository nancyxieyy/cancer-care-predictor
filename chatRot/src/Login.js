import React, { useEffect, useRef, useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const passwordInputRef = useRef();
  const beamRef = useRef();

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (beamRef.current) {
        let rect = beamRef.current.getBoundingClientRect();
        let mouseX = rect.right + (rect.width / 2);
        let mouseY = rect.top + (rect.height / 2);
        let rad = Math.atan2(mouseX - e.pageX, mouseY - e.pageY);
        let degrees = (rad * (20 / Math.PI) * -1) - 350;
        document.documentElement.style.setProperty('--beamDegrees', `${degrees}deg`);
      }
    };

    document.documentElement.addEventListener('mousemove', handleMouseMove);

    return () => {
      document.documentElement.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
    if (passwordInputRef.current) {
      passwordInputRef.current.type = passwordInputRef.current.type === 'password' ? 'text' : 'password';
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    navigate('/chat'); // 导航到聊天页面
  };

  return (
    <div className={showPassword ? 'show-password' : ''}>
        <div className="shell">
      <form onSubmit={handleSubmit}>
        <h2>Login</h2>
        <div className="form-item">
          <label htmlFor="username">Username</label>
          <div className="input-wrapper">
            <input type="text" id="username" />
          </div>
        </div>
        <div className="form-item">
          <label htmlFor="password">Password</label>
          <div className="input-wrapper">
            <input ref={passwordInputRef} type="password" id="password" />
            <button type="button" id="eyeball" onClick={togglePasswordVisibility}>
              <div className="eye"></div>
            </button>
            <div id="beam" ref={beamRef}></div>
          </div>
        </div>
        <button type="submit" id="submit">Sign in</button>
      </form>
      </div>
    </div>
  );
};

export default Login;
