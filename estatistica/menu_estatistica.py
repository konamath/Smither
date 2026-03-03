"""
Menu de Estatística - Smither
=============================
Interface interativa para ferramentas estatísticas.
"""


class Cores:
    """Cores para terminal."""
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def menu_estatistica():
    """Menu principal de estatística."""
    
    while True:
        print("\n" + "="*70)
        print("                        ESTATÍSTICA")
        print("="*70)
        print("\n  Estatística Descritiva:")
        print("    1. Medidas de tendência central (média, mediana, moda)")
        print("    2. Medidas de dispersão (variância, desvio padrão)")
        print("    3. Análise de distribuição")
        
        print("\n  Teste de Hipóteses:")
        print("    4. Teste t")
        print("    5. Teste chi-quadrado")
        print("    6. ANOVA")
        
        print("\n  Regressão:")
        print("    7. Regressão linear simples")
        print("    8. Regressão múltipla")
        
        print(f"\n  {Cores.OKBLUE}0{Cores.ENDC}. Voltar ao Menu Anterior\n")
        
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == '0':
            break
        elif escolha == '1':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Medidas de tendência central{Cores.ENDC}")
        elif escolha == '2':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Medidas de dispersão{Cores.ENDC}")
        elif escolha == '3':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Análise de distribuição{Cores.ENDC}")
        elif escolha == '4':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Teste t{Cores.ENDC}")
        elif escolha == '5':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Teste chi-quadrado{Cores.ENDC}")
        elif escolha == '6':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] ANOVA{Cores.ENDC}")
        elif escolha == '7':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Regressão linear simples{Cores.ENDC}")
        elif escolha == '8':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Regressão múltipla{Cores.ENDC}")
        else:
            print(f"{Cores.FAIL}[Erro] Opcao invalida!{Cores.ENDC}")
