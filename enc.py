"""
Encryption utility for .env file
"""

from cryptography.fernet import Fernet

def encrypt_env_file():
    """Encrypt the .env file using Fernet encryption"""
    
    # The encryption key
    key = "sXNET5eRc7oPXUirMSOgd6F78f-z1aacBxmQZYtoIts="
    
    # Initialize Fernet cipher
    fernet = Fernet(key.encode())
    
    # Read the .env file
    try:
        with open(".env", "rb") as f:
            env_data = f.read()
        print("✓ .env file read successfully")
    except FileNotFoundError:
        print("✗ .env file not found")
        return False
    
    # Encrypt the data
    encrypted_data = fernet.encrypt(env_data)
    print("✓ .env file encrypted successfully")
    
    # Write the encrypted data to .env.enc
    try:
        with open(".env.enc", "wb") as f:
            f.write(encrypted_data)
        print("✓ Encrypted file saved as .env.enc")
    except Exception as e:
        print(f"✗ Error saving encrypted file: {str(e)}")
        return False
    
    print("\n✅ Encryption completed successfully!")
    print("You can now use the .env.enc file with the decrypt function in main.py")
    return True


if __name__ == "__main__":
    encrypt_env_file()
