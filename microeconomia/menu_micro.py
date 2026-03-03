"""
Menu de Microeconomia - Smither
===============================
Interface interativa para ferramentas de microeconomia.
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


def menu_micro():
    """Menu principal de microeconomia."""
    
    while True:
        print("\n" + "="*70)
        print("                      MICROECONOMIA")
        print("="*70)
        print("\n  Teoria do Consumidor:")
        print("    1. Curvas de indiferença")
        print("    2. Restrição orçamentária")
        print("    3. Escolha ótima do consumidor")
        
        print("\n  Teoria da Produção:")
        print("    4. Funções de produção")
        print("    5. Isoquantas e caminho de expansão")
        print("    6. Custos de produção")
        
        print("\n  Mercados:")
        print("    7. Concorrência perfeita")
        print("    8. Monopólio")
        print("    9. Oligopólio")
        
        print(f"\n  {Cores.OKBLUE}0{Cores.ENDC}. Voltar ao Menu Anterior\n")
        
        escolha = input("Escolha uma opcao: ").strip()
        
        if escolha == '0':
            break
        elif escolha == '1':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Curvas de indiferen\u00e7a{Cores.ENDC}")
        elif escolha == '2':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Restri\u00e7\u00e3o or\u00e7ament\u00e1ria{Cores.ENDC}")
        elif escolha == '3':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Escolha \u00f3tima do consumidor{Cores.ENDC}")
        elif escolha == '4':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Fun\u00e7\u00f5es de produ\u00e7\u00e3o{Cores.ENDC}")
        elif escolha == '5':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Isoquantas e caminho de expans\u00e3o{Cores.ENDC}")
        elif escolha == '6':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Custos de produ\u00e7\u00e3o{Cores.ENDC}")
        elif escolha == '7':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Concorr\u00eancia perfeita{Cores.ENDC}")
        elif escolha == '8':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Monop\u00f3lio{Cores.ENDC}")
        elif escolha == '9':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Oligop\u00f3lio{Cores.ENDC}")
        else:
            print(f"{Cores.FAIL}[Erro] Opcao invalida!{Cores.ENDC}")
