from src.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "FastAPI123"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True


def test_password_verification_fails_for_wrong_password():
    password = "FastAPI123"
    wrong_password = "WrongPassword123"

    hashed = hash_password(password)

    assert verify_password(wrong_password, hashed) is False


def test_create_and_decode_access_token():
    token = create_access_token(
        subject="manoj",
        role="user",
    )

    assert token is not None
    assert isinstance(token, str)

    payload = decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == "manoj"
    assert payload["role"] == "user"