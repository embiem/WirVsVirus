import React from 'react';
import ReactDOM from 'react-dom';
import { ApolloProvider } from '@apollo/react-hooks';
import { navigate } from '@reach/router';

import './index.tailwind.css';
import { Auth0Provider } from './utils/react-auth0-spa';
import apolloClient from './graphql/apolloClient';
import config from './config/auth_config.json';
import './styles/styles.scss';
import App from './App';
import * as serviceWorker from './serviceWorker';

// A function that routes the user to the right place
// after login
const onRedirectCallback = (appState) => {
  navigate(appState && appState.targetUrl ? appState.targetUrl : window.location.pathname);
};

ReactDOM.render(
  <ApolloProvider client={apolloClient}>
    <Auth0Provider
      domain={config.domain}
      client_id={config.clientId}
      audience={config.audience}
      redirect_uri={window.location.origin}
      onRedirectCallback={onRedirectCallback}
    >
      <App />
    </Auth0Provider>
  </ApolloProvider>,
  document.getElementById('root'),
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
