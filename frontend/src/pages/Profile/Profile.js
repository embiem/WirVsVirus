import React, { Fragment } from 'react';
import {
  Container, Paper, Box, Avatar,
} from '@material-ui/core';
import { useAuth0 } from '../../utils/react-auth0-spa';
import useLoginRedirect from '../../utils/useLoginRedirect';

const Profile = () => {
  // Will redirect to login if not already authenticated
  useLoginRedirect();

  const { loading, user } = useAuth0();

  if (loading || !user) {
    return <div>Loading...</div>;
  }

  return (
        <Container >
        <Paper className="paper--content-wrapper" >
          <Box display="flex" flexDirection="column" alignItems="center">
            <Box>
              <Avatar alt={user.name} src={user.picture} />
            </Box>
              <h2>{user.name}</h2>
              <p>{user.email}</p>

          </Box>
        </Paper>
     </Container>

  );
};

export default Profile;
