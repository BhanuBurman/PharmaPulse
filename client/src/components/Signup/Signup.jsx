// Signup.jsx
import React, { useState, useEffect } from 'react';
import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';

import './Signup.scss'; // Import the styles

const Signup = (props) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [signupSuccess, setSignupSuccess] = useState(false);

  const isEmailValid = (email) => {
    // Use a regular expression to check email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSignup = async () => {
    try {
      // Clear previous errors and success state
      setEmailError('');
      setPasswordError('');
      setSignupSuccess(false);

      // Validation checks
      if (!email) {
        setEmailError('Email is required.');
        return;
      }

      if (!isEmailValid(email)) {
        setEmailError('Invalid email format.');
        return;
      }

      if (!password) {
        setPasswordError('Password is required.');
        return;
      }

      // Firebase signup
      await firebase.auth().createUserWithEmailAndPassword(email, password);
      console.log('Signup successful');

      // Set signup success state
      setSignupSuccess(true);

      // Automatically close the popup after 2 seconds
      setTimeout(() => {
        props.onClose();
      }, 2000);
    } catch (error) {
      // Handle Firebase authentication errors
      if (error.code === 'auth/invalid-email' || error.code === 'auth/email-already-in-use') {
        setEmailError('Invalid email or email already in use.');
      } else if (error.code === 'auth/weak-password') {
        setPasswordError('Weak password. Choose a stronger password.');
      } else {
        console.error('Error signing up:', error.message);
      }
    }
  };

  // Password strength indicator function
  const getPasswordStrengthColor = () => {
    // Add your own logic to determine password strength
    // For example, check length and inclusion of special characters
    if (password.length >= 8 && /[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      return 'green';
    } else if (password.length >= 8) {
      return 'yellow';
    } else {
      return 'red';
    }
  };

  useEffect(() => {
    // Cleanup function to clear the success state after unmounting
    return () => {
      setSignupSuccess(false);
    };
  }, []);

  return (
    <div className="popup-overlay">
      <div className={`popup-signup ${signupSuccess ? 'success' : ''}`}>
        <button className="close__button" onClick={props.onClose}>
          X
        </button>
        <h2>Signup</h2>
        <form action="">
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setEmailError('');
            }}
            style={{
              borderColor: emailError ? 'red' : isEmailValid(email) ? 'green' : '',
            }}
          />
          {emailError && <div className="error-message">{emailError}</div>}

          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ borderColor: password ? getPasswordStrengthColor() : '' }}
          />
          {password && (
            <div className={`password-strength ${getPasswordStrengthColor()}`}>
              {getPasswordStrengthColor() === 'red' && 'Weak - minimum 8 characters'}
              {getPasswordStrengthColor() === 'yellow' && 'Medium - minimum 1 special character'}
              {getPasswordStrengthColor() === 'green' && 'Strong'}
            </div>
          )}
          {passwordError && <div className="error-message">{passwordError}</div>}

          <button
            className={`signup__button ${signupSuccess ? 'success' : ''}`}
            onClick={handleSignup}
            disabled={signupSuccess}
            style={{
              backgroundColor: signupSuccess?'green':'',
              fontSize: signupSuccess ? 'small' : '', // Apply smaller font size only when successful
            }}
          >
            {signupSuccess ? 'Successful' : 'Signup'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Signup;
