# Authorization utilities

import functools
from typing import Any, Dict, List, Optional

import requests
from authlib.jose import JWTClaims, jwt
from authlib.jose.errors import JoseError
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, ValidationError
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


class JWTPayload(BaseModel):
    iss: str
    sub: str
    aud: List[str] = []
    iat: int
    exp: int
    azp: str = ""
    scope: str = ""
    token: str = ""  # original jwt token

    @property
    def scopes(self) -> List[str]:
        """Scopes as list."""
        [s.strip() for s in self.scope.split(" ")]


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
            payload = jwt.decode(
                token,
                self.jwks.keys,
                claims_options={"iss": {"value": settings.auth_issuer}},
            )
            payload.validate()
        except JoseError as e:
            breakpoint()
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=e.args[0])

        return payload

    async def __call__(self, request: Request) -> JWTPayload:  # type: ignore
        if not settings.auth_enabled:
            return JWTPayload(sub="noone", iss="noone", iat=0, exp=0)
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        token = credentials.credentials
        payload = self.decode_jwt(token)
        try:
            return JWTPayload(**payload, token=token)
        except ValidationError as e:
            breakpoint()
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail=f"Invalid jwt: {e.args[0]}"
            )


class UserInfo(BaseModel):
    """User info model based on auth0 userinfo response.

    See: https://auth0.com/docs/api/authentication?http#get-user-info
    """

    sub: str
    email: str
    email_verified: bool = False
    phone_number: Optional[str]
    locale: Optional[str]
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    middle_name: Optional[str]


async def get_user_info(token: str):
    """Obtain userinfo from auth0 given an access token."""
    response = requests.get(
        settings.auth_issuer + "userinfo", headers={"Authorization": f"Bearer {token}"}
    )
    user_info = UserInfo.parse_obj(response.json())
    return user_info


auth = Auth()
