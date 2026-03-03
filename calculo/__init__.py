"""
Módulo de Cálculo - Smither
===========================
Fornece ferramentas para:
- Cálculo de Derivadas (simples, parciais, direcionais)
- Análise de Extremos (máximos, mínimos, sela)
- Cálculo de Integrais (indefinidas, definidas, duplas, triplas)
- Visualização gráfica
"""

from .engine import (
    EngineCalculo, Derivada, DerivadaParcial, DerivadaDirecional, Extremos,
    Integral, IntegralDefinida, IntegralDupla
)
from . import campo_vetorial
from . import menu_calculo
from . import integrais


def menu():
    """Funcao de entrada do modulo de calculo."""
    menu_calculo.menu_calculo()


__all__ = [
    'menu',
    'campo_vetorial',
    'menu_calculo',
    'integrais',
    'EngineCalculo',
    'Derivada',
    'DerivadaParcial',
    'DerivadaDirecional',
    'Extremos',
    'Integral',
    'IntegralDefinida',
    'IntegralDupla'
]
