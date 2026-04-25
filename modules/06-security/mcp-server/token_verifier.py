import time

import jwt
from jwt import PyJWKClient
from mcp.server.auth.provider import AccessToken, TokenVerifier


class KeycloakTokenVerifier(TokenVerifier):
    """Validates JWTs issued by Keycloak using its JWKS endpoint."""

    def __init__(self, issuer_url: str, expected_audience: str) -> None:
        self.issuer_url = issuer_url
        self.expected_audience = expected_audience
        jwks_uri = f"{issuer_url}/protocol/openid-connect/certs"
        self.jwks_client = PyJWKClient(jwks_uri)

    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            decoded = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.expected_audience,
                issuer=self.issuer_url,
                options={"require": ["exp", "iss", "aud"]},
            )

            if decoded.get("exp", 0) < time.time():
                return None

            scopes = decoded.get("scope", "").split() if isinstance(decoded.get("scope"), str) else []

            return AccessToken(
                token=token,
                client_id=decoded.get("azp", decoded.get("client_id", "")),
                scopes=scopes,
                expires_at=decoded.get("exp"),
            )
        except jwt.exceptions.PyJWTError:
            return None
