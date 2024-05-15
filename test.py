def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Exemple d'utilisation
nombre1 = 48
nombre2 = 18
resultat = pgcd(nombre1, nombre2)
print("Le PGCD de", nombre1, "et", nombre2, "est:", resultat)