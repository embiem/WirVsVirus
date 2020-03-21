import React from "react";
import CssBaseline from "@material-ui/core/CssBaseline";
import { Router } from "@reach/router";

import Home from "./Home";
import SignIn from "./auth/SignIn";
import SignUp from "./auth/SignUp";
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
