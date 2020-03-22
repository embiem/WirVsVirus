import React from 'react';
import { Link, Redirect } from '@reach/router';

import {
  Container, Paper, Button, Box,
} from '@material-ui/core';
import { useAuth0 } from './utils/react-auth0-spa';

export default function Home() {
  const { isAuthenticated, loginWithRedirect } = useAuth0();

  // {isAuthenticated ? <Redirect to="/profile" /> :
  if (isAuthenticated) return <Redirect to="/profile" />;

  return <div className="py center-vertical">
    <Container >
        <Paper className="paper--content-wrapper" >
            <Box display="flex" justifyContent="center">
              <Button variant="contained" size="large" color="primary" onClick={() => loginWithRedirect()}>
              Anmelden
              </Button>
            </Box>
        </Paper>
     </Container>
     </div>;
}
