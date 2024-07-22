import UserRegisterForm from './forms/UserRegisterForm';
import UserLoginForm from "./forms/UserLoginForm";
import { logoutUser } from "../../services/auth";
import React, { useEffect, useState } from 'react';
import { checkIfLoggedIn} from "../../services/auth";

function UserPanel () {
  const [showRegistrationForm, setShowRegistrationForm] = useState(false);
  const [showLoginForm, setShowLoginForm] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [error, setError] = useState('');
  const [user, setUser] = useState(null);

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
      setIsLoggedIn(false);
    } catch (err) {
      setError('Logout failed!');
    }
  };

  useEffect(() => {
    const verifyUser = async () => {
      const userData = await checkIfLoggedIn();
      if (userData) {
        setIsLoggedIn(true);
        setUser(userData);
      }
    };
    verifyUser();
  }, []);

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
      {showRegistrationForm && <UserRegisterForm onRegistrationSuccess={onRegistrationSuccess}/>}
      {showLoginForm && <UserLoginForm onLoginSuccess={onLoginSuccess}/>}
    </div>
  )
}

export default UserPanel;