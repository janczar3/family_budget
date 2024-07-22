import React, {useState} from 'react';
import AuthPanel from "./components/auth/AuthPanel";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  return (
    <div className="App">
      <AuthPanel isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn}/>
    </div>
  );
}

export default App;
