import bcrypt

USER_DATA = {
    "user1": 
}

def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

print(hash_password("hello.123"))

# $2b$12$v8pWrE/tE0QHbUr2xASq7OaxChjcauomapTXRleSHNy1kK3HG6KZi

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )

passw = hash_password("hello.123")
print(verify_password("hello.23", passw))