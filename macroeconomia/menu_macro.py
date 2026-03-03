"""
Menu de Macroeconomia - Smither
===============================
Interface interativa para ferramentas de macroeconomia.
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


def menu_macro():
    """Menu principal de macroeconomia."""
    
    while True:
        print("\n" + "="*70)
        print("                      MACROECONOMIA")
        print("="*70)
        print("\n  Contas Nacionais:")
        print("    1. Produto Interno Bruto (PIB)")
        print("    2. Componentes do PIB")
        print("    3. Índices de preço")
        
        print("\n  Moeda e Inflação:")
        print("    4. Oferta e demanda de moeda")
        print("    5. Taxa de inflação")
        print("    6. Política monetária")
        
        print("\n  Crescimento Econômico:")
        print("    7. Modelo de Solow")
        print("    8. Crescimento endógeno")
        print("    9. Produtividade")
        
        print(f"\n  {Cores.OKBLUE}0{Cores.ENDC}. Voltar ao Menu Anterior\n")
        
        escolha = input("Escolha uma opcao: ").strip()
        
        if escolha == '0':
            break
        elif escolha == '1':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Produto Interno Bruto (PIB){Cores.ENDC}")
        elif escolha == '2':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Componentes do PIB{Cores.ENDC}")
        elif escolha == '3':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] \u00cdndices de preço{Cores.ENDC}")
        elif escolha == '4':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Oferta e demanda de moeda{Cores.ENDC}")
        elif escolha == '5':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Taxa de infla\u00e7\u00e3o{Cores.ENDC}")
        elif escolha == '6':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Pol\u00edtica monet\u00e1ria{Cores.ENDC}")
        elif escolha == '7':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Modelo de Solow{Cores.ENDC}")
        elif escolha == '8':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Crescimento end\u00f3geno{Cores.ENDC}")
        elif escolha == '9':
            print(f"\n{Cores.WARNING}[Em desenvolvimento] Produtividade{Cores.ENDC}")
        else:
            print(f"{Cores.FAIL}[Erro] Opcao invalida!{Cores.ENDC}")
