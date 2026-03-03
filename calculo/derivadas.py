"""
Módulo de Derivadas - Smither
=============================
Funções específicas para cálculo de derivadas com visualizações gráficas.
"""

from . import engine
from .engine import Derivada, DerivadaParcial, DerivadaDirecional, Extremos, EngineCalculo
from . import graficos
from .graficos import GraficoDerivada, GraficoDerivadaParcial
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


def menu_derivadas():
    """Menu interativo para cálculos de derivadas."""
    
    while True:
        print("\n" + "="*70)
        print("                          DERIVADAS")
        print("="*70)
        print(f"\n{Cores.BOLD}Funções de Uma Variável:{Cores.ENDC}")
        print("  1. Derivada Simples (1ª Ordem)")
        print("  2. Derivada de Ordem Superior")
        print("  3. Valor da Derivada em um Ponto")
        print("  4. Máximos e Mínimos (uma variável)")
        
        print(f"\n{Cores.BOLD}Funções de Múltiplas Variáveis:{Cores.ENDC}")
        print("  5. Derivadas Parciais")
        print("  6. Gradiente")
        print("  7. Derivada Direcional")
        print("  8. Extremos em 2 Variáveis (Máximos/Mínimos/Sela)")
        
        print(f"\n  {Cores.OKBLUE}0{Cores.ENDC}. Voltar ao Menu Anterior\n")
        
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == '0':
            break
        elif escolha == '1':
            _calcular_derivada_simples()
        elif escolha == '2':
            _calcular_derivada_ordem_superior()
        elif escolha == '3':
            _calcular_derivada_ponto()
        elif escolha == '4':
            _extremos_1var()
        elif escolha == '5':
            _derivadas_parciais()
        elif escolha == '6':
            _calcular_gradiente()
        elif escolha == '7':
            _derivada_direcional()
        elif escolha == '8':
            _extremos_2var()
        else:
            print(f"{Cores.FAIL}❌ Opção inválida!{Cores.ENDC}")


def _calcular_derivada_simples():
    """Calcula derivada de primeira ordem com gráfico."""
    print("\n" + "-"*70)
    print("DERIVADA DE 1ª ORDEM")
    print("-"*70)
    
    expr = input("\nDigite a expressão (ex: x**2 + 3*x + 5): ").strip()
    var = input("Digite a variável (ex: x): ").strip()
    
    # Valida expressão
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}❌ Expressão inválida: {erro}{Cores.ENDC}")
        return
    
    resultado = Derivada.calcular(expr, var, ordem=1)
    
    if resultado:
        orig, deriv = resultado
        print(f"\n{Cores.OKGREEN}✓ Resultado:{Cores.ENDC}")
        print(f"  Função Original: f({var}) = {orig}")
        print(f"  Derivada:       f'({var}) = {deriv}")
        
        plotar = input(f"\n{Cores.OKCYAN}Como exibir o gráfico? (v)er / (s)alvar / (a)uto [padrão v]: {Cores.ENDC}").strip().lower()
        if plotar in ('v', ''):
            salvar = False
        elif plotar == 's':
            salvar = True
        else:
            salvar = None

        intervalo = _obter_intervalo()
        try:
            res = GraficoDerivada.plotar_funcao_derivada_1var(expr, var, intervalo, salvar=salvar)
            if isinstance(res, str):
                print(f"{Cores.OKGREEN}✓ Gráfico salvo em: {res}{Cores.ENDC}")
        except Exception as e:
            print(f"{Cores.FAIL}❌ Erro ao gerar gráfico: {e}{Cores.ENDC}")
    else:
        print(f"{Cores.FAIL}❌ Erro ao calcular derivada{Cores.ENDC}")


