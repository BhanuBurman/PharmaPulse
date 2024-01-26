// Login.jsx
import React, { useState, useEffect } from 'react';
import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';

import "./Login.scss";

const Login = (props) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [loginSuccess, setLoginSuccess] = useState(false);

  const handleLogin = async () => {
    try {
      // Clear previous errors and success state
      setEmailError('');
      setPasswordError('');
      setLoginSuccess(false);

      // Validation checks
      if (!email) {
        setEmailError('Email is required.');
        return;
      }

      if (!password) {
        setPasswordError('Password is required.');
        return;
      }

      // Firebase login
      await firebase.auth().signInWithEmailAndPassword(email, password);
      console.log('Login successful');

      // Set login success state
      setLoginSuccess(true);

      // Automatically close the popup after 2 seconds
      setTimeout(() => {
        props.onClose();
      }, 2000);
    } catch (error) {
      // Handle Firebase authentication errors
      if (error.code === 'auth/invalid-email' || error.code === 'auth/user-not-found' || error.code === 'auth/wrong-password') {
        setEmailError('Invalid email or password. Please try again.');
        setPasswordError('Invalid email or password. Please try again.');
      } else if(error.code === 'auth/invalid-credential') {
        setEmailError('Invalid-Credentials. Please try again.');
        setPasswordError('Invalid-Credentials. Please try again.');
      }else {
        console.error('Error logging in:', error.message);
      }
    }
  };

  useEffect(() => {
    // Cleanup function to clear the success state after unmounting
    return () => {
      setLoginSuccess(false);
    };
  }, []);

  return (
    <div className="popup-overlay">
      <div className={`popup-login ${loginSuccess ? 'success' : ''}`}>
        <button className="close__button" onClick={props.onClose}>X</button>
        <h2>Login</h2>

        <form>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setEmailError('');
            }}
            style={{
              borderColor: emailError ? 'red' : '',
            }}
          />
          {emailError && <div className="error-message">{emailError}</div>}

          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ borderColor: passwordError ? 'red' : '' }}
          />
          {passwordError && <div className="error-message">{passwordError}</div>}

          <button
            type="button"
            className={`login__button ${loginSuccess ? 'success' : ''}`}
            onClick={handleLogin}
            disabled={loginSuccess}
            style={{
              backgroundColor: loginSuccess?'green':'',
              fontSize: loginSuccess ? 'small' : '', // Apply smaller font size only when successful
            }}
          >
            {loginSuccess ? 'Successful' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
