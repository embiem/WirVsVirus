import React from "react";
import CssBaseline from "@material-ui/core/CssBaseline";
import { Router, Link } from "@reach/router";

import Home from './Home'
import SignIn from './SignIn'
import SignUp from './SignUp'
import "./App.css";

function App() {
  return (
    <>
      <CssBaseline />
      <Router>
        <Home path="/" />
        <SignIn path="/login" />
        <SignUp path="/signup" />
      </Router>
    </>
  );
}

export default App;