def _calcular_derivada_ordem_superior():
    """Calcula derivada de ordem superior."""
    print("\n" + "-"*70)
    print("DERIVADA DE ORDEM SUPERIOR")
    print("-"*70)
    
    expr = input("\nDigite a expressão (ex: x**3 + 2*x**2): ").strip()
    var = input("Digite a variável (ex: x): ").strip()
    
    try:
        ordem = int(input("Digite a ordem da derivada (2, 3, ...): ").strip())
        if ordem < 1:
            print(f"{Cores.FAIL}❌ A ordem deve ser um número positivo{Cores.ENDC}")
            return
    except ValueError:
        print(f"{Cores.FAIL}❌ Digite um número inteiro válido{Cores.ENDC}")
        return
    
    # Valida expressão
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}❌ Expressão inválida: {erro}{Cores.ENDC}")
        return
    
    resultado = Derivada.calcular(expr, var, ordem=ordem)
    
    if resultado:
        orig, deriv = resultado
        print(f"\n{Cores.OKGREEN}✓ Resultado:{Cores.ENDC}")
        print(f"  Função Original:    f({var})      = {orig}")
        print(f"  Derivada de {ordem}ª ordem: f^({ordem})({var}) = {deriv}")
    else:
        print(f"{Cores.FAIL}❌ Erro ao calcular derivada{Cores.ENDC}")


def _calcular_derivada_ponto():
    """Calcula o valor da derivada em um ponto específico."""
    print("\n" + "-"*70)
    print("VALOR DA DERIVADA NO PONTO")
    print("-"*70)
    
    expr = input("\nDigite a expressão (ex: x**2 + 5*x): ").strip()
    var = input("Digite a variável (ex: x): ").strip()
    
    # Ler ponto como string para permitir símbolos (
    # ex: pi, e, 2*pi, etc.)
    ponto_raw = input("Digite o ponto (ex: 2, 3.5): ").strip()
    ponto = None
    uso_simbolico = False
    try:
        ponto = float(ponto_raw)
    except Exception:
        try:
            import sympy as _sp
            ponto = float(_sp.N(_sp.sympify(ponto_raw)))
            uso_simbolico = True
        except Exception:
            print(f"{Cores.FAIL}❌ Digite um número válido{Cores.ENDC}")
            return
    
    # Valida expressão
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}❌ Expressão inválida: {erro}{Cores.ENDC}")
        return
    
    valor = Derivada.calcular_ponto(expr, var, ponto, ordem=1)
    
    if valor is not None:
        display_point = ponto_raw if uso_simbolico else ponto
        print(f"\n{Cores.OKGREEN}✓ Resultado:{Cores.ENDC}")
        print(f"  f'({display_point}) = {valor:.6g}")
        print(f"\n  📊 Interpretação: Taxa de variação em x = {display_point}")
    else:
        print(f"{Cores.FAIL}❌ Erro ao calcular{Cores.ENDC}")


def _extremos_1var():
    """Encontra e classifica máximos e mínimos para funções de 1 variável."""
    print("\n" + "-"*70)
    print("MÁXIMOS E MÍNIMOS (Uma Variável)")
    print("-"*70)
    
    expr = input("\nDigite a expressão (ex: x**3 - 3*x**2 + 2): ").strip()
    var = input("Digite a variável (ex: x): ").strip()
    
    # Valida expressão
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}❌ Expressão inválida: {erro}{Cores.ENDC}")
        return
    
    # Encontra pontos críticos
    pontos_criticos = Extremos.encontrar_pontos_criticos_1var(expr, var)
    
    if not pontos_criticos:
        print(f"\n{Cores.WARNING}⚠ Nenhum ponto crítico encontrado ou função sem extremos.{Cores.ENDC}")
        return
    
    # Classifica extremos
    extremos = Extremos.classificar_extremos_1var(expr, var, pontos_criticos)
    
    print(f"\n{Cores.OKGREEN}✓ Resultado:{Cores.ENDC}")
    print(f"  Função: f({var}) = {expr}")
    
    if extremos['maximos']:
        print(f"\n  {Cores.BOLD}Máximos Locais:{Cores.ENDC}")
        for x, y in extremos['maximos']:
            print(f"    ({x:.4f}, {y:.4f})")
    
    if extremos['minimos']:
        print(f"\n  {Cores.BOLD}Mínimos Locais:{Cores.ENDC}")
        for x, y in extremos['minimos']:
            print(f"    ({x:.4f}, {y:.4f})")
    
    if extremos['inflexao']:
        print(f"\n  {Cores.BOLD}Pontos de Inflexão:{Cores.ENDC}")
        for x, y in extremos['inflexao']:
            print(f"    ({x:.4f}, {y:.4f})")
    
    plotar = input(f"\n{Cores.OKCYAN}Como exibir o gráfico? (v)er / (s)alvar / (a)uto [padrão v]: {Cores.ENDC}").strip().lower()
    if plotar in ('v', '', 's', 'a'):
        if plotar in ('v', ''):
            salvar = False
        elif plotar == 's':
            salvar = True
        else:
            salvar = None

        intervalo = _obter_intervalo()
        try:
            res = GraficoDerivada.plotar_extremos_1var(expr, var, extremos, intervalo, salvar=salvar)
            if isinstance(res, str):
                print(f"{Cores.OKGREEN}✓ Gráfico salvo em: {res}{Cores.ENDC}")
        except Exception as e:
            print(f"{Cores.FAIL}❌ Erro ao gerar gráfico: {e}{Cores.ENDC}")


