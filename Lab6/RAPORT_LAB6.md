# Raport Laborator 6 - Semnături Digitale
## RSA și ElGamal Digital Signatures

---

## Echivalențe Python - Wolfram Mathematica

| Wolfram | Python | Descriere |
|---------|--------|-----------|
| `Prime[n]` | `sympy.prime(n)` | Al n-lea număr prim |
| `RandomPrime[{imin, imax}]` | `sympy.randprime(imin, imax)` | Număr prim aleator între imin și imax |
| `RandomInteger[imax]` | `random.randint(0, imax)` sau `secrets.randbelow(imax)` | Număr întreg aleator 0-imax |
| `Mod[a, n]` | `a % n` sau `pow(a, 1, n)` | Restul împărțirii a la n |
| `PowerMod[a, b, n]` | `pow(a, b, n)` | Restul împărțirii a^b la n |
| `FactorInteger[n]` | `sympy.factorint(n)` | Factorizare în factori primi |
| `IntegerDigits[n, b]` | Conversie manuală sau `format(n, f'0{len}b')` | Cifrele în baza b |
| `Length[lst]` | `len(lst)` | Lungimea listei |

---

## Task 1: RSA Digital Signature

### Parametri
- **k (număr student)**: 20
- **i (index hash)**: i = (k mod 24) + 1 = (20 mod 24) + 1 = 21
- **Hash algoritm**: NTLM (index 21 în listă)
- **Hash hex**: `AE6BAA4ABE48DE6E65AA9E8DAF88AD8D`
- **Hash decimal**: `231844700961845480207942948153796898189`
- **Dimensiune n**: ≥ 3072 biți

---

### Pașii Algoritmului RSA Digital Signature

#### PASUL 1: Conversie hash din hexadecimal în decimal

**Explicație**: Hash-ul mesajului a fost calculat cu NTLM (MD4) și obținut în format hexadecimal. Pentru semnarea RSA, trebuie convertit în număr întreg (decimal).

**Cod Python**:
```python
NTLM_HEX = "AE6BAA4ABE48DE6E65AA9E8DAF88AD8D"
h = int(NTLM_HEX, 16)
# Rezultat: h = 231844700961845480207942948153796898189
```

**Echivalent Wolfram**: `FromDigits[IntegerDigits[hex_string, 16], 10]`

**Rezultat**:
- Hash hex: `AE6BAA4ABE48DE6E65AA9E8DAF88AD8D`
- Hash decimal: `231844700961845480207942948153796898189`

---

#### PASUL 2: Generare numere prime p și q

**Explicație**: Pentru n ≥ 3072 biți, generăm două numere prime p și q, fiecare de aproximativ 1536 biți, astfel încât n = p × q să aibă cel puțin 3072 biți.

**Cod Python**:
```python
from sympy import randprime

bits = 1536  # Fiecare prim are ~1536 biți
while True:
    p = randprime(2**(bits - 1), 2**bits)  # Prime între 2^1535 și 2^1536
    q = randprime(2**(bits - 1), 2**bits)
    while p == q:  # Asigură că p ≠ q
        q = randprime(2**(bits - 1), 2**bits)
    n = p * q
    if n.bit_length() >= 3072:  # Verifică condiția n ≥ 3072 biți
        break
```

**Echivalent Wolfram**: 
```mathematica
p = RandomPrime[{2^(1535), 2^(1536)}];
q = RandomPrime[{2^(1535), 2^(1536)}];
n = p * q;
```

**Explicație detaliată**:
- `randprime(2**(bits - 1), 2**bits)` generează un număr prim aleator între 2^(1535) și 2^1536
- Verificăm că p ≠ q pentru a evita atacuri criptografice
- Loop-ul continuă până când n = p × q are cel puțin 3072 biți (uneori poate fi 3071 dacă cele două prime sunt apropiate de limita inferioară)

**Rezultat exemplu**:
- p: număr prim de ~1536 biți
- q: număr prim de ~1536 biți
- n: modul de 3072 biți

---

#### PASUL 3: Calculul funcției Euler φ(n)

**Explicație**: Funcția Euler φ(n) reprezintă numărul de numere întregi pozitive mai mici decât n și coprime cu n. Pentru n = p × q (unde p și q sunt prime), φ(n) = (p-1) × (q-1).

**Cod Python**:
```python
phi_n = (p - 1) * (q - 1)
```

**Echivalent Wolfram**: `EulerPhi[n]` sau `(p-1)*(q-1)`

**Rezultat**: φ(n) = (p-1) × (q-1) - un număr foarte mare, aproape de n

---

#### PASUL 4: Alegerea exponentului public e

