from app.encryption import encrypt, decrypt

phone = "9876543210"

encrypted = encrypt(phone)
print("Encrypted:", encrypted)

decrypted = decrypt(encrypted)
print("Decrypted:", decrypted)