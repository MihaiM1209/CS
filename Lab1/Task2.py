#!/usr/bin/env python3
import string

STANDARD_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def validate_key1(key):
    try:
        key_int = int(key)
        return 1 <= key_int <= 25
    except (ValueError, TypeError):
        return False

def validate_key2(key):
    if len(key) < 7:
        return False
    for char in key:
        if not char.isalpha():
            return False
    return True

def validate_text(text):
    for char in text:
        if not char.isalpha():
            return False
    return True

def preprocess_text(text):
    return text.upper().replace(' ', '')

def generate_permuted_alphabet(key2):
    key2_upper = key2.upper()
    permuted_part = ""
    for char in key2_upper:
        if char not in permuted_part:
            permuted_part += char
    remaining_part = ""
    for char in STANDARD_ALPHABET:
        if char not in permuted_part:
            remaining_part += char
    return permuted_part + remaining_part

def permuted_letter_to_number(letter, permuted_alphabet):
    return permuted_alphabet.index(letter)

def permuted_number_to_letter(number, permuted_alphabet):
    return permuted_alphabet[number % 26]

def encrypt_caesar_2keys(plaintext, key1, permuted_alphabet):
    ciphertext = ""
    for char in plaintext:
        letter_num = permuted_letter_to_number(char, permuted_alphabet)
        encrypted_num = (letter_num + key1) % 26
        ciphertext += permuted_number_to_letter(encrypted_num, permuted_alphabet)
    return ciphertext

def decrypt_caesar_2keys(ciphertext, key1, permuted_alphabet):
    plaintext = ""
    for char in ciphertext:
        letter_num = permuted_letter_to_number(char, permuted_alphabet)
        decrypted_num = (letter_num - key1) % 26
        plaintext += permuted_number_to_letter(decrypted_num, permuted_alphabet)
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

def get_key1():
    while True:
        key_input = input("Enter key 1 (Caesar Shift: 1-25): ").strip()
        if validate_key1(key_input):
            return int(key_input)
        else:
            print("Invalid key 1. Please enter a number between 1 and 25 inclusive.")

def get_key2():
    while True:
        key_input = input("Enter key 2 (Permutation Keyword: min 7 letters): ").strip()
        if validate_key2(key_input):
            return key_input
        else:
            print("Invalid key 2. Please enter only Latin letters with at least 7 characters.")

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
    print("=" * 60)
    print("Caesar Cipher with Permutation Implementation - Task 2")
    print("=" * 60)
    try:
        while True:
            operation = get_operation()
            print("\nEnter the keys:")
            key1 = get_key1()
            key2 = get_key2()
            permuted_alphabet = generate_permuted_alphabet(key2)
            print(f"\nPermuted Alphabet (k2='{key2}'): {permuted_alphabet}")
            text = get_text(operation)
            if operation == 'encrypt':
                result = encrypt_caesar_2keys(text, key1, permuted_alphabet)
                print(f"\nEncrypted ciphertext: {result}")
                print(f"Used keys: Caesar Shift (k1)={key1}, Keyword (k2)='{key2}'")
            else:
                result = decrypt_caesar_2keys(text, key1, permuted_alphabet)
                print(f"\nDecrypted plaintext: {result}")
                print(f"Used keys: Caesar Shift (k1)={key1}, Keyword (k2)='{key2}'")
            while True:
                continue_choice = input("\nDo you want to perform another operation? (y/n): ").strip().lower()
                if continue_choice in ['y', 'yes']:
                    break
                elif continue_choice in ['n', 'no']:
                    print("Thank you for using the Caesar Cipher with Permutation!")
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
