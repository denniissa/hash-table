import pandas as pd
import random
import hashlib
from collections import defaultdict

# Dicționar de nume masculine și feminine (noua listă de nume)
nume_masculine = ["Andrei", "Alexandru", "Mihai", "Cristian", "Gabriel"]
nume_feminine = ["Maria", "Elena", "Ioana", "Raluca", "Adriana"]

# Distribuția județelor (simplificată pentru exemplu)
judete = [f"{i:02d}" for i in range(1, 53)]  # Coduri județe 01-52
populatie_judete = [random.randint(1, 100) for _ in judete]  # Distribuție simplă

# Funcție pentru generarea unui CNP valid
def genereaza_cnp():
    sex = random.choice([1, 2])  # 1: Bărbat, 2: Femeie
    anul_nasterii = random.randint(1900, 2022)
    secol = 1 if anul_nasterii < 2000 else 2
    sex += (secol - 1) * 2

    aa = f"{anul_nasterii % 100:02d}"  # Anul nașterii
    ll = f"{random.randint(1, 12):02d}"  # Luna nașterii
    zile_in_luna = [31, 29 if int(aa) % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    zz = f"{random.randint(1, zile_in_luna[int(ll) - 1]):02d}"  # Ziua nașterii

    judet = random.choices(judete, weights=populatie_judete, k=1)[0]  # Județ
    nnn = f"{random.randint(0, 999):03d}"  # Număr unic

    cnp_fara_c = f"{sex}{aa}{ll}{zz}{judet}{nnn}"  # Fără cifra de control
    cifre_control = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    suma_control = sum(int(cnp_fara_c[i]) * cifre_control[i] for i in range(12))
    c = suma_control % 11
    if c == 10:
        c = 1

    return cnp_fara_c + str(c)

# Generare CNP-uri și asocierea de nume
def genereaza_date_cnp(n):
    cnp_nume = []
    for _ in range(n):
        cnp = genereaza_cnp()
        sex = int(cnp[0])
        nume = random.choice(nume_masculine if sex in [1, 3, 5, 7] else nume_feminine)
        cnp_nume.append((cnp, nume))
    return cnp_nume

# Crearea structurii hash
def hash_function(cnp):
    return int(hashlib.sha256(cnp.encode()).hexdigest(), 16) % 1000

def creeaza_hash_table(cnp_nume):
    hash_table = defaultdict(list)
    for cnp, nume in cnp_nume:
        index = hash_function(cnp)
        hash_table[index].append((cnp, nume))
    return hash_table

# Căutare CNP-uri
def cauta_cnpuri(cnp_de_cautat, hash_table):
    rezultate_cautare = []
    for cnp, nume in cnp_de_cautat:
        index = hash_function(cnp)
        lista = hash_table[index]
        iteratii = 0
        for item in lista:
            iteratii += 1
            if item[0] == cnp:
                rezultate_cautare.append({"CNP": cnp, "Nume": nume, "Iteratii": iteratii})
                break
    return rezultate_cautare

# Configurări
NUMAR_CNP_URI = 10_000
NUMAR_CNP_DE_CAUTAT = 1_000

# Generare date
cnp_nume = genereaza_date_cnp(NUMAR_CNP_URI)
hash_table = creeaza_hash_table(cnp_nume)
cnp_de_cautat = random.sample(cnp_nume, NUMAR_CNP_DE_CAUTAT)

# Căutare și salvare rezultate
rezultate_cautare = cauta_cnpuri(cnp_de_cautat, hash_table)
df_rezultate = pd.DataFrame(rezultate_cautare)

# Salvăm tabelul
output_file = "rezultate_cnp.xlsx"
df_rezultate.to_excel(output_file, index=False)
print(f"Rezultatele au fost salvate în fișierul '{output_file}'.")
