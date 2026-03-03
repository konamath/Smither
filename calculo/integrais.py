"""
Módulo de Integrais - Smither
==============================
Funções específicas para cálculo de integrais com visualizações gráficas.
"""

from . import engine
from .engine import Integral, IntegralDefinida, IntegralDupla, EngineCalculo
from . import graficos
from .graficos import GraficoDerivada, GraficoIntegral
from typing import Optional, Tuple
import numpy as np


class Cores:
    """Cores para terminal."""
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def menu_integrais():
    """Menu interativo para calculo de integrais."""
    
    while True:
        print("\n" + "="*70)
        print("                          INTEGRAIS")
        print("="*70)
        print(f"\n{Cores.BOLD}Funcoes de Uma Variavel:{Cores.ENDC}")
        print("  1. Integral Indefinida")
        print("  2. Integral Definida")
        
        print(f"\n{Cores.BOLD}Funcoes de Multiplas Variaveis:{Cores.ENDC}")
        print("  3. Integral Dupla Indefinida")
        print("  4. Integral Dupla Definida")
        
        print(f"\n  {Cores.OKBLUE}0{Cores.ENDC}. Voltar ao Menu Anterior\n")
        
        escolha = input("Escolha uma opcao: ").strip()
        
        if escolha == '0':
            break
        elif escolha == '1':
            _integral_indefinida()
        elif escolha == '2':
            _integral_definida()
        elif escolha == '3':
            _integral_dupla_indefinida()
        elif escolha == '4':
            _integral_dupla_definida()
        # opção de integrais triplas removida
        else:
            print(f"{Cores.FAIL}[Erro] Opcao invalida!{Cores.ENDC}")


def _integral_indefinida():
    """Calcula integral indefinida."""
    print("\n" + "-"*70)
    print("INTEGRAL INDEFINIDA")
    print("-"*70)
    
    expr = input("\nDigite a expressao (ex: x**2 + 3*x): ").strip()
    var = input("Digite a variavel (ex: x): ").strip()
    
    # Valida expressao
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}[Erro] Expressao invalida: {erro}{Cores.ENDC}")
        return
    
    resultado = Integral.calcular(expr, var)
    
    if resultado:
        orig, integral = resultado
        print(f"\n{Cores.OKGREEN}[OK] Resultado:{Cores.ENDC}")
        print(f"  Funcao: f({var}) = {orig}")
        print(f"  Integral: S f({var})d{var} = {integral} + C")
        
        plotar = input(f"\n{Cores.OKCYAN}Como exibir o grafico? (v)er / (s)alvar / (a)uto [padrao v]: {Cores.ENDC}").strip().lower()
        if plotar in ('v', '', 's', 'a'):
            if plotar in ('v', ''):
                salvar = False
            elif plotar == 's':
                salvar = True
            else:
                salvar = None
            
            intervalo = _obter_intervalo()
            try:
                res = GraficoDerivada.plotar_funcao_1var(expr, var, intervalo, titulo=f'Funcao para integrar', salvar=salvar)
                if isinstance(res, str):
                    print(f"{Cores.OKGREEN}[OK] Grafico salvo em: {res}{Cores.ENDC}")
            except Exception as e:
                print(f"{Cores.FAIL}[Erro] ao gerar grafico: {e}{Cores.ENDC}")
    else:
        print(f"{Cores.FAIL}[Erro] ao calcular integral{Cores.ENDC}")


def _integral_definida():
    """Calcula integral definida e mostra area."""
    print("\n" + "-"*70)
    print("INTEGRAL DEFINIDA")
    print("-"*70)
    
    expr = input("\nDigite a expressao (ex: x**2): ").strip()
    var = input("Digite a variavel (ex: x): ").strip()
    
    # Valida expressao
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}[Erro] Expressao invalida: {erro}{Cores.ENDC}")
        return
    
    # Ler limites como strings para permitir simbolicos (ex: pi)
    a_raw = input("Digite o limite inferior (a): ").strip()
    b_raw = input("Digite o limite superior (b): ").strip()

    # Tenta converter para numeros reais. Se falhar, usaremos processamento simbólico.
    a_val = None
    b_val = None
    uso_simbolico = False
    try:
        a_val = float(a_raw)
        b_val = float(b_raw)
    except Exception:
        uso_simbolico = True

    resultado = None
    if not uso_simbolico:
        if a_val >= b_val:
            print(f"{Cores.FAIL}[Erro] Limite inferior deve ser menor que o superior{Cores.ENDC}")
            return
        resultado = IntegralDefinida.calcular(expr, var, a_val, b_val)
    else:
        # Usa a versão simbólica do cálculo para aceitar pi, oo, etc.
        try:
            resultado = IntegralDefinida.calcular_simbolico(expr, var, a_raw, b_raw)
        except Exception:
            resultado = None
    
    if resultado:
        orig, valor = resultado
        print(f"\n{Cores.OKGREEN}[OK] Resultado:{Cores.ENDC}")
        print(f"  Funcao: f({var}) = {orig}")
        # use raw inputs when available for symbolic limits
        low = a_raw if uso_simbolico else a_val
        high = b_raw if uso_simbolico else b_val
        print(f"  Integral de {low} a {high}: S f({var})d{var} = {valor:.6g}")
        print(f"\n  [Info] Valor representa a AREA sob a curva")
        
        plotar = input(f"\n{Cores.OKCYAN}Como exibir o grafico com area? (v)er / (s)alvar / (a)uto [padrao v]: {Cores.ENDC}").strip().lower()
        if plotar in ('v', '', 's', 'a'):
            if plotar in ('v', ''):
                salvar = False
            elif plotar == 's':
                salvar = True
            else:
                salvar = None
            
            try:
                res = GraficoIntegral.plotar_area_integral(expr, var, a, b, salvar=salvar)
                if isinstance(res, str):
                    print(f"{Cores.OKGREEN}[OK] Grafico salvo em: {res}{Cores.ENDC}")
            except Exception as e:
                print(f"{Cores.FAIL}[Erro] ao gerar grafico: {e}{Cores.ENDC}")
    else:
        print(f"{Cores.FAIL}[Erro] ao calcular integral{Cores.ENDC}")


