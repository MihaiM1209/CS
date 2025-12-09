import secrets
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

p = 32317006071311007300153513477825163362488057133489075174588434139269806834136210002792056362640164685458556357935330816928829023080573472625273554742461245741026202527916572972862706300325263428213145766931414223654220941111348629991657478268034230553086349050635557712219187890332729569696129743856241741236237225197346402691855797767976823014625397933058015226858730761197532436467475855460715043896844940366130497697812854295958659597567051283852132784468522925504568272879113720098931873959143374175837826000278034973198552060607533234122603254684088120031105907484281003994966956119696956248629032338072839127039
g = 2

WHIRLPOOL_HEX = "DA797370298016DFD13DC0B90F952102F14881088C34511558C192D92D958791FAAAFF267F286CFEAF72E418ED24C7CB854998214B34F21CAF26D9C6D4B1F975"
h = int(WHIRLPOOL_HEX, 16)

print(f"Whirlpool hash (hex): {WHIRLPOOL_HEX}")
print(f"Whirlpool hash (decimal): {h}\n")

print(f"ElGamal parameters:")
print(f"p (2048-bit prime): {p}")
print(f"g (generator): {g}\n")

x = secrets.randbelow(p - 2) + 2
y = pow(g, x, p)

print(f"Private key x: {x}")
print(f"Public key y = g^x mod p: {y}\n")

h_mod = h % (p - 1)

while True:
    k = secrets.randbelow(p - 2) + 2
    if gcd(k, p - 1) == 1:
        break

r = pow(g, k, p)
k_inv = modinv(k, p - 1)
s = ((h_mod - x * r) * k_inv) % (p - 1)

print(f"Signature (r, s):")
print(f"r = g^k mod p: {r}")
print(f"s = (h - x*r) * k^(-1) mod (p-1): {s}\n")

left = pow(g, h_mod, p)
right = (pow(y, r, p) * pow(r, s, p)) % p

print(f"Verification:")
print(f"Left: g^h mod p = {left}")
print(f"Right: y^r * r^s mod p = {right}")
print("Result:", "SUCCESS" if left == right else "FAILED")