**Explicație**: Exponentul public e trebuie să fie coprime cu φ(n), adică GCD(e, φ(n)) = 1. Valoarea standard folosită este e = 65537 (2^16 + 1), care este prim și suficient de mare pentru securitate.

**Cod Python**:
```python
from math import gcd

e = 65537
if gcd(e, phi_n) != 1:
    raise ValueError("e and phi(n) are not coprime")
```

**Echivalent Wolfram**: 
```mathematica
e = 65537;
If[GCD[e, phi_n] != 1, Throw["e and phi(n) are not coprime"]]
```

**Verificare**: GCD(65537, φ(n)) trebuie să fie 1. Dacă nu, trebuie regenerați p și q (foarte rar).

---

#### PASUL 5: Calculul exponentului privat d

**Explicație**: Exponentul privat d este inversul modular al lui e modulo φ(n), adică d este numărul pentru care e × d ≡ 1 (mod φ(n)). Acest lucru permite decriptarea și semnarea.

**Cod Python**:
```python
def modinv(a, m):
    """
    Calculează inversul modular al lui a modulo m folosind algoritmul Euclid extins.
    
    Algoritm:
    1. Inițializăm: m0 = m, x0 = 0, x1 = 1
    2. În timp ce a > 1:
       - Calculăm q = a // m (câtul)
       - Actualizăm: a, m = m, a % m (restul)
       - Actualizăm: x0, x1 = x1 - q*x0, x0
    3. Dacă x1 < 0, adunăm m0 pentru a obține un rezultat pozitiv
    """
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m      # Câtul împărțirii
        a, m = m, a % m  # Euclid: a = m, m = a mod m
        x0, x1 = x1 - q * x0, x0  # Actualizare coeficienți
    if x1 < 0:
        x1 += m0
    return x1

d = modinv(e, phi_n)
```

**Echivalent Wolfram**: `PowerMod[e, -1, phi_n]`

**Verificare**: (e × d) mod φ(n) = 1

**Rezultat**: d este un număr foarte mare (aproape de φ(n)), parte a cheii private.

---

#### PASUL 6: Reducere hash modulo n (dacă necesar)

**Explicație**: Hash-ul trebuie să fie mai mic decât modulul n pentru ca semnarea să funcționeze corect. Dacă h ≥ n, reducem h modulo n.

**Cod Python**:
```python
if h >= n:
    h = h % n  # Reducere modulo n
```

**Echivalent Wolfram**: `h = Mod[h, n]`

**În cazul nostru**: Hash-ul NTLM (128 biți) este mult mai mic decât n (3072 biți), deci nu este necesară reducerea.

---

#### PASUL 7: Generarea semnăturii RSA

**Explicație**: Semnătura s se calculează ridicând hash-ul h la puterea exponentului privat d, modulo n. Acest lucru dovedește că mesajul a fost semnat de deținătorul cheii private.

**Cod Python**:
```python
s = pow(h, d, n)  # s = h^d mod n
```

**Echivalent Wolfram**: `s = PowerMod[h, d, n]`

**Explicație detaliată**:
- Folosim exponențiere modulară eficientă (`pow` cu 3 argumente este optimizat)
- Rezultatul s este semnătura digitală
- Doar deținătorul cheii private (d) poate genera această semnătură

**Rezultat**: s = h^d mod n - un număr mare de ~3072 biți

---

#### PASUL 8: Verificarea semnăturii RSA

**Explicație**: Verificarea se face ridicând semnătura s la puterea exponentului public e, modulo n. Dacă rezultatul este egal cu hash-ul original h, semnătura este validă.

**Cod Python**:
```python
v = pow(s, e, n)  # v = s^e mod n
is_valid = (v == h)
```

**Echivalent Wolfram**: `v = PowerMod[s, e, n]`

**Demonstrație matematică**:
```
v = s^e mod n
  = (h^d)^e mod n
  = h^(d×e) mod n
  = h^(1) mod n        (pentru că d×e ≡ 1 mod φ(n))
  = h mod n
```

**Rezultat**: Dacă v == h, semnătura este VALIDĂ ✓

---

### Rezumat Task 1

**Chei generate**:
- Public key: (n, e) unde n ≥ 3072 biți, e = 65537
- Private key: (d, n) unde d este calculat ca invers modular

**Proces semnare**:
1. Hash mesaj → NTLM → h (decimal)
2. Semnătură: s = h^d mod n

**Proces verificare**:
1. Verificare: v = s^e mod n
2. Validare: v == h → SUCCESS

---

## Task 2: ElGamal Digital Signature

