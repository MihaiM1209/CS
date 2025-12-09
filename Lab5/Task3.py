#!/usr/bin/env python3

import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes



P = 32317006071311007300153513477825163362488057133489075174588434139269806834136210002792056362640164685458556357935330816928829023080573472625273554742461245741026202527916572972862706300325263428213145766931414223654220941111348629991657478268034230553086349050635557712219187890332729569696129743856241741236237225197346402691855797767976823014625397933058015226858730761197532436467475855460715043896844940366130497697812854295958659597567051283852132784468522925504568272879113720098931873959143374175837826000278034973198552060607533234122603254684088120031105907484281003994966956119696956248629032338072839127039
G = 2


def generate_diffie_hellman_secret(p):


    min_bits = 256
    max_bits = min(p.bit_length() - 1, 512)


    secret_bits = random.randint(min_bits, max_bits)
    secret_min = 2**(secret_bits - 1)
    secret_max = min(2**secret_bits - 1, p - 2)

    secret = random.randint(secret_min, secret_max)
    return secret


def diffie_hellman_key_exchange(p, g):
    print("\n" + "=" * 80)
    print("DIFFIE-HELLMAN KEY EXCHANGE")
    print("=" * 80)

    print(f"\nGiven parameters:")
    print(f"  p = {p}")
    print(f"  p has {p.bit_length()} bits")
    print(f"  g = {g} (generator)")


    print("\n" + "=" * 80)
    print("ALICE's SIDE")
    print("=" * 80)

    print("\nStep 1: Alice chooses secret a (randomly)")
    a = generate_diffie_hellman_secret(p)
    print(f"  Selected secret a = {a}")
    print(f"  Verification: 1 < {a} < {p-1} ✓")
    print(f"  a has {a.bit_length()} bits")

    print("\nStep 2: Alice calculates A = g^a (mod p)")
    print(f"  A = {g}^{a} mod {p}")
    A = pow(g, a, p)
    print(f"  A = {A}")

    print("\nStep 3: Alice sends A to Bob")
    print(f"  Public value A = {A}")


    print("\n" + "=" * 80)
    print("BOB's SIDE")
    print("=" * 80)

    print("\nStep 1: Bob chooses secret b (randomly)")
    b = generate_diffie_hellman_secret(p)
    print(f"  Selected secret b = {b}")
    print(f"  Verification: 1 < {b} < {p-1} ✓")
    print(f"  b has {b.bit_length()} bits")

    print("\nStep 2: Bob calculates B = g^b (mod p)")
    print(f"  B = {g}^{b} mod {p}")
    B = pow(g, b, p)
    print(f"  B = {B}")

    print("\nStep 3: Bob sends B to Alice")
    print(f"  Public value B = {B}")


    print("\n" + "=" * 80)
    print("SHARED SECRET CALCULATION")
    print("=" * 80)

    print("\nAlice calculates: K = B^a (mod p)")
    print(f"  K = {B}^{a} mod {p}")
    K_alice = pow(B, a, p)
    print(f"  K (Alice) = {K_alice}")

    print("\nBob calculates: K = A^b (mod p)")
    print(f"  K = {A}^{b} mod {p}")
    K_bob = pow(A, b, p)
    print(f"  K (Bob) = {K_bob}")


    if K_alice == K_bob:
        print(f"\n✓ Shared secret matches! K = {K_alice}")
    else:
        print(f"\n✗ ERROR: Shared secrets do not match!")
        print(f"  Alice's K: {K_alice}")
        print(f"  Bob's K: {K_bob}")

    shared_secret = K_alice

    return {
        'p': p,
        'g': g,
        'a': a,
        'b': b,
        'A': A,
        'B': B,
        'shared_secret': shared_secret
    }


