import os
import sys

# ajout du répertoire parent pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.calcul import calcul_carre


# accurate tests
def test_carre_positif():
    """test avec un entier positif standard"""
    assert calcul_carre(4)  == 16
    assert calcul_carre(7)  == 49
    assert calcul_carre(10) == 100

def test_carre_zero():
    """test avec 0 : cas limite"""
    assert calcul_carre(0) == 0

def test_carre_negatif():
    """test avec un entier négatif: le carré doit être +"""
    assert calcul_carre(-3)  == 9
    assert calcul_carre(-10) == 100

def test_carre_grand_nombre():
    """test avec la valeur maximale acceptée."""
    assert calcul_carre(10_000) == 100_000_000

def test_carre_un():
    """test avec 1 et -1."""
    assert calcul_carre(1)  == 1
    assert calcul_carre(-1) == 1



# errors tests
def test_type_float():
    """un float doit lever une TypeError"""
    import pytest
    with pytest.raises(TypeError):
        calcul_carre(3.14)

def test_type_string():
    """une chaîne doit lever une TypeError"""
    import pytest
    with pytest.raises(TypeError):
        calcul_carre("cinq")

def test_valeur_trop_grande():
    """une valeur > 10 000 doit lever une ValueError"""
    import pytest
    with pytest.raises(ValueError):
        calcul_carre(10_001)

def test_valeur_trop_petite():
    """une valeur < -10 000 doit lever une ValueError"""
    import pytest
    with pytest.raises(ValueError):
        calcul_carre(-10_001)