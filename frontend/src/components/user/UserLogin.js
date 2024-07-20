import React, { useState } from 'react';
import { loginUser} from "../../services/user";

const UserLogin = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [errors, setErrors] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await loginUser(username, password);
      setUsername('');
      setPassword('');
      setError('');
      setErrors('');
      setMessage('Login successful!');
      onLoginSuccess();
    } catch (err) {
      setErrors(err.response.data);
      setError('Login failed. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Username</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        {errors.username && errors.username.map((error, index) => (
            <li key={index} style={{ color: 'red' }}>{error}</li>
          ))}
      </div>
      <div>
        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {errors.password && errors.password.map((error, index) => (
          <li key={index} style={{ color: 'red' }}>{error}</li>
        ))}
      </div>
      {message && <p>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="submit">Login</button>
    </form>
  );
};

export default UserLogin;
