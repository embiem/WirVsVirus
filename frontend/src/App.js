import React from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import { Router } from '@reach/router';

import './App.css';
import Home from './Home';
import RegisterPage from './pages/Register/Register';
import ProfilePage from './pages/Profile/Profile';
import HospitalDashboardPage from './pages/Hospital/Dashboard';
import CreateInvitationPage from './pages/CreateInvitation/CreateInvitation';
import Header from './components/Header/Header';
import { useAuth0 } from './utils/react-auth0-spa';

function App() {
  const { loading } = useAuth0();

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <CssBaseline />
      <Header />

      <Router>
        <Home path="/" />
        <RegisterPage path="/register" />
        <ProfilePage path="/profile" />
        <HospitalDashboardPage path="/hospital" />
        <CreateInvitationPage path="/hospital/requirements" />
      </Router>
    </>
  );
}

export default App;