def _derivadas_parciais():
    """Calcula derivadas parciais de funções de 2 variáveis."""
    print("\n" + "-"*70)
    print("DERIVADAS PARCIAIS")
    print("-"*70)
    print("\nExemplo: x**2 + 3*x*y + y**2")
    
    expr = input("\nDigite a expressão (use 'x' e 'y'): ").strip()
    
    # Valida expressão
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}❌ Expressão inválida: {erro}{Cores.ENDC}")
        return
    
    # Calcula derivadas parciais
    resultado_x = DerivadaParcial.calcular(expr, 'x', ordem=1)
    resultado_y = DerivadaParcial.calcular(expr, 'y', ordem=1)
    
    if resultado_x and resultado_y:
        orig, df_dx = resultado_x
        _, df_dy = resultado_y
        
        print(f"\n{Cores.OKGREEN}✓ Resultado:{Cores.ENDC}")
        print(f"  Função: f(x,y) = {orig}")
        print(f"  ∂f/∂x = {df_dx}")
        print(f"  ∂f/∂y = {df_dy}")
        
        plotar = input(f"\n{Cores.OKCYAN}Como exibir o gráfico 3D? (v)er / (s)alvar / (a)uto [padrão v]: {Cores.ENDC}").strip().lower()
        if plotar in ('v', '', 's', 'a'):
            if plotar in ('v', ''):
                salvar = False
            elif plotar == 's':
                salvar = True
            else:
                salvar = None

            intervalo = _obter_intervalo()
            try:
                res = GraficoDerivadaParcial.plotar_derivada_parcial(expr, intervalo=intervalo, salvar=salvar)
                if isinstance(res, str):
                    print(f"{Cores.OKGREEN}✓ Gráfico salvo em: {res}{Cores.ENDC}")
            except Exception as e:
                print(f"{Cores.FAIL}❌ Erro ao gerar gráfico: {e}{Cores.ENDC}")
    else:
        print(f"{Cores.FAIL}❌ Erro ao calcular derivadas parciais{Cores.ENDC}")


def _calcular_gradiente():
    """Calcula gradiente de uma função de 2 variáveis."""
    print("\n" + "-"*70)
    print("GRADIENTE (∇f)")
    print("-"*70)
    print("\nO gradiente é o vetor das derivadas parciais: ∇f = (∂f/∂x, ∂f/∂y)")
    
    expr = input("\nDigite a expressão (use 'x' e 'y'): ").strip()
    
    # Valida expressão
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}❌ Expressão inválida: {erro}{Cores.ENDC}")
        return
    
    # Calcula gradiente
    resultado = DerivadaParcial.calcular_gradiente(expr)
    
    if resultado:
        orig, derivadas_list = resultado
        df_dx, df_dy = derivadas_list
        print(f"\n{Cores.OKGREEN}✓ Resultado:{Cores.ENDC}")
        print(f"  Função: f(x,y) = {orig}")
        print(f"  ∇f = ({df_dx}, {df_dy})")
        
        # Calcula gradiente em um ponto
        calcular_ponto = input(f"\n{Cores.OKCYAN}Calcular gradiente em um ponto? (s/n): {Cores.ENDC}").strip().lower()
        if calcular_ponto == 's':
            try:
                x_val = float(input("Digite o valor de x: ").strip())
                y_val = float(input("Digite o valor de y: ").strip())
                
                grad = DerivadaParcial.calcular_gradiente_ponto(expr, {"x": x_val, "y": y_val})
                if grad:
                    df_dx_val, df_dy_val = grad
                    print(f"\n  {Cores.BOLD}Gradiente no ponto ({x_val}, {y_val}):{Cores.ENDC}")
                    print(f"  ∇f = ({df_dx_val:.6g}, {df_dy_val:.6g})")
                    print(f"\n  📊 Interpretação: Direção de maior crescimento da função")
                    
                    visualizar_grad = input(f"\n{Cores.OKCYAN}Como exibir o gradiente? (v)er / (s)alvar / (a)uto [padrão v]: {Cores.ENDC}").strip().lower()
                    if visualizar_grad in ('v', '', 's', 'a'):
                        if visualizar_grad in ('v', ''):
                            salvar = False
                        elif visualizar_grad == 's':
                            salvar = True
                        else:
                            salvar = None

                        intervalo = _obter_intervalo()
                        try:
                            res = GraficoDerivadaParcial.plotar_gradiente_no_ponto(expr, (x_val, y_val), intervalo=intervalo, salvar=salvar)
                            if isinstance(res, str):
                                print(f"{Cores.OKGREEN}✓ Gráfico salvo em: {res}{Cores.ENDC}")
                        except Exception as e:
                            print(f"{Cores.FAIL}❌ Erro ao gerar gráfico: {e}{Cores.ENDC}")
            except ValueError:
                print(f"{Cores.FAIL}❌ Valores inválidos{Cores.ENDC}")
    else:
        print(f"{Cores.FAIL}❌ Erro ao calcular gradiente{Cores.ENDC}")


