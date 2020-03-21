import React from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import { Router } from '@reach/router';

import './App.css';
import Home from './Home';
import RegisterPage from './pages/Register/Register';
import ProfilePage from './pages/Profile/Profile';
import SearchPage from './pages/Search/Search';
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
        <SearchPage path="/hospital/search" />
        <CreateInvitationPage path="/hospital/create-invitation" />
      </Router>
    </>
  );
}

export default App;
