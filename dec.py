from cryptography.fernet import Fernet

# Load the Fernet key (must be the SAME key used for encryption)
key = "sXNET5eRc7oPXUirMSOgd6F78f-z1aacBxmQZYtoIts="

fernet = Fernet(key)

# Read encrypted .env file
with open(".env.enc", "rb") as enc_file:
    encrypted_data = enc_file.read()

# Decrypt
decrypted_data = fernet.decrypt(encrypted_data)

# Write decrypted env file
with open(".env", "wb") as env_file:
    env_file.write(decrypted_data)

print("✅ Decryption successful. .env restored.")