def _derivada_direcional():
    """Calcula derivada direcional."""
    print("\n" + "-"*70)
    print("DERIVADA DIRECIONAL")
    print("-"*70)
    print("\nA derivada direcional mede a taxa de variação em uma direção específica.")
    
    expr = input("\nDigite a expressão (use 'x' e 'y'): ").strip()
    
    # Valida expressão
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}❌ Expressão inválida: {erro}{Cores.ENDC}")
        return
    
    try:
        x_val = float(input("\nDigite o valor de x do ponto: ").strip())
        y_val = float(input("Digite o valor de y do ponto: ").strip())
        dx = float(input("Digite o componente dx da direção: ").strip())
        dy = float(input("Digite o componente dy da direção: ").strip())
    except ValueError:
        print(f"{Cores.FAIL}❌ Valores inválidos{Cores.ENDC}")
        return
    
    # Calcula derivada direcional
    derivada_dir = DerivadaDirecional.calcular_direcional(
        expr, [dx, dy], {"x": x_val, "y": y_val}
    )
    
    if derivada_dir is not None:
        print(f"\n{Cores.OKGREEN}✓ Resultado:{Cores.ENDC}")
        print(f"  Função: f(x,y) = {expr}")
        print(f"  Ponto: ({x_val}, {y_val})")
        print(f"  Direção: ({dx}, {dy})")
        print(f"  D_u(f) = {derivada_dir:.6g}")
        print(f"\n  📊 Interpretação: Taxa de variação na direção especificada")
    else:
        print(f"{Cores.FAIL}❌ Erro ao calcular derivada direcional{Cores.ENDC}")


def _extremos_2var():
    """Encontra e classifica extremos para funções de 2 variáveis."""
    print("\n" + "-"*70)
    print("EXTREMOS EM 2 VARIÁVEIS (Máximos/Mínimos/Sela)")
    print("-"*70)
    print("\nExemplo: x**2 + y**2 - 2*x - 4*y + 5")
    
    expr = input("\nDigite a expressão (use 'x' e 'y'): ").strip()
    
    # Valida expressão
    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}❌ Expressão inválida: {erro}{Cores.ENDC}")
        return
    
    # Encontra pontos críticos
    pontos_criticos = Extremos.encontrar_pontos_criticos_2var(expr)
    
    if not pontos_criticos:
        print(f"\n{Cores.WARNING}⚠ Nenhum ponto crítico encontrado.{Cores.ENDC}")
        return
    
    print(f"\n{Cores.OKGREEN}✓ Resultado:{Cores.ENDC}")
    print(f"  Função: f(x,y) = {expr}")
    print(f"\n  {Cores.BOLD}Pontos Críticos:{Cores.ENDC}")
    
    for x, y in pontos_criticos:
        classificacao = Extremos.teste_hessiana_2var(expr, (x, y))
        
        print(f"\n  Ponto: ({x:.4f}, {y:.4f})")
        print(f"  Classificação: {classificacao.upper()}")
        
        # Calcula valor da função no ponto
        import sympy as sp
        x_sym, y_sym = sp.symbols('x y')
        f = EngineCalculo._parse(expr)
        f_val = float(f.subs({x_sym: x, y_sym: y}))
        print(f"  f({x:.4f}, {y:.4f}) = {f_val:.6g}")
    
    plotar = input(f"\n{Cores.OKCYAN}Como exibir o gráfico 3D? (v)er / (s)alvar / (a)uto [padrão v]: {Cores.ENDC}").strip().lower()
    if plotar in ('v', '', 's', 'a'):
        if plotar in ('v', ''):
            salvar = False
        elif plotar == 's':
            salvar = True
        else:
            salvar = None

        intervalo = _obter_intervalo()
        try:
            res = GraficoDerivada.plotar_funcao_2var(expr, intervalo=intervalo, tipo_plot='surface', salvar=salvar)
            if isinstance(res, str):
                print(f"{Cores.OKGREEN}✓ Gráfico salvo em: {res}{Cores.ENDC}")
        except Exception as e:
            print(f"{Cores.FAIL}❌ Erro ao gerar gráfico: {e}{Cores.ENDC}")


