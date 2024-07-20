import React, { useState } from 'react';
import { registerUser } from "../../services/user";

const UserRegister = ({ onRegistrationSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [errors, setErrors] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await registerUser(username, password, passwordConfirm);
      setMessage('Registration successful!');
      setUsername('');
      setPassword('');
      setPasswordConfirm('');
      setError('');
      setErrors('');
      onRegistrationSuccess();
    } catch (err) {
      setErrors(err.response.data);
      setError('Registration failed. Please try again.');
      setMessage('');
    }
  };

  return (
    <div className="register-container">
      <h1>Register</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          {errors.username && errors.username.map((error, index) => (
            <li key={index} style={{ color: 'red' }}>{error}</li>
          ))}
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {errors.password && errors.password.map((error, index) => (
            <li key={index} style={{ color: 'red' }}>{error}</li>
          ))}
        </div>
        <div>
          <label htmlFor="passwordConfirm">Confirm Password:</label>
          <input
            type="password"
            id="passwordConfirm"
            value={passwordConfirm}
            onChange={(e) => setPasswordConfirm(e.target.value)}
            required
          />
          {errors.password_confirm && errors.password_confirm.map((error, index) => (
            <li key={index} style={{ color: 'red' }}>{error}</li>
          ))}
        </div>
        <button type="submit">Register</button>
      </form>
      {message && <p>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default UserRegister;
