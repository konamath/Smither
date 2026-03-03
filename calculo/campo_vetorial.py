"""
Visualizacao de campo vetorial para funcoes de duas variaveis.
"""

from .engine import EngineCalculo, DerivadaParcial
from .graficos import GraficoDerivadaParcial


class Cores:
    """Cores para terminal."""

    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def menu_campo_vetorial():
    """Coleta dados do usuario e plota o campo vetorial do gradiente."""
    print("\n" + "-" * 70)
    print("CAMPO VETORIAL (GRADIENTE)")
    print("-" * 70)
    print("\nUse uma funcao escalar de duas variaveis, com x e y.")
    print("O grafico exibido sera o mapa da funcao com o campo vetorial de ∇f.")
    print("Exemplo: x**2 + y**2")

    expr = input("\nDigite a expressao (use 'x' e 'y'): ").strip()

    valida, erro = EngineCalculo.validar_expressao(expr)
    if not valida:
        print(f"{Cores.FAIL}Erro: expressao invalida: {erro}{Cores.ENDC}")
        return

    resultado = DerivadaParcial.calcular_gradiente(expr)
    if not resultado:
        print(f"{Cores.FAIL}Erro: nao foi possivel calcular o gradiente.{Cores.ENDC}")
        return

    _, derivadas_list = resultado
    df_dx, df_dy = derivadas_list

    print(f"\n{Cores.OKGREEN}Resultado:{Cores.ENDC}")
    print(f"  Funcao: f(x,y) = {expr}")
    print(f"  Campo vetorial exibido: ∇f = ({df_dx}, {df_dy})")

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
        res = GraficoDerivadaParcial.plotar_campo_gradiente_2var(
            expr,
            intervalo=intervalo,
            salvar=salvar,
        )
        if isinstance(res, str):
            print(f"{Cores.OKGREEN}Grafico salvo em: {res}{Cores.ENDC}")
    except Exception as e:
        print(f"{Cores.FAIL}Erro ao gerar grafico: {e}{Cores.ENDC}")


def _obter_intervalo():
    """Le intervalo do grafico."""
    try:
        print(f"\n{Cores.OKCYAN}Intervalo para o grafico:{Cores.ENDC}")
        min_val = float(input("  Valor minimo (padrao -5): ").strip() or "-5")
        max_val = float(input("  Valor maximo (padrao 5): ").strip() or "5")
        return (min_val, max_val)
    except ValueError:
        print(f"{Cores.WARNING}Usando intervalo padrao (-5, 5){Cores.ENDC}")
        return (-5, 5)
