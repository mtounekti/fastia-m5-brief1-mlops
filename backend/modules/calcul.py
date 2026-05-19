# Module de calcul: logique métier découplée et testable

def calcul_carre(n: int) -> int:
    """
    calcule le carré d'un entier

    args:
        n (int): l'entier à élever au carré

    returns:
        int: Le carré de n (n * n)

    raises:
        TypeError: Si n n'est pas un entier.
        ValueError: Si n est en dehors des limites acceptées.
    """
    if not isinstance(n, int):
        raise TypeError(f"Le paramètre doit être un entier, reçu : {type(n).__name__}")

    if abs(n) > 10_000:
        raise ValueError(f"La valeur {n} est trop grande (max ±10 000)")

    return n * n