import React, { useEffect, useState } from 'react';
import {
  Container, Button, Paper, Box, Avatar,
} from '@material-ui/core';
import { Link as RouterLink } from '@reach/router';
import axios from 'axios';
import { useAuth0 } from '../../utils/react-auth0-spa';
import useLoginRedirect from '../../utils/useLoginRedirect';

const Proceed = ({ profileType }) => {
  if (profileType === 'helper') {
    return <div>
        Du bist ein Helfer.
        <RouterLink to="/register">Hier</RouterLink> kannst Du Dein Profil verändern
      </div>;
  } if (profileType === 'hospital') {
    return <div>
        Du suchst als Krankenhausmitarbeiter nach Hilfe.
        Suche <RouterLink to="/hospital">hier</RouterLink> nach Helfern.
      </div>;
  }
  return '';
};
const Profile = () => {
  useLoginRedirect();
  const { user } = useAuth0();

  const [profileType, setProfileType] = useState(null);

  useEffect(() => {
    (async () => {
    // todo: this should be a custom hook.
      const Axios = axios.create({
        baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
        headers: {
          Authorization: document.auth_token ? `Bearer ${document.auth_token}` : '',
        },
      });
      try {
        const res = await Axios.get('/profile');
        console.log(res);
        setProfileType(res.data.profileType);
      } catch (e) {
        console.log(e);
      }
    })();
  });


  return (
        <Container >
        <Paper className="paper--content-wrapper" >
          <Box display="flex" flexDirection="column" alignItems="center">
            <Box>
              <Avatar alt={user.name} src={user.picture} />
            </Box>
              <h2>{user.name}</h2>
              <p>{user.email}</p>
              {profileType}
              { !profileType ? <Button to="/register" component={RouterLink}>registrieren</Button>
                : <Proceed profileType={profileType} />
  }
          </Box>
        </Paper>
     </Container>

  );
};

export default Profile;
