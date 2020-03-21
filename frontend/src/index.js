import React from 'react';
import ReactDOM from 'react-dom';
import ApolloClient from 'apollo-boost';
import { ApolloProvider } from '@apollo/react-hooks';

import './styles/styles.scss';
import App from './App';
import * as serviceWorker from './serviceWorker';

const GRAPHQL_URL = process.env.GRAPHQL_URL || 'http://localhost:9002/graphql';

const client = new ApolloClient({
  uri: GRAPHQL_URL,
});

ReactDOM.render(
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>,
  document.getElementById('root'),
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
