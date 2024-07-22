import React, {useState} from 'react';
import AuthPanel from "./components/auth/AuthPanel";
import BudgetPanel from "./components/budget/BudgetPanel";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  return (
    <div className="App">
      <AuthPanel isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn}/>
      {isLoggedIn && (
        <BudgetPanel/>
      )}
    </div>
  );
}

export default App;
