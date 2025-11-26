#!/usr/bin/env python3

def validate_key(key):
    try:
        key_int = int(key)
        return 1 <= key_int <= 25
    except (ValueError, TypeError):
        return False

def validate_text(text):
    for char in text:
        if not char.isalpha():
            return False
    return True

def preprocess_text(text):
    return text.upper().replace(' ', '')

def letter_to_number(letter):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return alphabet.index(letter)

def number_to_letter(number):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return alphabet[number % 26]

def encrypt_caesar(plaintext, key):
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            letter_num = letter_to_number(char)
            encrypted_num = (letter_num + key) % 26
            ciphertext += number_to_letter(encrypted_num)
    return ciphertext

def decrypt_caesar(ciphertext, key):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            letter_num = letter_to_number(char)
            decrypted_num = (letter_num - key) % 26
            plaintext += number_to_letter(decrypted_num)
    return plaintext

def get_operation():
    while True:
        print("\nChoose an operation:")
        print("1. Encrypt")
        print("2. Decrypt")
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice == '1':
            return 'encrypt'
        elif choice == '2':
            return 'decrypt'
        else:
            print("Invalid choice. Please enter 1 for encrypt or 2 for decrypt.")

def get_key():
    while True:
        key_input = input("Enter the key (1-25): ").strip()
        if validate_key(key_input):
            return int(key_input)
        else:
            print("Invalid key. Please enter a number between 1 and 25 inclusive.")

def get_text(operation):
    text_type = "message" if operation == 'encrypt' else "ciphertext"
    while True:
        text = input(f"Enter the {text_type}: ").strip()
        if not text:
            print(f"Please enter a {text_type}.")
            continue
        processed_text = preprocess_text(text)
        if not processed_text:
            print("Please enter text that contains at least some letters.")
            continue
        if validate_text(processed_text):
            return processed_text
        else:
            print("Invalid characters. Please enter only letters (A-Z or a-z).")

def main():
    print("=" * 50)
    print("Caesar Cipher Implementation - Task 1")
    print("=" * 50)
    try:
        while True:
            operation = get_operation()
            key = get_key()
            text = get_text(operation)
            if operation == 'encrypt':
                result = encrypt_caesar(text, key)
                print(f"\nEncrypted ciphertext: {result}")
            else:
                result = decrypt_caesar(text, key)
                print(f"\nDecrypted plaintext: {result}")
            while True:
                continue_choice = input("\nDo you want to perform another operation? (y/n): ").strip().lower()
                if continue_choice in ['y', 'yes']:
                    break
                elif continue_choice in ['n', 'no']:
                    print("Thank you for using the Caesar Cipher!")
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
