from sympy import randprime
from math import gcd

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

NTLM_HEX = "AE6BAA4ABE48DE6E65AA9E8DAF88AD8D"
h = int(NTLM_HEX, 16)

print(f"NTLM hash (hex): {NTLM_HEX}")
print(f"NTLM hash (decimal): {h}\n")

bits = 1536
while True:
    p = randprime(2**(bits - 1), 2**bits)
    q = randprime(2**(bits - 1), 2**bits)
    while p == q:
        q = randprime(2**(bits - 1), 2**bits)
    n = p * q
    if n.bit_length() >= 3072:
        break

phi_n = (p - 1) * (q - 1)
e = 65537
if gcd(e, phi_n) != 1:
    raise ValueError("e and phi(n) are not coprime")

d = modinv(e, phi_n)

print(f"RSA modulus n: {n.bit_length()} bits")
print(f"Public key (n, e): n with {n.bit_length()} bits, e = {e}")
print(f"Private key (d, n): d with {d.bit_length()} bits\n")

if h >= n:
    h = h % n

s = pow(h, d, n)
print(f"Signature: s = h^d mod n = {s}\n")

v = pow(s, e, n)
print(f"Verification: v = s^e mod n = {v}")
print(f"Expected h = {h}")
print("Result:", "SUCCESS" if v == h else "FAILED")
