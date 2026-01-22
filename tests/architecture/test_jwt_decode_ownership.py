"""
This ensures:

- get_current_user cannot import jose.jwt directly.
- Any new auth dependency must use decode_access_token.
- Architecture remains consistent over time.
"""
import pathlib

AUTH_PATH = pathlib.Path("app/core/auth.py")
JWT_PATH = pathlib.Path("app/core/jwt.py")

FORBIDDEN = (
    "jose.jwt",
    "jwt.decode",
)

def test_auth_does_not_decode_jwt_directly():
    content = AUTH_PATH.read_text()
    for token in FORBIDDEN:
        assert token not in content, (
            f"{AUTH_PATH} decodes JWT directly! "
            "Use decode_access_token from core/jwt.py"
        )
