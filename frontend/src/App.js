import React from "react";
import CssBaseline from "@material-ui/core/CssBaseline";
import { Router } from "@reach/router";

import Home from "./Home";
import "./App.css";

function App() {
  return (
    <>
      <CssBaseline />
      <Router>
        <Home path="/" />
      </Router>
    </>
  );
}

export default App;
