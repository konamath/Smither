"""
Módulo de Limites - Smither
===========================
Funções específicas para cálculo de limites com aplicações econômicas.
"""

from engine import Limite, EngineCalculo
from typing import Optional


def menu_limites():
    """Menu interativo para cálculos de limites."""
    
    while True:
        print("\n" + "="*70)
        print("                          LIMITES")
        print("="*70)
        print("\n1. Calcular Limite em um Ponto")
        print("2. Calcular Limite no Infinito")
        print("3. Análise de Comportamento Assintótico (Economia)")
        print("0. Voltar ao Menu de Cálculo\n")
        
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == '0':
            break
        elif escolha == '1':
            _calcular_limite_ponto()
        elif escolha == '2':
            _calcular_limite_infinito()
        elif escolha == '3':
            _analise_assintotica()
        else:
            print("❌ Opção inválida!")


def _calcular_limite_ponto():
    """Calcula limite quando x tende a um ponto específico."""
    print("\n" + "-"*70)
    print("LIMITE EM UM PONTO")
    print("-"*70)
    print("Calculará: lim (x→a) f(x)")
    
    expr = input("\nDigite a expressão (ex: (x**2 - 1)/(x - 1)): ").strip()
    var = input("Digite a variável (ex: x): ").strip()
    
    try:
        ponto = float(input("Digite o ponto onde x tende: ").strip())
    except ValueError:
        print("❌ Digite um número válido")
        return
    
    # Valida expressão
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"❌ Expressão inválida: {erro}")
        return
    
    resultado = Limite.calcular(expr, var, ponto)
    
    if resultado:
        orig, lim = resultado
        print(f"\n✓ Resultado:")
        print(f"  Função: f({var}) = {orig}")
        print(f"  lim (x→{ponto}) f({var}) = {lim}")
    else:
        print("❌ Erro ao calcular limite")


def _calcular_limite_infinito():
    """Calcula limite quando x tende ao infinito."""
    print("\n" + "-"*70)
    print("LIMITE NO INFINITO")
    print("-"*70)
    print("Calculará: lim (x→∞) f(x) ou lim (x→-∞) f(x)")
    
    expr = input("\nDigite a expressão (ex: (3*x**2 + 2*x)/(x**2 + 1)): ").strip()
    var = input("Digite a variável (ex: x): ").strip()
    
    print("\nEscolha a direção:")
    print("1. x → +∞ (mais infinito)")
    print("2. x → -∞ (menos infinito)")
    opcao = input("Escolha (1 ou 2): ").strip()
    
    if opcao == '1':
        ponto = 'oo'
        direcao = "+∞"
    elif opcao == '2':
        ponto = '-oo'
        direcao = "-∞"
    else:
        print("❌ Opção inválida")
        return
    
    # Valida expressão
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"❌ Expressão inválida: {erro}")
        return
    
    resultado = Limite.calcular(expr, var, ponto)
    
    if resultado:
        orig, lim = resultado
        print(f"\n✓ Resultado:")
        print(f"  Função: f({var}) = {orig}")
        print(f"  lim (x→{direcao}) f({var}) = {lim}")
    else:
        print("❌ Erro ao calcular limite")


def _analise_assintotica():
    """
    Análise de comportamento assintótico útil em economia.
    Exs: Limites de produção, crescimento econômico de longo prazo, etc.
    """
    print("\n" + "-"*70)
    print("ANÁLISE DE COMPORTAMENTO ASSINTÓTICO")
    print("-"*70)
    print("\nÚtil para analisar:")
    print("  • Limite de produção")
    print("  • Crescimento de longo prazo")
    print("  • Convergência econômica")
    print("  • Comportamento assintótico de custos")
    
    print("\nExemplo: Y = 100 - 50*e^(-0.1*t)")
    print("Limite quando t→∞ converge para 100 (produto potencial)")
    
    expr = input("\nDigite a função (ex: 100 - 50*exp(-0.1*x)): ").strip()
    var = input("Digite a variável temporal/progressiva (ex: x, t): ").strip()
    
    # Valida expressão
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"❌ Expressão inválida: {erro}")
        return
    
    resultado = Limite.calcular(expr, var, 'oo')
    
    if resultado:
        orig, lim = resultado
        
        # Tenta converter para float para análise
        try:
            lim_valor = float(lim)
            print(f"\n✓ Resultado:")
            print(f"  Função: f({var}) = {orig}")
            print(f"  lim (x→∞) f({var}) = {lim}")
            print(f"\n  📊 Interpretação Econômica:")
            print(f"     Quando {var} tende a infinito, f({var}) converge para {lim_valor:.4f}")
            print(f"     Este é o valor assintótico/de equilíbrio de longo prazo.")
        except:
            print(f"\n✓ Resultado:")
            print(f"  Função: f({var}) = {orig}")
            print(f"  lim (x→∞) f({var}) = {lim}")
            print(f"\n  📊 Este é o comportamento de longo prazo da função.")
    else:
        print("❌ Erro ao calcular limite")
