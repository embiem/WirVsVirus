import React from "react";
import CssBaseline from "@material-ui/core/CssBaseline";
import { Router } from "@reach/router";

import Home from "./Home";
import "./App.css";
import RegisterPage from './pages/Register/Register';

function App() {
  return (
    <>
      <CssBaseline />
      <Router>
        <Home path="/" />
        <RegisterPage path="/register" />
      </Router>
    </>
  );
}

export default App;