def _obter_intervalo():
    """Obtém intervalo do usuário para plotagem."""
    try:
        print("\n{} Intervalo para o gráfico: {}".format(Cores.OKCYAN, Cores.ENDC))
        min_val = float(input("  Valor mínimo (padrão -10): ").strip() or "-10")
        max_val = float(input("  Valor máximo (padrão 10): ").strip() or "10")
        return (min_val, max_val)
    except ValueError:
        print(f"{Cores.WARNING}⚠ Usando intervalo padrão (-10, 10){Cores.ENDC}")
        return (-10, 10)


def _ler_valor_real(valor_raw: str):
    """Converte entrada textual em numero real, aceitando pi, e, etc."""
    try:
        return float(valor_raw)
    except Exception:
        try:
            import sympy as sp
            valor = EngineCalculo._parse(valor_raw)
            if getattr(valor, 'is_real', None) is False:
                return None
            return float(sp.N(valor))
        except Exception:
            return None


def _calcular_reta_tangente():
    """Calcula a reta tangente de uma funcao de uma variavel."""
    print("\n" + "-" * 70)
    print("RETA TANGENTE (UMA VARIAVEL)")
    print("-" * 70)

    expr = input("\nDigite a expressao (ex: x**2 + 3*x + 1): ").strip()
    var = input("Digite a variavel (ex: x): ").strip()
    ponto_raw = input("Digite o ponto de tangencia (ex: 2, pi): ").strip()

    ponto = _ler_valor_real(ponto_raw)
    if ponto is None:
        print(f"{Cores.FAIL}Erro: digite um ponto real valido.{Cores.ENDC}")
        return

    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}Erro: expressao invalida: {erro}{Cores.ENDC}")
        return

    resultado = Derivada.calcular_reta_tangente(expr, var, ponto_raw)
    if not resultado:
        print(f"{Cores.FAIL}Erro ao calcular reta tangente.{Cores.ENDC}")
        return

    print(f"\n{Cores.OKGREEN}Resultado:{Cores.ENDC}")
    print(f"  Funcao: f({var}) = {resultado['funcao']}")
    print(f"  Ponto: {var} = {ponto_raw}")
    print(f"  f({ponto_raw}) = {resultado['valor_ponto']}")
    print(f"  Coeficiente angular: {resultado['coef_angular']}")
    print(f"  Reta tangente: y = {resultado['equacao']}")

    plotar = input(
        f"\n{Cores.OKCYAN}Como exibir o grafico? (v)er / (s)alvar / (a)uto [padrao v]: {Cores.ENDC}"
    ).strip().lower()
    if plotar in ('v', ''):
        salvar = False
    elif plotar == 's':
        salvar = True
    else:
        salvar = None

    intervalo = _obter_intervalo()
    try:
        res = GraficoDerivada.plotar_reta_tangente_1var(expr, var, ponto, intervalo=intervalo, salvar=salvar)
        if isinstance(res, str):
            print(f"{Cores.OKGREEN}Grafico salvo em: {res}{Cores.ENDC}")
    except Exception as e:
        print(f"{Cores.FAIL}Erro ao gerar grafico: {e}{Cores.ENDC}")


