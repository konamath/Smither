"""
Menu Principal do Módulo de Cálculo - Smither
==============================================
Menu de Derivadas e Integrais para análises econômicas.
"""

from . import derivadas
from . import campo_vetorial
from . import integrais
from . import limites


class Cores:
    """Cores para terminal."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def menu_calculo():
    """Menu principal do módulo de Cálculo.

    Exibe opções para escolher Derivadas ou Integrais.
    """
    while True:
        print(f"\n{Cores.HEADER}{Cores.BOLD}")
        print("════════════════════════════════════════════════════════════════════════════════")
        print("                              MÓDULO DE CÁLCULO")
        print("════════════════════════════════════════════════════════════════════════════════")
        print(f"{Cores.ENDC}")
        print(f"\n{Cores.OKBLUE}Escolha uma opção:{Cores.ENDC}")
        print("(1) Derivadas")
        print("(2) Integrais")
        print("(3) Campo Vetorial (Gradiente)")
        print("(4) Limites")
        print("(5) Máximos e Mínimos Condicionais (Lagrange)")
        print("(0) Voltar ao menu principal")
        
        opcao = input(f"\n{Cores.OKGREEN}Digite sua opcao: {Cores.ENDC}").strip()
        
        if opcao == "1":
            derivadas.menu_derivadas()
        elif opcao == "2":
            integrais.menu_integrais()
        elif opcao == "3":
            campo_vetorial.menu_campo_vetorial()
        elif opcao == "4":
            limites.menu_limites()
        elif opcao == "5":
            derivadas.menu_extremos_condicionais()
        elif opcao == "0":
            print(f"\n{Cores.WARNING}Voltando ao menu principal...{Cores.ENDC}")
            return
        else:
            print(f"{Cores.FAIL}Opcao invalida! Tente novamente.{Cores.ENDC}")


def menu():
    """Menu principal do módulo de Cálculo (alias para menu_calculo)."""
    menu_calculo()


if __name__ == "__main__":
    menu()
