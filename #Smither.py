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
    
    print(f"  {Cores.OKBLUE}0{Cores.ENDC}. Sair\n")
    
    try:
        escolha = input(f"{Cores.OKCYAN}Escolha uma opção: {Cores.ENDC}").strip()
        
        if escolha == '0':
            return None
        
        idx = int(escolha) - 1
        if 0 <= idx < len(modulos):
            return modulos[idx]
        else:
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
        escolha = exibir_menu_principal(motor)
        
        if escolha is None:
            print(f"{Cores.OKGREEN}Obrigado por usar Smither!{Cores.ENDC}\n")
            break
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
