"""
Modulo de Algebra Linear - Smither
==================================
"""

from . import menu_algebralinear


def menu():
    """Funcao de entrada do modulo."""
    menu_algebralinear.menu()


__all__ = [
    "menu",
    "menu_algebralinear",
]