def _calcular_plano_tangente():
    """Calcula o plano tangente de uma funcao de duas variaveis."""
    print("\n" + "-" * 70)
    print("PLANO TANGENTE (DUAS VARIAVEIS)")
    print("-" * 70)
    print("\nExemplo: x**2 + x*y + y**2")

    expr = input("\nDigite a expressao (use 'x' e 'y'): ").strip()
    x_raw = input("Digite o ponto x0 (ex: 1, pi): ").strip()
    y_raw = input("Digite o ponto y0 (ex: 2, e): ").strip()

    x_val = _ler_valor_real(x_raw)
    y_val = _ler_valor_real(y_raw)
    if x_val is None or y_val is None:
        print(f"{Cores.FAIL}Erro: digite valores reais validos para o ponto.{Cores.ENDC}")
        return

    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}Erro: expressao invalida: {erro}{Cores.ENDC}")
        return

    resultado = DerivadaParcial.calcular_plano_tangente(expr, {"x": x_raw, "y": y_raw})
    if not resultado:
        print(f"{Cores.FAIL}Erro ao calcular plano tangente.{Cores.ENDC}")
        return

    print(f"\n{Cores.OKGREEN}Resultado:{Cores.ENDC}")
    print(f"  Funcao: f(x,y) = {resultado['funcao']}")
    print(f"  Ponto: ({resultado['ponto_x']}, {resultado['ponto_y']}, {resultado['valor_ponto']})")
    print(f"  df/dx no ponto = {resultado['df_dx_ponto']}")
    print(f"  df/dy no ponto = {resultado['df_dy_ponto']}")
    print(f"  Plano tangente: z = {resultado['equacao']}")

    plotar = input(
        f"\n{Cores.OKCYAN}Como exibir o grafico 3D? (v)er / (s)alvar / (a)uto [padrao v]: {Cores.ENDC}"
    ).strip().lower()
    if plotar in ('v', ''):
        salvar = False
    elif plotar == 's':
        salvar = True
    else:
        salvar = None

    intervalo = _obter_intervalo()
    try:
        res = GraficoDerivadaParcial.plotar_plano_tangente_2var(
            expr,
            (x_val, y_val),
            intervalo=intervalo,
            salvar=salvar,
        )
        if isinstance(res, str):
            print(f"{Cores.OKGREEN}Grafico salvo em: {res}{Cores.ENDC}")
    except Exception as e:
        print(f"{Cores.FAIL}Erro ao gerar grafico: {e}{Cores.ENDC}")


def menu_derivadas_com_tangentes():
    """Menu interativo com opcoes de reta e plano tangente."""
    while True:
        print("\n" + "=" * 70)
        print("                          DERIVADAS")
        print("=" * 70)
        print(f"\n{Cores.BOLD}Funcoes de Uma Variavel:{Cores.ENDC}")
        print("  1. Derivada Simples (1a Ordem)")
        print("  2. Derivada de Ordem Superior")
        print("  3. Valor da Derivada em um Ponto")
        print("  4. Reta Tangente (uma variavel)")
        print("  5. Maximos e Minimos (uma variavel)")

        print(f"\n{Cores.BOLD}Funcoes de Multiplas Variaveis:{Cores.ENDC}")
        print("  6. Derivadas Parciais")
        print("  7. Gradiente")
        print("  8. Plano Tangente (duas variaveis)")
        print("  9. Derivada Direcional")
        print("  10. Extremos em 2 Variaveis (Maximos/Minimos/Sela)")

        print(f"\n  {Cores.OKBLUE}0{Cores.ENDC}. Voltar ao Menu Anterior\n")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == '0':
            break
        elif escolha == '1':
            _calcular_derivada_simples()
        elif escolha == '2':
            _calcular_derivada_ordem_superior()
        elif escolha == '3':
            _calcular_derivada_ponto()
        elif escolha == '4':
            _calcular_reta_tangente()
        elif escolha == '5':
            _extremos_1var()
        elif escolha == '6':
            _derivadas_parciais()
        elif escolha == '7':
            _calcular_gradiente()
        elif escolha == '8':
            _calcular_plano_tangente()
        elif escolha == '9':
            _derivada_direcional()
        elif escolha == '10':
            _extremos_2var()
        else:
            print(f"{Cores.FAIL}Erro: opcao invalida!{Cores.ENDC}")


menu_derivadas = menu_derivadas_com_tangentes
