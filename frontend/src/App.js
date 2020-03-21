import React from "react";
import CssBaseline from "@material-ui/core/CssBaseline";
import { Router } from "@reach/router";

import Home from "./Home";
import "./App.css";
import RegisterPage from "./pages/Register/Register";
import ProfilePage from "./pages/Profile/Profile";
import { useAuth0 } from "./utils/react-auth0-spa";

function App() {
  const { loading } = useAuth0();

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <CssBaseline />
      <Router>
        <Home path="/" />
        <RegisterPage path="/register" />
        <ProfilePage path="/profile" />
      </Router>
    </>
  );
}

export default App;
