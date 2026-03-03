"""
Módulo de Estatística - Smither
================================
Funcionalidades estatísticas e análise de dados.
"""

from .menu_estatistica import menu_estatistica


def menu():
    """Função de entrada do módulo de estatística."""
    menu_estatistica()


__all__ = ['menu']
