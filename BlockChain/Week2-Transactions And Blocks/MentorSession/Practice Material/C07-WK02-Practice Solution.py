from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# Define private and public key of Bob and Alice
Bob_private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=2048)
Bob_public_key = Bob_private_key.public_key()

Alice_private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=2048)
Alice_public_key = Alice_private_key.public_key()

# Encrypt message for Bob
secret_message = 'This is a secret message for Bob.'
print(secret_message)
encrypted_message_for_Bob = Bob_public_key.encrypt(
    secret_message.encode(),
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                 algorithm=hashes.SHA256(), label=None))

# Sign the message
signature = Alice_private_key.sign(
    encrypted_message_for_Bob,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256())

# Verify the signature
result = Alice_public_key.verify(
    signature,
    encrypted_message_for_Bob,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256())

# Decrypt the message
decrypted_message_for_Bob = Bob_private_key.decrypt(
    encrypted_message_for_Bob,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                 algorithm=hashes.SHA256(), label=None))

print(decrypted_message_for_Bob)
