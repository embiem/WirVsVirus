import React from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import { Router } from '@reach/router';

import './App.css';

import Header from './components/Header/Header';
import Home from './Home';
import RegisterPage from './pages/Register/Register';
import CreateInvitationPage from './pages/CreateInvitation/CreateInvitation';

function App() {
  return (
    <>
      <CssBaseline />
      <Header />

      <Router>
        <Home path="/" />
        <RegisterPage path="/register" />
        <CreateInvitationPage path="/hospital/create-invitation" />
      </Router>
    </>
  );
}

export default App;
