"""
════════════════════════════════════════════════════════════════════════════════
                              SMITHER - CALCULADORA ECONÔMICA
                    Ferramenta Integrada de Cálculo para Economistas
════════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import importlib
from pathlib import Path

# Configuração de cores para terminal
class Cores:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SmitherMotor:
    """Motor central do Smither que gerencia todos os módulos de cálculo."""
    
    def __init__(self):
        self.modulos = {}
        self.caminho_base = Path(__file__).parent
        self._carregar_modulos()
    
    def _carregar_modulos(self):
        """
        Carrega automaticamente todos os módulos disponíveis.
        Busca por pastas com arquivo 'menu_*.py' no diretório raiz.
        """
        for pasta in self.caminho_base.iterdir():
            if not pasta.is_dir():
                continue
            
            # Ignora pastas ocultas e __pycache__
            if pasta.name.startswith('_') or pasta.name.startswith('.'):
                continue
            
            # Procura por arquivo menu_*.py
            for arquivo in pasta.iterdir():
                if arquivo.name.startswith('menu_') and arquivo.suffix == '.py':
                    nome_modulo = pasta.name
                    try:
                        # Importa o módulo dinamicamente
                        modulo = importlib.import_module(f'{nome_modulo}.{arquivo.stem}')
                        
                        # Armazena referência do módulo
                        self.modulos[nome_modulo] = {
                            'modulo': modulo,
                            'arquivo': arquivo.name,
                            'caminho': str(pasta)
                        }
                    except Exception as e:
                        print(f"{Cores.FAIL}⚠ Erro ao carregar '{nome_modulo}': {e}{Cores.ENDC}")
                    break
    
    def obter_modulos_ordenados(self):
        """Retorna lista de módulos ordenada alfabeticamente."""
        return sorted(self.modulos.keys())
    
    def executar_modulo(self, nome_modulo):
        """
        Executa o menu principal de um módulo específico.
        """
        if nome_modulo not in self.modulos:
            print(f"{Cores.FAIL}Módulo '{nome_modulo}' não encontrado.{Cores.ENDC}")
            return
        
        modulo = self.modulos[nome_modulo]['modulo']
        
        # Tenta executar função 'menu()' do módulo
        if hasattr(modulo, 'menu'):
            try:
                modulo.menu()
            except Exception as e:
                print(f"{Cores.FAIL}Erro ao executar menu de '{nome_modulo}': {e}{Cores.ENDC}")
        else:
            print(f"{Cores.WARNING}Módulo '{nome_modulo}' não possui função 'menu()'{Cores.ENDC}")


def exibir_guia_sintaxe():
    """Exibe um guia rápido da sintaxe matemática aceita pelo projeto."""
    print(f"\n{Cores.BOLD}GUIA DE SINTAXE MATEMÁTICA{Cores.ENDC}\n")
    print("Estas são as formas recomendadas para escrever expressões:")
    print("")
    print(f"{Cores.OKBLUE}Variáveis:{Cores.ENDC}")
    print("  x, y, z")
    print("  Exemplos: x**2, 3x, 2xy, x*y")
    print("")
    print(f"{Cores.OKBLUE}Operações básicas:{Cores.ENDC}")
    print("  Soma:           a + b")
    print("  Subtração:      a - b")
    print("  Multiplicação:  a*b  ou  3x")
    print("  Divisão:        a/b")
    print("  Potência:       x**2")
    print("  Parênteses:     (x + 1)*(x - 1)")
    print("")
    print(f"{Cores.OKBLUE}Constantes:{Cores.ENDC}")
    print("  e ou E          constante de Euler")
    print("  pi ou Pi        número pi")
    print("  oo              infinito")
    print("")
    print(f"{Cores.OKBLUE}Exponenciais e logaritmos:{Cores.ENDC}")
    print("  exp(x)          e**x")
    print("  e**x            exponencial com base e")
    print("  log(x)          logaritmo natural")
    print("  log(x, 10)      logaritmo em outra base")
    print("  sqrt(x)         raiz quadrada")
    print("")
    print(f"{Cores.OKBLUE}Trigonométricas:{Cores.ENDC}")
    print("  sin(x), cos(x), tan(x)")
    print("  asin(x), acos(x), atan(x)")
    print("  Também funciona em casos simples: sinx, cosx, tanx")
    print("")
    print(f"{Cores.OKBLUE}Hiperbólicas:{Cores.ENDC}")
    print("  sinh(x), cosh(x), tanh(x)")
    print("")
    print(f"{Cores.OKBLUE}Outras funções úteis:{Cores.ENDC}")
    print("  abs(x)          valor absoluto")
    print("  factorial(n)    fatorial")
    print("  sign(x)         sinal")
    print("  Outras funções do SymPy também podem funcionar")
    print("  se forem escritas com parênteses, como sec(x)")
    print("")
    print(f"{Cores.OKBLUE}Exemplos válidos:{Cores.ENDC}")
    print("  e**x")
    print("  exp(-x**2)")
    print("  sin(x) + cos(x)")
    print("  log(x) / x")
    print("  sqrt(x**2 + 1)")
    print("  x**3 - 3x + 2")
    print("")
    print(f"{Cores.WARNING}Dica NumPy:{Cores.ENDC} em código Python com NumPy, use")
    print("np.exp(x), np.sin(x), np.cos(x), np.tan(x), np.pi e np.e.")


def exibir_cabecalho():
    """Exibe o cabeçalho da aplicação."""
    print(f"\n{Cores.HEADER}{Cores.BOLD}")
    print("════════════════════════════════════════════════════════════════════════════════")
    print("                              SMITHER - CALCULADORA ECONÔMICA")
    print("                    Ferramenta Integrada de Cálculo para Economistas")
    print("════════════════════════════════════════════════════════════════════════════════")
    print(f"{Cores.ENDC}\n")


def exibir_menu_principal(motor):
    """Exibe o menu principal com todos os módulos disponíveis."""
    modulos = motor.obter_modulos_ordenados()
    
    if not modulos:
        print(f"{Cores.FAIL}Nenhum módulo disponível.{Cores.ENDC}")
        return None
    
    print(f"{Cores.BOLD}Módulos Disponíveis:{Cores.ENDC}\n")
    
    for idx, modulo in enumerate(modulos, 1):
        # Formata o nome do módulo de forma legível
        nome_formatado = modulo.replace('_', ' ').title()
        print(f"  {Cores.OKBLUE}{idx}{Cores.ENDC}. {nome_formatado}")
    
    opcao_guia = len(modulos) + 1
    print(f"  {Cores.OKBLUE}{opcao_guia}{Cores.ENDC}. Guia de Sintaxe Matemática")
    print(f"  {Cores.OKBLUE}0{Cores.ENDC}. Sair\n")
    
    try:
        escolha = input(f"{Cores.OKCYAN}Escolha uma opção: {Cores.ENDC}").strip()
        
        if escolha == '0':
            return None
        
        idx = int(escolha) - 1
        if idx == len(modulos):
            return "guia"
        if 0 <= idx < len(modulos):
            return modulos[idx]
        else:
            print(f"{Cores.FAIL}Opção inválida!{Cores.ENDC}")
            return "invalido"
    
    except ValueError:
        print(f"{Cores.FAIL}Por favor, digite um número válido.{Cores.ENDC}")
        return "invalido"


def exibir_menu_principal_ordenado(motor):
    """Exibe o menu principal com o guia na primeira opção."""
    modulos = motor.obter_modulos_ordenados()

    print(f"{Cores.BOLD}Módulos Disponíveis:{Cores.ENDC}\n")
    print(f"  {Cores.OKBLUE}1{Cores.ENDC}. Guia de Sintaxe Matemática")

    if not modulos:
        print(f"\n{Cores.FAIL}Nenhum módulo disponível.{Cores.ENDC}")

    for idx, modulo in enumerate(modulos, 2):
        nome_formatado = modulo.replace('_', ' ').title()
        print(f"  {Cores.OKBLUE}{idx}{Cores.ENDC}. {nome_formatado}")

    print(f"  {Cores.OKBLUE}0{Cores.ENDC}. Sair\n")

    try:
        escolha = input(f"{Cores.OKCYAN}Escolha uma opção: {Cores.ENDC}").strip()

        if escolha == '0':
            return None

        if escolha == '1':
            return "guia"

        idx = int(escolha) - 2
        if 0 <= idx < len(modulos):
            return modulos[idx]

        print(f"{Cores.FAIL}Opção inválida!{Cores.ENDC}")
        return "invalido"

    except ValueError:
        print(f"{Cores.FAIL}Por favor, digite um número válido.{Cores.ENDC}")
        return "invalido"


def menu_principal():
    """Loop principal da aplicação."""
    motor = SmitherMotor()
    
    while True:
        exibir_cabecalho()
        escolha = exibir_menu_principal_ordenado(motor)
        
        if escolha is None:
            print(f"{Cores.OKGREEN}Obrigado por usar Smither!{Cores.ENDC}\n")
            break
        elif escolha == "guia":
            exibir_guia_sintaxe()
            input(f"\n{Cores.WARNING}Pressione ENTER para voltar ao menu...{Cores.ENDC}")
        elif escolha == "invalido":
            input(f"{Cores.WARNING}Pressione ENTER para continuar...{Cores.ENDC}")
            continue
        else:
            motor.executar_modulo(escolha)
            input(f"\n{Cores.WARNING}Pressione ENTER para voltar ao menu...{Cores.ENDC}")


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(f"\n{Cores.FAIL}Programa interrompido pelo usuário.{Cores.ENDC}\n")
        sys.exit(0)