### Parametri
- **k (număr student)**: 20
- **i (index hash)**: i = (k mod 24) + 1 = (20 mod 24) + 1 = 21
- **Hash algoritm**: Whirlpool (index 21 în lista task 2)
- **Hash hex**: `DA797370298016DFD13DC0B90F952102F14881088C34511558C192D92D958791FAAAFF267F286CFEAF72E418ED24C7CB854998214B34F21CAF26D9C6D4B1F975`
- **Hash decimal**: Număr mare (512 biți)
- **p**: 2048 biți (dat)
- **g**: 2 (generator dat)

---

### Pașii Algoritmului ElGamal Digital Signature

#### PASUL 1: Inițializare parametri

**Explicație**: Parametrii p (prim de 2048 biți) și g = 2 (generator) sunt dați. Hash-ul mesajului este calculat cu Whirlpool.

**Cod Python**:
```python
p = 32317006071311007300153513477825163362488057133489075174588434139269806834136210002792056362640164685458556357935330816928829023080573472625273554742461245741026202527916572972862706300325263428213145766931414223654220941111348629991657478268034230553086349050635557712219187890332729569696129743856241741236237225197346402691855797767976823014625397933058015226858730761197532436467475855460715043896844940366130497697812854295958659597567051283852132784468522925504568272879113720098931873959143374175837826000278034973198552060607533234122603254684088120031105907484281003994966956119696956248629032338072839127039
g = 2

WHIRLPOOL_HEX = "DA797370298016DFD13DC0B90F952102F14881088C34511558C192D92D958791FAAAFF267F286CFEAF72E418ED24C7CB854998214B34F21CAF26D9C6D4B1F975"
h = int(WHIRLPOOL_HEX, 16)
```

**Echivalent Wolfram**: 
```mathematica
p = <număr prim dat>;
g = 2;
h = FromDigits[IntegerDigits[whirlpool_hex, 16], 10];
```

---

#### PASUL 2: Generare cheie privată x

**Explicație**: Cheia privată x este un număr aleator între 2 și p-2 (inclusiv), generat folosind generator criptografic securizat.

**Cod Python**:
```python
import secrets

x = secrets.randbelow(p - 2) + 2  # Număr aleator între 2 și p-1
```

**Echivalent Wolfram**: `x = RandomInteger[{2, p-2}]`

**Explicație detaliată**:
- `secrets.randbelow(p - 2)` generează un număr aleator 0 ≤ k < p-2
- Adăugăm 2 pentru a obține 2 ≤ x ≤ p-1
- x trebuie să fie secret și păstrat sigur

---

#### PASUL 3: Calcul cheie publică y

**Explicație**: Cheia publică y se calculează ca y = g^x mod p. Aceasta este parte din cheia publică și poate fi distribuită.

**Cod Python**:
```python
y = pow(g, x, p)  # y = g^x mod p
```

**Echivalent Wolfram**: `y = PowerMod[g, x, p]`

**Rezultat**: y este un număr mare (până la p-1) care face parte din cheia publică.

---

#### PASUL 4: Reducere hash modulo (p-1)

**Explicație**: Pentru semnarea ElGamal, hash-ul trebuie redus modulo (p-1), deoarece exponenții în semnătură vor fi modulo (p-1).

**Cod Python**:
```python
h_mod = h % (p - 1)  # h mod (p-1)
```

**Echivalent Wolfram**: `h_mod = Mod[h, p-1]`

**Rezultat**: h_mod este hash-ul redus, mai mic decât p-1.

---

#### PASUL 5: Generare k (număr aleator pentru semnătură)

**Explicație**: k este un număr aleator între 2 și p-2, care trebuie să fie coprime cu (p-1), adică GCD(k, p-1) = 1. Acest lucru este necesar pentru ca inversul modular al lui k să existe.

**Cod Python**:
```python
from math import gcd

while True:
    k = secrets.randbelow(p - 2) + 2  # Număr aleator între 2 și p-1
    if gcd(k, p - 1) == 1:  # Verifică că k și (p-1) sunt coprime
        break
```

**Echivalent Wolfram**: 
```mathematica
k = RandomInteger[{2, p-2}];
While[GCD[k, p-1] != 1, k = RandomInteger[{2, p-2}]];
```

**Explicație detaliată**:
- Loop continuă până când găsim un k cu GCD(k, p-1) = 1
- Probabilitatea ca două numere aleatoare să fie coprime este foarte mare
- k trebuie să fie unic pentru fiecare semnătură (nu trebuie reutilizat)

---

#### PASUL 6: Calcul componenta r a semnăturii

**Explicație**: Prima componentă a semnăturii ElGamal este r = g^k mod p. Aceasta "mască" valoarea k.

