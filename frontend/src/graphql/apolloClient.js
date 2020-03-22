import ApolloClient from 'apollo-boost';

const GRAPHQL_URL = process.env.REACT_APP_GRAPHQL_URL || 'http://localhost:9002/graphql';

const client = new ApolloClient({
  uri: GRAPHQL_URL,
  request: (operation) => {
    operation.setContext({
      headers: {
        Authorization: document.auth_token ? `Bearer ${document.auth_token}` : '',
      },
    });
  },
});

export default client;