def _integral_dupla_definida():
    """Calcula integral dupla definida."""
    print("\n" + "-"*70)
    print("INTEGRAL DUPLA DEFINIDA")
    print("-"*70)
    print("\nExemplo: x*y (com limites x: 0 a 1, y: 0 a 2)")
    
    # existing code for defined case has been moved here
    expr = input("\nDigite a expressao (use 'x' e 'y'): ").strip()
    
    # Valida expressao
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}[Erro] Expressao invalida: {erro}{Cores.ENDC}")
        return
    
    try:
        x1 = float(input("Limite inferior de x: ").strip())
        x2 = float(input("Limite superior de x: ").strip())
        y1 = float(input("Limite inferior de y: ").strip())
        y2 = float(input("Limite superior de y: ").strip())
    except ValueError:
        print(f"{Cores.FAIL}[Erro] Limites devem ser numeros{Cores.ENDC}")
        return
    
    if x1 >= x2 or y1 >= y2:
        print(f"{Cores.FAIL}[Erro] Limites invalidos{Cores.ENDC}")
        return
    
    resultado = IntegralDupla.calcular(expr, 'x', x1, x2, 'y', y1, y2)
    
    if resultado:
        orig, valor = resultado
        print(f"\n{Cores.OKGREEN}[OK] Resultado:{Cores.ENDC}")
        print(f"  Funcao: f(x,y) = {orig}")
        print(f"  Integral dupla: S S f(x,y) dx dy = {valor:.6g}")
        print(f"\n  [Info] Valor representa o VOLUME sob a superficie")
        
        plotar = input(f"\n{Cores.OKCYAN}Como exibir a superficie? (v)er / (s)alvar / (a)uto [padrao v]: {Cores.ENDC}").strip().lower()
        if plotar in ('v', '', 's', 'a'):
            if plotar in ('v', ''):
                salvar = False
            elif plotar == 's':
                salvar = True
            else:
                salvar = None
            
            try:
                res = GraficoDerivada.plotar_funcao_2var(expr, intervalo=(min(x1, y1), max(x2, y2)), tipo_plot='surface', salvar=salvar)
                if isinstance(res, str):
                    print(f"{Cores.OKGREEN}[OK] Grafico salvo em: {res}{Cores.ENDC}")
            except Exception as e:
                print(f"{Cores.FAIL}[Erro] ao gerar grafico: {e}{Cores.ENDC}")
    else:
        print(f"{Cores.FAIL}[Erro] ao calcular integral dupla{Cores.ENDC}")




def _integral_dupla_indefinida():
    """Calcula integral dupla indefinida."""
    print("\n" + "-"*70)
    print("INTEGRAL DUPLA INDEFINIDA")
    print("-"*70)
    expr = input("\nDigite a expressao (use 'x' e 'y'): ").strip()
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}[Erro] Expressao invalida: {erro}{Cores.ENDC}")
        return
    var1 = input("Digite a primeira variavel (ex: x) [x]: ").strip() or 'x'
    var2 = input("Digite a segunda variavel (ex: y) [y]: ").strip() or 'y'
    resultado = IntegralDupla.calcular_indefinida(expr, var1, var2)
    if resultado:
        orig, simb = resultado
        print(f"\n{Cores.OKGREEN}[OK] Resultado da integral dupla indefinida:{Cores.ENDC}")
        print(f"  f({var1},{var2}) = {orig}")
        print(f"  Integral: F({var1},{var2}) = {simb} + C")
    else:
        print(f"{Cores.FAIL}[Erro] ao calcular integral dupla indefinida{Cores.ENDC}")

# Triple integrals removed by user request.


def _obter_intervalo():
    """Obtém intervalo do usuário para plotagem."""
    try:
        print(f"\n{Cores.OKCYAN}Intervalo para o grafico:{Cores.ENDC}")
        min_val = float(input("  Valor minimo (padrao -10): ").strip() or "-10")
        max_val = float(input("  Valor maximo (padrao 10): ").strip() or "10")
        return (min_val, max_val)
    except ValueError:
        print(f"{Cores.WARNING}[Aviso] Usando intervalo padrao (-10, 10){Cores.ENDC}")
        return (-10, 10)
