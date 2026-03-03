"""Script de utilidade para CI: gera vários plots e salva em `outputs/`.

Executar como pacote é preferível (``python -m tools.generate_plots``), mas o
script também pode ser chamado diretamente. Quando rodado como arquivo ele
adiciona automaticamente a raiz do projeto ao ``sys.path`` para que o
pacote ``calculo`` seja encontrado.
"""
import sys
from pathlib import Path

# garantir que a raiz do repositório esteja no path para permitir import
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from calculo.graficos import GraficoDerivada, GraficoDerivadaParcial
import os


def main():
    os.makedirs('outputs', exist_ok=True)
    saved = []

    try:
        f1 = GraficoDerivada.plotar_funcao_1var('x**2 + 3*x', 'x', intervalo=(-5,5), titulo='ci_test_1', salvar=True)
        saved.append(f1)
    except Exception as e:
        print('Erro plotar_funcao_1var:', e)

    try:
        f2 = GraficoDerivada.plotar_funcao_derivada_1var('x**3 - 3*x', 'x', intervalo=(-5,5), salvar=True)
        saved.append(f2)
    except Exception as e:
        print('Erro plotar_funcao_derivada_1var:', e)

    try:
        f3 = GraficoDerivada.plotar_funcao_2var('x**2 + y**2', intervalo=(-3,3), tipo_plot='contour', salvar=True)
        saved.append(f3)
    except Exception as e:
        print('Erro plotar_funcao_2var:', e)

    try:
        extremos = {'maximos': [], 'minimos': [(0.0, 0.0)], 'inflexao': []}
        f4 = GraficoDerivada.plotar_extremos_1var('x**3 - 3*x', 'x', extremos, intervalo=(-3,3), salvar=True)
        saved.append(f4)
    except Exception as e:
        print('Erro plotar_extremos_1var:', e)

    try:
        f5 = GraficoDerivadaParcial.plotar_gradiente_no_ponto('x**2 + y**2', (1,1), intervalo=(-3,3), salvar=True)
        saved.append(f5)
    except Exception as e:
        print('Erro plotar_gradiente_no_ponto:', e)

    print('\nArquivos gerados:')
    for p in saved:
        print(' -', p, 'exists=', os.path.exists(p) if p else False)


if __name__ == '__main__':
    main()
