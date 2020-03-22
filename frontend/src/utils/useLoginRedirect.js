import { useEffect } from 'react';
import { useAuth0 } from './react-auth0-spa';

export default function () {
  const { loading, isAuthenticated, loginWithRedirect } = useAuth0();

  useEffect(() => {
    if (loading || isAuthenticated) {
      return;
    }
    (async () => {
      await loginWithRedirect({
        appState: { targetUrl: window.location.pathname },
      });
    })();
  }, [loading, isAuthenticated, loginWithRedirect]);
}
