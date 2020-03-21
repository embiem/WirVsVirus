import ApolloClient from "apollo-boost";

const GRAPHQL_URL = process.env.GRAPHQL_URL || "http://localhost:9002/graphql";

const client = new ApolloClient({
  uri: GRAPHQL_URL,
  request: operation => {
    operation.setContext({
      headers: {
        Authorization: document.auth_token
          ? `Bearer ${document.auth_token}`
          : ""
      }
    });
  }
});

export default client;
