# Authorization utilities

import functools
from typing import Any, Dict, List, Optional

import requests
from authlib.jose import JWTClaims, jwt
from authlib.jose.errors import JoseError
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from wirvsvirus.settings import settings
from wirvsvirus import db, models, crud

JWK = Dict[str, Any]


class JWKS(BaseModel):
    keys: List[JWK] = []


class JWTAuthorizationCredentials(BaseModel):
    jwt_token: str
    header: Dict[str, str]
    claims: Dict[str, str]
    signature: str
    message: str


@functools.lru_cache()
def get_jwks() -> JWKS:
    """Get JSON Web Key Set from auth settings.

    More information: https://auth0.com/docs/tokens/concepts/jwks
    """
    response = requests.get(settings.auth_jwks_uri, timeout=10)
    response.raise_for_status()
    response_json = response.json()
    return JWKS(**response_json)


class Auth(HTTPBearer):
    """Authorization header jwt bearer handler.

    This can be used as a dependency and will verify that an http bearer token
    is signed by the correct authority.
    """

    @functools.cached_property
    def jwks(self) -> JWKS:
        """Get json web key set."""
        return get_jwks()

    @functools.cached_property
    def kid_to_jwk(self) -> Dict[str, JWK]:
        """Map key ids to json web key."""
        return {jwk["kid"]: jwk for jwk in self.jwks.keys if jwk.get("kid")}

    def decode_jwt(self, token: str) -> JWTClaims:
        """Verify jwt."""
        try:
            payload = jwt.decode(token, self.jwks.keys, claims_options={"iss": {"value": settings.auth_issuer}})
            payload.validate()
        except JoseError as e:
            breakpoint()
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=e.args[0])

        return payload

    async def __call__(self, request: Request) -> Optional[dict]:
        if not settings.auth_enabled:
            return {}
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        token = credentials.credentials
        payload = self.decode_jwt(token)


auth = Auth()


async def current_profile(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer), jwt_payload: dict = Depends(auth)) -> models.Profile:
    """Get current profile.

    If a profile is not available, create one.
    """
    user_id = jwt_payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail='Invalid token payload. Must have valid user id')
    profiles = db.get_database().profiles
    result = await profiles.find_one({'user_id': jwt_payload['sub']})

    if result:
        profile = models.Profile(**result)
    else:
        token = credentials.credentials
        # TODO: replace with httpx if too slow, as not async
        response = requests.get(settings.auth_issuer + 'userinfo', headers={'Authorization': f'Bearer {token}'})
        user_info = response.json()
        if not user_info.get('email_verified'):
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                                detail='Email not verified.')
        base_profile = models.BaseProfile(user_id=user_id, email=user_info['email'])
        created = crud.create_item('profiles', base_profile)
        profile = models.Profile(**created)

    return profile
