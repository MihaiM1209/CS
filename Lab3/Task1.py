#!/usr/bin/env python3

def validate_key(key):
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


def letter_to_number(letter):


    alphabet = "AĂÂBCDEFGHIÎJKLMNOPQRSTȘȚUVWXYZ"
    return alphabet.index(letter)


def number_to_letter(number):

    alphabet = "AĂÂBCDEFGHIÎJKLMNOPQRSTȘȚUVWXYZ"
    return alphabet[number % 31]


def encrypt_vigenere(plaintext, key):
    ciphertext = ""
    key_upper = key.upper()

    for i, char in enumerate(plaintext):
        if char.isalpha():

            key_char = key_upper[i % len(key_upper)]
            key_value = letter_to_number(key_char)


            letter_num = letter_to_number(char)

            encrypted_num = (letter_num + key_value) % 31

            ciphertext += number_to_letter(encrypted_num)
    return ciphertext


def decrypt_vigenere(ciphertext, key):
    plaintext = ""
    key_upper = key.upper()

    for i, char in enumerate(ciphertext):
        if char.isalpha():

            key_char = key_upper[i % len(key_upper)]
            key_value = letter_to_number(key_char)


            letter_num = letter_to_number(char)

            decrypted_num = (letter_num - key_value) % 31

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
        key_input = input("Enter the key (minimum 7 characters, letters only): ").strip()

        if validate_key(key_input):
            return key_input
        else:
            print("Invalid key. Please enter at least 7 characters using only Romanian letters (A-Z, a-z).")


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
            print("Invalid characters. Please enter only Romanian letters (A-Z or a-z).")


def main():
    print("=" * 60)
    print("Vigenère Cipher Implementation for Romanian Language - Lab 3")
    print("=" * 60)
    print("Romanian alphabet (31 letters): A, Ă, Â, B, C, D, E, F, G, H, I, Î, J, K, L, M, N, O, P, Q, R, S, Ș, T, Ț, U, V, W, X, Y, Z")
    print("Letter encoding: A=0, Ă=1, Â=2, ..., Z=30")
    print("Key requirements: minimum 7 characters, letters only")

    try:
        while True:

            operation = get_operation()


            key = get_key()


            text = get_text(operation)


            if operation == 'encrypt':
                result = encrypt_vigenere(text, key)
                print(f"\nEncrypted ciphertext: {result}")
                print(f"Used key: '{key}'")
            else:
                result = decrypt_vigenere(text, key)
                print(f"\nDecrypted plaintext: {result}")
                print(f"Used key: '{key}'")


            while True:
                continue_choice = input("\nDo you want to perform another operation? (y/n): ").strip().lower()
                if continue_choice in ['y', 'yes']:
                    break
                elif continue_choice in ['n', 'no']:
                    print("Thank you for using the Romanian Vigenère Cipher!")
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()


