"""
Módulo de Limites - Smither
===========================
Funções específicas para cálculo de limites com aplicações econômicas.
"""

from .engine import Limite, EngineCalculo


def menu_limites():
    """Menu interativo para cálculos de limites."""
    
    while True:
        print("\n" + "="*70)
        print("                          LIMITES")
        print("="*70)
        print("\n1. Limites de 1 Variável")
        print("2. Limites de 2 Variáveis")
        print("3. Assíntotas e Comportamento")
        print("0. Voltar ao Menu de Cálculo\n")
        
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == '0':
            break
        elif escolha == '1':
            _menu_limite_uma_variavel()
        elif escolha == '2':
            _calcular_limite_duas_variaveis()
        elif escolha == '3':
            _menu_assintotas()
        else:
            print("❌ Opção inválida!")


def _menu_limite_uma_variavel():
    """Submenu para limites com uma única variável."""
    while True:
        print("\n" + "-"*70)
        print("LIMITES DE 1 VARIÁVEL")
        print("-"*70)
        print("\n1. Calcular Limite em um Ponto")
        print("2. Calcular Limite no Infinito")
        print("0. Voltar\n")
        
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == '0':
            break
        elif escolha == '1':
            _calcular_limite_ponto()
        elif escolha == '2':
            _calcular_limite_infinito()
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


def _calcular_limite_duas_variaveis():
    """Calcula limite para funções de duas variáveis."""
    print("\n" + "-"*70)
    print("LIMITES DE 2 VARIÁVEIS")
    print("-"*70)
    print("Calculará: lim f(x, y) conforme (x, y) → (a, b)")
    
    expr = input("\nDigite a expressão (ex: (x**2 + y**2)/(x**2 + y**2 + 1)): ").strip()
    variaveis_input = input("Variáveis (separadas por vírgula, padrão: x,y): ").strip()
    if variaveis_input:
        variaveis = [v.strip() for v in variaveis_input.split(',') if v.strip()]
    else:
        variaveis = ['x', 'y']
    
    if len(variaveis) != 2:
        print("❌ Informe exatamente duas variáveis, como 'x,y'.")
        return
    
    pontos = []
    for var in variaveis:
        valor = input(f"Valor limite para {var} (ex: 0, oo, -oo): ").strip()
        if not valor:
            print("❌ Valor inválido.")
            return
        pontos.append(valor)
    
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"❌ Expressão inválida: {erro}")
        return
    
    resultado = Limite.calcular_multivariavel(expr, variaveis, pontos)
    
    if not resultado:
        print("❌ Não foi possível calcular o limite multivariável.")
        return
    
    alvo = ", ".join([f"{var}→{val}" for var, val in zip(variaveis, pontos)])
    print(f"\nFunção: f({', '.join(variaveis)}) = {resultado['expressao']}")
    print(f"Ponto de aproximação: ({alvo})")
    
    print("\nResultados por ordem de aproximação:")
    for info in resultado['resultados_ordem']:
        ordem = " → ".join(info['ordem'])
        print(f"  - Ordem {ordem}: {info['valor']}")
    
    if resultado['caminhos']:
        print("\nTestes por trajetórias:")
        for caminho in resultado['caminhos']:
            print(f"  - {caminho['descricao']} ⇒ {caminho['valor']}")
    
    if resultado['consistente'] and resultado['valor']:
        print(f"\n🎯 Limite estimado: {resultado['valor']}")
        print("   Resultados coerentes em todas as ordens e trajetórias testadas.")
    else:
        print("\n⚠️ Os valores divergem entre ordens ou trajetórias.")
        print("   Isso sugere que o limite pode não existir ou depende do caminho.")


def _menu_assintotas():
    """Menu para assíntotas e comportamento de longo prazo."""
    while True:
        print("\n" + "-"*70)
        print("ASSÍNTOTAS E COMPORTAMENTO")
        print("-"*70)
        print("\n1. Detectar assíntotas (verticais, horizontais e oblíquas)")
        print("2. Análise de comportamento assintótico (econômico)")
        print("0. Voltar\n")
        
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == '0':
            break
        elif escolha == '1':
            _detectar_assintotas()
        elif escolha == '2':
            _analise_assintotica()
        else:
            print("❌ Opção inválida!")


def _detectar_assintotas():
    """Detecta assíntotas verticais, horizontais e oblíquas."""
    print("\n" + "-"*70)
    print("DETECÇÃO DE ASSÍNTOTAS")
    print("-"*70)
    
    expr = input("\nDigite a função (ex: (x**2 + 1)/(x - 1)): ").strip()
    var = input("Digite a variável (padrão: x): ").strip() or 'x'
    
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"❌ Expressão inválida: {erro}")
        return
    
    resultado = Limite.encontrar_assintotas(expr, var)
    if not resultado:
        print("❌ Não foi possível identificar assíntotas para essa função.")
        return
    
    print(f"\nFunção analisada: f({var}) = {resultado['expressao']}")
    
    def _mostrar(titulo, itens):
        print(f"\n{titulo}:")
        if itens:
            for item in itens:
                print(f"  • {item}")
        else:
            print("  (Nenhuma detectada)")
    
    _mostrar("Assíntotas Verticais", resultado.get('verticais', []))
    _mostrar("Assíntotas Horizontais", resultado.get('horizontais', []))
    _mostrar("Assíntotas Oblíquas", resultado.get('obliquas', []))
    
    if not any([resultado.get('verticais'), resultado.get('horizontais'), resultado.get('obliquas')]):
        print("\nℹ️ A função não apresenta assíntotas com os critérios analisados.")


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
