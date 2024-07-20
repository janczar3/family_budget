import UserRegister from './UserRegister';
import UserLogin from "./UserLogin";
import {logoutUser} from "../../services/user";
import React, {useState} from "react";

function UserPanel () {
  const [showRegistrationForm, setShowRegistrationForm] = useState(false);
  const [showLoginForm, setShowLoginForm] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [error, setError] = useState('');

  const toggleRegistrationForm = () => {
    setShowRegistrationForm(!showRegistrationForm);
    setShowLoginForm(false);
  };

  const toggleLoginForm = () => {
    setShowLoginForm(!showLoginForm);
    setShowRegistrationForm(false);
  };

  const onRegistrationSuccess = () => {
    toggleRegistrationForm();
    toggleLoginForm();
  };

  const onLoginSuccess = () => {
    setIsLoggedIn(true);
    setShowLoginForm(false);
  };

  const logout = async () => {
    try {
      await logoutUser();
      setShowLoginForm(true);
      setShowRegistrationForm(true);
    } catch (err) {
      setError('Logout failed!');
    }
  };

  return (
    <div className="UserPanel">
      <nav>
        <ul>
          {!isLoggedIn && (
            <>
              <li>
                <a href="#" onClick={toggleRegistrationForm}>
                  Register
                </a>
              </li>
              <li>
                <a href="#" onClick={toggleLoginForm}>
                  Login
                </a>
              </li>
            </>
          )}
          {isLoggedIn && (
            <>
              <li>
                <a href="#" onClick={logout}>
                  Logout
                </a>
              </li>
              <p>TODO Budget data here</p>
            </>
          )}
        </ul>
      </nav>
      {error && <p style={{color: 'red'}}>{error}</p>}
      {showRegistrationForm && <UserRegister onRegistrationSuccess={onRegistrationSuccess}/>}
      {showLoginForm && <UserLogin onLoginSuccess={onLoginSuccess}/>}
    </div>
  )
}

export default UserPanel;