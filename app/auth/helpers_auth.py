import bcrypt


def hash_pwd(password: str) -> bytes:
    salt = bcrypt.gensalt()
    bytes_password: bytes = password.encode()
    return bcrypt.hashpw(
        password=bytes_password,
        salt=salt,
    )


def verify_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
