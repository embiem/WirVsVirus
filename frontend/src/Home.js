import React, { Component } from "react";
import { useQuery } from "@apollo/react-hooks";
import { gql } from "apollo-boost";

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

  return (
    <div>
      <h1>Home</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
