"""Utility functions for encrypting and decrypting sensitive data."""

from cryptography.fernet import Fernet

from app.config import AES_KEY

cipher = Fernet(AES_KEY.encode())


def encrypt(text: str) -> str:
    """Encrypt a string and return the encrypted text."""
    return cipher.encrypt(text.encode()).decode()


def decrypt(cipher_text: str) -> str:
    """Decrypt an encrypted string and return the original text."""
    return cipher.decrypt(cipher_text.encode()).decode()