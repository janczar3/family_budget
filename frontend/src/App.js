import React, { useEffect, useState } from 'react';
import api from './api';
import UserRegister from './UserRegister';

function App() {
  const [message, setMessage] = useState('');
  const [showRegistrationForm, setShowRegistrationForm] = useState(false);

  const toggleRegistrationForm = () => {
    setShowRegistrationForm(!showRegistrationForm);
  };

  useEffect(() => {
    api.get('example/')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error("There was an error fetching the data!", error);
      });
  }, []);

  return (
    <div className="App">
      <nav>
        <ul>
          <li>
            <a href="#" onClick={toggleRegistrationForm}>
              Register
            </a>
          </li>
          {/* Inne linki do menu */}
        </ul>
      </nav>

      {showRegistrationForm && <UserRegister/>}
    </div>
  );
}

export default App;