def derive_aes_key(shared_secret, key_size_bytes=32):
    print("\n" + "=" * 80)
    print("AES KEY DERIVATION")
    print("=" * 80)

    print(f"\nShared secret: K = {shared_secret}")
    print(f"Shared secret (hex): {hex(shared_secret)}")


    secret_bytes = shared_secret.to_bytes((shared_secret.bit_length() + 7) // 8, 'big')
    print(f"\nShared secret as bytes: {secret_bytes.hex()}")


    print(f"\nDeriving AES-256 key using SHA-256 hash")
    print(f"  SHA-256(K)")
    aes_key = hashlib.sha256(secret_bytes).digest()

    print(f"\nAES-256 Key: {aes_key.hex()}")
    print(f"Key length: {len(aes_key)} bytes = {len(aes_key) * 8} bits")

    return aes_key


def aes_encrypt(plaintext, key):
    print("\n" + "=" * 80)
    print("AES-256 ENCRYPTION")
    print("=" * 80)

    print(f"\nPlaintext: {plaintext}")
    print(f"Plaintext (hex): {plaintext.hex()}")
    print(f"Plaintext length: {len(plaintext)} bytes")

    print(f"\nAES-256 Key: {key.hex()}")
    print(f"Key length: {len(key)} bytes = {len(key) * 8} bits")



    iv = get_random_bytes(16)
    print(f"\nGenerated IV (Initialization Vector): {iv.hex()}")
    print(f"IV length: {len(iv)} bytes = {len(iv) * 8} bits")


    cipher = AES.new(key, AES.MODE_CBC, iv)


    print(f"\nPadding plaintext to AES block size (16 bytes)")
    padded_plaintext = pad(plaintext, AES.block_size)
    print(f"Padded plaintext length: {len(padded_plaintext)} bytes")
    print(f"Padded plaintext (hex): {padded_plaintext.hex()}")


    print(f"\nEncrypting with AES-256-CBC...")
    ciphertext = cipher.encrypt(padded_plaintext)

    print(f"\nCiphertext: {ciphertext.hex()}")
    print(f"Ciphertext length: {len(ciphertext)} bytes")

    return ciphertext, iv


def aes_decrypt(ciphertext, key, iv):
    print("\n" + "=" * 80)
    print("AES-256 DECRYPTION")
    print("=" * 80)

    print(f"\nCiphertext: {ciphertext.hex()}")
    print(f"Ciphertext length: {len(ciphertext)} bytes")

    print(f"\nAES-256 Key: {key.hex()}")
    print(f"Key length: {len(key)} bytes = {len(key) * 8} bits")

    print(f"\nIV (Initialization Vector): {iv.hex()}")
    print(f"IV length: {len(iv)} bytes = {len(iv) * 8} bits")


    cipher = AES.new(key, AES.MODE_CBC, iv)


    print(f"\nDecrypting with AES-256-CBC...")
    padded_plaintext = cipher.decrypt(ciphertext)

    print(f"Decrypted (padded) plaintext: {padded_plaintext.hex()}")
    print(f"Decrypted (padded) plaintext length: {len(padded_plaintext)} bytes")


    print(f"\nRemoving padding...")
    plaintext = unpad(padded_plaintext, AES.block_size)

    print(f"Plaintext: {plaintext}")
    print(f"Plaintext (hex): {plaintext.hex()}")
    print(f"Plaintext length: {len(plaintext)} bytes")

    return plaintext


def main():
    print("=" * 80)
    print("DIFFIE-HELLMAN KEY EXCHANGE + AES ENCRYPTION - Lab 5, Task 3")
    print("=" * 80)
    print("Requirements:")
    print("- Perform Diffie-Hellman key exchange between Alice and Bob")
    print("- Use shared secret to derive AES-256 key")
    print("- Encrypt and decrypt message using AES-256")
    print("- Parameters: p (2048-bit) and g=2")
    print("- Secret numbers a and b chosen randomly according to algorithm requirements")


    message_text = "Mustea Mihai"
    message_bytes = message_text.encode('utf-8')

    print(f"\nOriginal message: '{message_text}'")


    dh_result = diffie_hellman_key_exchange(P, G)

    a = dh_result['a']
    b = dh_result['b']
    A = dh_result['A']
    B = dh_result['B']
    shared_secret = dh_result['shared_secret']


    aes_key = derive_aes_key(shared_secret, key_size_bytes=32)


    ciphertext, iv = aes_encrypt(message_bytes, aes_key)


    decrypted_bytes = aes_decrypt(ciphertext, aes_key, iv)
    decrypted_text = decrypted_bytes.decode('utf-8')


    print("\n" + "=" * 80)
    print("VERIFICATION")
    print("=" * 80)
    print(f"Original message: '{message_text}'")
    print(f"Decrypted message: '{decrypted_text}'")

    if message_text == decrypted_text:
        print("✓ Decryption successful! Messages match.")
    else:
        print("✗ Decryption failed! Messages do not match.")


    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Message: '{message_text}'")
    print(f"\nDiffie-Hellman Parameters:")
    print(f"  Prime p: {P} ({P.bit_length()} bits)")
    print(f"  Generator g: {G}")
    print(f"  Alice's secret a: {a} ({a.bit_length()} bits)")
    print(f"  Bob's secret b: {b} ({b.bit_length()} bits)")
    print(f"  Alice's public value A: {A}")
    print(f"  Bob's public value B: {B}")
    print(f"  Shared secret K: {shared_secret}")
    print(f"\nAES Encryption:")
    print(f"  AES-256 Key: {aes_key.hex()}")
    print(f"  IV: {iv.hex()}")
    print(f"  Ciphertext: {ciphertext.hex()}")
    print(f"  Decrypted message: '{decrypted_text}'")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()