**Cod Python**:
```python
r = pow(g, k, p)  # r = g^k mod p
```

**Echivalent Wolfram**: `r = PowerMod[g, k, p]`

**Rezultat**: r este prima componentă a semnăturii (r, s).

---

#### PASUL 7: Calcul invers modular al lui k

**Explicație**: Pentru calcularea componentei s, avem nevoie de inversul modular al lui k modulo (p-1), adică k^(-1) mod (p-1).

**Cod Python**:
```python
k_inv = modinv(k, p - 1)  # k^(-1) mod (p-1)
```

**Echivalent Wolfram**: `k_inv = PowerMod[k, -1, p-1]`

**Verificare**: (k × k_inv) mod (p-1) = 1

---

#### PASUL 8: Calcul componenta s a semnăturii

**Explicație**: A doua componentă a semnăturii este s = (h - x×r) × k^(-1) mod (p-1). Aceasta combină hash-ul, cheia privată x, componenta r și inversul lui k.

**Cod Python**:
```python
s = ((h_mod - x * r) * k_inv) % (p - 1)
```

**Echivalent Wolfram**: `s = Mod[(h_mod - x*r) * k_inv, p-1]`

**Explicație detaliată**:
1. Calculăm h_mod - x×r (diferența dintre hash și produsul cheii private cu r)
2. Înmulțim cu inversul lui k
3. Reducem modulo (p-1)

**Rezultat**: s este a doua componentă a semnăturii (r, s).

**Semnătura completă**: (r, s) - două numere care dovedesc autenticitatea mesajului.

---

#### PASUL 9: Verificarea semnăturii ElGamal

**Explicație**: Verificarea se face prin compararea valorii g^h mod p cu produsul y^r × r^s mod p. Dacă sunt egale, semnătura este validă.

**Cod Python**:
```python
left = pow(g, h_mod, p)                    # g^h mod p
right = (pow(y, r, p) * pow(r, s, p)) % p  # y^r × r^s mod p
is_valid = (left == right)
```

**Echivalent Wolfram**: 
```mathematica
left = PowerMod[g, h_mod, p];
right = Mod[PowerMod[y, r, p] * PowerMod[r, s, p], p];
is_valid = (left == right);
```

**Demonstrație matematică**:
```
left = g^h mod p

right = y^r × r^s mod p
      = (g^x)^r × (g^k)^s mod p
      = g^(x×r) × g^(k×s) mod p
      = g^(x×r + k×s) mod p

Din definiția lui s:
s = (h - x×r) × k^(-1) mod (p-1)
k×s = h - x×r mod (p-1)
x×r + k×s = h mod (p-1)

Prin urmare:
right = g^(x×r + k×s) mod p
      = g^h mod p
      = left ✓
```

**Rezultat**: Dacă left == right, semnătura este VALIDĂ ✓

---

### Rezumat Task 2

**Chei generate**:
- Private key: x (aleator, secret)
- Public key: y = g^x mod p (distribuit public)

**Proces semnare**:
1. Hash mesaj → Whirlpool → h (decimal)
2. Reducere: h_mod = h mod (p-1)
3. Alege k aleator cu GCD(k, p-1) = 1
4. Calculează: r = g^k mod p
5. Calculează: s = (h_mod - x×r) × k^(-1) mod (p-1)
6. Semnătură: (r, s)

**Proces verificare**:
1. Calculează: left = g^h_mod mod p
2. Calculează: right = y^r × r^s mod p
3. Validare: left == right → SUCCESS

---

## Comparație RSA vs ElGamal

| Aspect | RSA | ElGamal |
|--------|-----|---------|
| **Dimensiune semnătură** | 1 număr (s) | 2 numere (r, s) |
| **Complexitate calcul** | O(log³ n) | O(log³ p) |
| **Securitate** | Bazată pe factorizare | Bazată pe logaritm discret |
| **Dimensiune cheie** | n ≥ 3072 biți | p = 2048 biți |
| **Hash utilizat** | NTLM (128 biți) | Whirlpool (512 biți) |

---

## Concluzii

Ambele algoritme de semnătură digitală funcționează corect:
- **RSA**: Semnătură simplă (un număr), verificare rapidă
- **ElGamal**: Semnătură dublă (două numere), securitate bazată pe logaritm discret

Ambele oferă:
- **Autentificare**: Dovedesc că mesajul vine de la expeditor
- **Integritate**: Orice modificare invalidă semnătura
- **Non-repudiere**: Semnătorul nu poate nega că a semnat

---

**Autor**: [Nume Student]  
**Data**: [Data]  
**Grupa**: [Grupa]  
**Număr student**: 20

