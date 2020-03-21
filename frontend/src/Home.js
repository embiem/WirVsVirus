import React from "react";
import { Link } from "@reach/router";
import { useQuery } from "@apollo/react-hooks";
import { gql } from "apollo-boost";

import { useAuth0 } from "./utils/react-auth0-spa";

const TEST_QUERY = gql`
  {
    hospital(id: "test") {
      id
      name
      address {
        zipCode
        street
        latitude
        longitude
      }
      email
      website
      phone
    }
  }
`;

export default function Home() {
  const { loading, error, data } = useQuery(TEST_QUERY);

  const { isAuthenticated, loginWithRedirect, logout } = useAuth0();

  return (
    <div>
      <h1>Home</h1>
      <Link to="/profile">Profile</Link>
      <pre>{JSON.stringify(data, null, 2)}</pre>
      <div>
        {!isAuthenticated && (
          <button onClick={() => loginWithRedirect({})}>Log in</button>
        )}

        {isAuthenticated && <button onClick={() => logout()}>Abmelden</button>}
      </div>
    </div>
  );
}
