from src.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

password = "FastAPI123"

hashed = hash_password(password)
print("Hashed Password:")
print(hashed)

print("\nPassword Verification:")
print(verify_password(password, hashed))

token = create_access_token(subject="manoj")

print("\nJWT Token:")
print(token)

print("\nDecoded Token:")
print(decode_access_token(token))