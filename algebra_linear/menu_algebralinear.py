"""
Modulo de Algebra Linear - Smither
==================================
Operacoes basicas com matrizes e resolucao de sistemas lineares.
"""

import os
from datetime import datetime
from pathlib import Path
from fractions import Fraction


class Cores:
    """Cores para terminal."""

    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def menu_algebra_linear():
    """Menu principal do modulo de algebra linear."""
    while True:
        print("\n" + "=" * 70)
        print("                       ALGEBRA LINEAR")
        print("=" * 70)
        print("\n1. Operacoes Basicas de Matrizes")
        print("2. Sistemas Lineares por Gauss-Jordan")
        print("0. Voltar ao menu anterior\n")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            break
        if escolha == "1":
            _menu_operacoes_matrizes()
        elif escolha == "2":
            _resolver_sistema_gauss_jordan()
        else:
            print(f"{Cores.FAIL}Opcao invalida!{Cores.ENDC}")


def _menu_operacoes_matrizes():
    """Submenu de operacoes basicas de matrizes."""
    while True:
        print("\n" + "-" * 70)
        print("OPERACOES BASICAS DE MATRIZES")
        print("-" * 70)
        print("1. Soma de matrizes")
        print("2. Subtracao de matrizes")
        print("3. Multiplicacao de matrizes")
        print("4. Transposta")
        print("5. Determinante (n x n)")
        print("6. Inversa")
        print("0. Voltar\n")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            break
        if escolha == "1":
            _operacao_soma()
        elif escolha == "2":
            _operacao_subtracao()
        elif escolha == "3":
            _operacao_multiplicacao()
        elif escolha == "4":
            _operacao_transposta()
        elif escolha == "5":
            _operacao_determinante()
        elif escolha == "6":
            _operacao_inversa()
        else:
            print(f"{Cores.FAIL}Opcao invalida!{Cores.ENDC}")


def _operacao_soma():
    print("\nSOMA DE MATRIZES")
    linhas = _ler_inteiro_positivo("Numero de linhas: ")
    colunas = _ler_inteiro_positivo("Numero de colunas: ")
    if linhas is None or colunas is None:
        return

    a = _ler_matriz("A", linhas, colunas)
    b = _ler_matriz("B", linhas, colunas)
    if a is None or b is None:
        return

    resultado = [
        [a[i][j] + b[i][j] for j in range(colunas)]
        for i in range(linhas)
    ]
    _exibir_resultado_matriz("A + B", resultado)


def _operacao_subtracao():
    print("\nSUBTRACAO DE MATRIZES")
    linhas = _ler_inteiro_positivo("Numero de linhas: ")
    colunas = _ler_inteiro_positivo("Numero de colunas: ")
    if linhas is None or colunas is None:
        return

    a = _ler_matriz("A", linhas, colunas)
    b = _ler_matriz("B", linhas, colunas)
    if a is None or b is None:
        return

    resultado = [
        [a[i][j] - b[i][j] for j in range(colunas)]
        for i in range(linhas)
    ]
    _exibir_resultado_matriz("A - B", resultado)


def _operacao_multiplicacao():
    print("\nMULTIPLICACAO DE MATRIZES")
    linhas_a = _ler_inteiro_positivo("Linhas da matriz A: ")
    colunas_a = _ler_inteiro_positivo("Colunas da matriz A: ")
    colunas_b = _ler_inteiro_positivo("Colunas da matriz B: ")
    if linhas_a is None or colunas_a is None or colunas_b is None:
        return

    a = _ler_matriz("A", linhas_a, colunas_a)
    b = _ler_matriz("B", colunas_a, colunas_b)
    if a is None or b is None:
        return

    resultado = []
    for i in range(linhas_a):
        linha = []
        for j in range(colunas_b):
            valor = Fraction(0)
            for k in range(colunas_a):
                valor += a[i][k] * b[k][j]
            linha.append(valor)
        resultado.append(linha)

    _exibir_resultado_matriz("A * B", resultado)


def _operacao_transposta():
    print("\nTRANSPOSTA")
    linhas = _ler_inteiro_positivo("Numero de linhas: ")
    colunas = _ler_inteiro_positivo("Numero de colunas: ")
    if linhas is None or colunas is None:
        return

    matriz = _ler_matriz("A", linhas, colunas)
    if matriz is None:
        return

    resultado = _transposta(matriz)
    _exibir_resultado_matriz("A^T", resultado)


def _operacao_determinante():
    print("\nDETERMINANTE DE MATRIZ (n x n)")
    ordem = _ler_inteiro_positivo("Informe a ordem n da matriz quadrada: ")
    if ordem is None:
        return

    matriz = _ler_matriz("A", ordem, ordem)
    if matriz is None:
        return

    det = _determinante(matriz)
    print(f"\n{Cores.OKGREEN}Resultado:{Cores.ENDC}")
    print(f"det(A) = {_formatar_numero(det)}")


def _operacao_inversa():
    print("\nINVERSA")
    ordem = _ler_inteiro_positivo("Ordem da matriz quadrada: ")
    if ordem is None:
        return

    matriz = _ler_matriz("A", ordem, ordem)
    if matriz is None:
        return

    inversa = _inversa(matriz)
    if inversa is None:
        print(f"{Cores.FAIL}A matriz nao e invertivel.{Cores.ENDC}")
        return

    _exibir_resultado_matriz("A^-1", inversa)


def _resolver_sistema_gauss_jordan():
    """Resolve sistema linear por Gauss-Jordan."""
    print("\n" + "-" * 70)
    print("SISTEMAS LINEARES POR GAUSS-JORDAN")
    print("-" * 70)
    print("Informe a matriz aumentada linha por linha.")
    print("Exemplo de linha para 3 variaveis: 2 1 -1 8")
    print("")
    print("Passo a passo:")
    print("1. Pegue a equacao e mantenha apenas os coeficientes e o termo independente.")
    print("2. Remova as letras x, y, z e os sinais de multiplicacao.")
    print("3. Digite tudo separado por espaco.")
    print("4. O ultimo numero e o valor depois do sinal de igual.")
    print("")
    print("Exemplo:")
    print("  3*x + 1*y - 3*z = 4")
    print("  vira")
    print("  3 1 -3 4")

    equacoes = _ler_inteiro_positivo("Numero de equacoes: ")
    variaveis = _ler_inteiro_positivo("Numero de variaveis: ")
    if equacoes is None or variaveis is None:
        return

    matriz = _ler_matriz_aumentada(equacoes, variaveis)
    if matriz is None:
        return

    resultado = _gauss_jordan_sistema(matriz, variaveis)

    print(f"\n{Cores.OKGREEN}Matriz reduzida (RREF):{Cores.ENDC}")
    print(_formatar_matriz(resultado["rref"]))

    if resultado["status"] == "inconsistente":
        print(f"\n{Cores.FAIL}Sistema impossivel: sem solucao.{Cores.ENDC}")
        return

    if resultado["status"] == "unico":
        print(f"\n{Cores.OKGREEN}Sistema possivel determinado:{Cores.ENDC}")
        for idx, valor in enumerate(resultado["solucao"], 1):
            print(f"  x{idx} = {_formatar_numero(valor)}")
        return

    print(f"\n{Cores.WARNING}Sistema possivel indeterminado:{Cores.ENDC}")
    for linha in resultado["expressoes"]:
        print(f"  {linha}")
    if resultado["livres"]:
        livres = ", ".join(resultado["livres"])
        print(f"  Variaveis livres: {livres}")


def _ler_inteiro_positivo(prompt: str):
    """Le um inteiro positivo do usuario."""
    try:
        valor = int(input(prompt).strip())
        if valor <= 0:
            print(f"{Cores.FAIL}Digite um inteiro positivo.{Cores.ENDC}")
            return None
        return valor
    except ValueError:
        print(f"{Cores.FAIL}Digite um numero inteiro valido.{Cores.ENDC}")
        return None


def _ler_matriz(nome: str, linhas: int, colunas: int):
    """Le uma matriz de dimensao fixa."""
    print(f"\nDigite a matriz {nome} ({linhas}x{colunas}).")
    print("Use numeros separados por espaco. Aceita inteiros, decimais e fracoes.")
    matriz = []

    for idx in range(linhas):
        linha_txt = input(f"Linha {idx + 1}: ").strip().replace(",", " ")
        partes = [p for p in linha_txt.split() if p]
        if len(partes) != colunas:
            print(f"{Cores.FAIL}Cada linha deve ter exatamente {colunas} valores.{Cores.ENDC}")
            return None

        try:
            linha = [_ler_fracao(valor) for valor in partes]
        except ValueError:
            print(f"{Cores.FAIL}Linha invalida. Use apenas numeros reais ou fracoes.{Cores.ENDC}")
            return None
        matriz.append(linha)

    return matriz


def _ler_matriz_aumentada(equacoes: int, variaveis: int):
    """Le a matriz aumentada de um sistema linear."""
    matriz = []
    total_colunas = variaveis + 1

    for idx in range(equacoes):
        linha_txt = input(f"Linha {idx + 1} ({variaveis} coeficientes + termo independente): ").strip()
        partes = [p for p in linha_txt.replace(",", " ").split() if p]
        if len(partes) != total_colunas:
            print(f"{Cores.FAIL}Cada linha deve ter exatamente {total_colunas} valores.{Cores.ENDC}")
            print(f"{Cores.WARNING}Digite apenas numeros separados por espaco.{Cores.ENDC}")
            print(f"{Cores.WARNING}Exemplo: 3*x + y - 3*z = 4  ->  3 1 -3 4{Cores.ENDC}")
            return None

        try:
            linha = [_ler_fracao(valor) for valor in partes]
        except ValueError:
            print(f"{Cores.FAIL}Linha invalida. Use apenas numeros reais ou fracoes.{Cores.ENDC}")
            return None
        matriz.append(linha)

    return matriz


def _ler_fracao(valor: str) -> Fraction:
    """Converte texto em Fraction."""
    return Fraction(valor)


def _transposta(matriz):
    """Retorna a transposta de uma matriz."""
    return [list(coluna) for coluna in zip(*matriz)]


def _determinante(matriz):
    """Calcula o determinante por eliminacao gaussiana."""
    n = len(matriz)
    trabalho = [linha[:] for linha in matriz]
    sinal = 1
    det = Fraction(1)

    for col in range(n):
        pivot = None
        for linha in range(col, n):
            if trabalho[linha][col] != 0:
                pivot = linha
                break

        if pivot is None:
            return Fraction(0)

        if pivot != col:
            trabalho[col], trabalho[pivot] = trabalho[pivot], trabalho[col]
            sinal *= -1

        pivot_valor = trabalho[col][col]
        det *= pivot_valor

        for linha in range(col + 1, n):
            if trabalho[linha][col] == 0:
                continue
            fator = trabalho[linha][col] / pivot_valor
            for k in range(col, n):
                trabalho[linha][k] -= fator * trabalho[col][k]

    return det * sinal


def _inversa(matriz):
    """Calcula a inversa por Gauss-Jordan."""
    n = len(matriz)
    identidade = _matriz_identidade(n)
    aumentada = [matriz[i][:] + identidade[i][:] for i in range(n)]
    rref, pivot_cols = _rref(aumentada, n)

    if len(pivot_cols) != n:
        return None

    for idx in range(n):
        if pivot_cols[idx] != idx:
            return None

    return [linha[n:] for linha in rref]


def _matriz_identidade(n: int):
    """Cria uma matriz identidade."""
    return [
        [Fraction(1 if i == j else 0) for j in range(n)]
        for i in range(n)
    ]


def _rref(matriz, colunas_pivo):
    """Retorna a forma reduzida por linhas e as colunas de pivo."""
    trabalho = [linha[:] for linha in matriz]
    linhas = len(trabalho)
    colunas = len(trabalho[0]) if linhas else 0
    linha_atual = 0
    pivos = []

    for col in range(colunas_pivo):
        pivot = None
        for linha in range(linha_atual, linhas):
            if trabalho[linha][col] != 0:
                pivot = linha
                break

        if pivot is None:
            continue

        if pivot != linha_atual:
            trabalho[linha_atual], trabalho[pivot] = trabalho[pivot], trabalho[linha_atual]

        pivot_valor = trabalho[linha_atual][col]
        trabalho[linha_atual] = [valor / pivot_valor for valor in trabalho[linha_atual]]

        for linha in range(linhas):
            if linha == linha_atual or trabalho[linha][col] == 0:
                continue
            fator = trabalho[linha][col]
            trabalho[linha] = [
                trabalho[linha][idx] - fator * trabalho[linha_atual][idx]
                for idx in range(colunas)
            ]

        pivos.append(col)
        linha_atual += 1
        if linha_atual == linhas:
            break

    return trabalho, pivos


def _gauss_jordan_sistema(matriz_aumentada, variaveis: int):
    """Resolve um sistema linear e classifica o tipo de solucao."""
    rref, pivot_cols = _rref(matriz_aumentada, variaveis)

    for linha in rref:
        if all(valor == 0 for valor in linha[:variaveis]) and linha[variaveis] != 0:
            return {
                "status": "inconsistente",
                "rref": rref,
                "solucao": [],
                "expressoes": [],
                "livres": [],
            }

    if len(pivot_cols) == variaveis:
        solucao = [Fraction(0) for _ in range(variaveis)]
        for linha_idx, pivot_col in enumerate(pivot_cols):
            solucao[pivot_col] = rref[linha_idx][variaveis]
        return {
            "status": "unico",
            "rref": rref,
            "solucao": solucao,
            "expressoes": [],
            "livres": [],
        }

    livres = [idx for idx in range(variaveis) if idx not in pivot_cols]
    expressoes = []
    for linha_idx, pivot_col in enumerate(pivot_cols):
        exp = _montar_expressao_solucao(rref[linha_idx], pivot_col, livres, variaveis)
        expressoes.append(f"x{pivot_col + 1} = {exp}")

    return {
        "status": "infinito",
        "rref": rref,
        "solucao": [],
        "expressoes": expressoes,
        "livres": [f"x{idx + 1}" for idx in livres],
    }


def _montar_expressao_solucao(linha, pivot_col, livres, variaveis):
    """Monta a expressao de uma variavel lider em funcao das livres."""
    partes = []
    constante = linha[variaveis]

    if constante != 0:
        partes.append(_formatar_numero(constante))

    for col in livres:
        coef = -linha[col]
        if coef == 0:
            continue

        termo = _formatar_termo(coef, f"x{col + 1}")
        if not partes:
            partes.append(termo)
        elif termo.startswith("-"):
            partes.append(f"- {termo[1:]}")
        else:
            partes.append(f"+ {termo}")

    if not partes:
        return "0"

    return " ".join(partes)


def _formatar_termo(coef: Fraction, variavel: str) -> str:
    """Formata um termo do tipo a*x."""
    if coef == 1:
        return variavel
    if coef == -1:
        return f"-{variavel}"
    return f"{_formatar_numero(coef)}*{variavel}"


def _exibir_resultado_matriz(titulo: str, matriz):
    """Exibe uma matriz resultado."""
    print(f"\n{Cores.OKGREEN}Resultado ({titulo}):{Cores.ENDC}")
    print(_formatar_matriz(matriz))
    _plotar_vetores_matriz(matriz, titulo)


def _formatar_matriz(matriz) -> str:
    """Formata uma matriz para impressao alinhada."""
    if not matriz:
        return "[]"

    linhas_txt = [[_formatar_numero(valor) for valor in linha] for linha in matriz]
    largura = max(len(item) for linha in linhas_txt for item in linha)

    saida = []
    for linha in linhas_txt:
        conteudo = "  ".join(item.rjust(largura) for item in linha)
        saida.append(f"[ {conteudo} ]")
    return "\n".join(saida)


def _plotar_vetores_matriz(matriz, titulo: str):
    """Gera uma representacao grafica dos vetores-linha do resultado."""
    if not matriz or not matriz[0]:
        return

    colunas = len(matriz[0])
    if any(len(linha) != colunas for linha in matriz):
        print(f"{Cores.WARNING}Nao foi possivel gerar o grafico: matriz irregular.{Cores.ENDC}")
        return

    if colunas == 1:
        vetores_plot = [[_converter_para_float(linha[0]), 0.0] for linha in matriz]
        vetores_legenda = [[_converter_para_float(linha[0])] for linha in matriz]
        dimensao = 2
        print(f"{Cores.OKBLUE}Plotando vetores 1D no plano (eixo y = 0).{Cores.ENDC}")
    elif colunas in (2, 3):
        vetores_plot = [[_converter_para_float(valor) for valor in linha] for linha in matriz]
        vetores_legenda = [vetor[:] for vetor in vetores_plot]
        dimensao = colunas
    else:
        print(f"{Cores.WARNING}Grafico vetorial disponivel apenas para resultados com ate 3 colunas.{Cores.ENDC}")
        return

    try:
        import matplotlib.pyplot as plt
        if dimensao == 3:
            from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    except Exception as exc:
        print(f"{Cores.WARNING}Nao foi possivel carregar o matplotlib: {exc}{Cores.ENDC}")
        return

    cmap = plt.cm.get_cmap('tab10', max(3, len(vetores_plot)))
    cores = [cmap(i % cmap.N) for i in range(len(vetores_plot))]
    limites = _calcular_limites_componentes(vetores_plot, dimensao)

    if dimensao == 2:
        fig, ax = plt.subplots(figsize=(7, 6))
        for idx, vetor in enumerate(vetores_plot):
            cor = cores[idx]
            ax.quiver(0, 0, vetor[0], vetor[1], angles='xy', scale_units='xy', scale=1, color=cor, width=0.006)
            ax.scatter([vetor[0]], [vetor[1]], color=cor)
            rotulo = _formatar_componentes_legenda(vetores_legenda[idx])
            ax.text(vetor[0], vetor[1], f"v{idx + 1} ({rotulo})", fontsize=9, color=cor)

        ax.axhline(0, color='gray', linewidth=0.6)
        ax.axvline(0, color='gray', linewidth=0.6)
        ax.set_xlim(*limites[0])
        ax.set_ylim(*limites[1])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.set_title(f"Representacao Vetorial de {titulo}")
        try:
            ax.set_aspect('equal', adjustable='box')
        except Exception:
            pass
    else:
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        for idx, vetor in enumerate(vetores_plot):
            cor = cores[idx]
            ax.quiver(0, 0, 0, vetor[0], vetor[1], vetor[2], color=cor, arrow_length_ratio=0.1, linewidth=2)
            rotulo = _formatar_componentes_legenda(vetores_legenda[idx])
            ax.text(vetor[0], vetor[1], vetor[2], f"v{idx + 1}\n({rotulo})", fontsize=8, color=cor)

        ax.set_xlim(*limites[0])
        ax.set_ylim(*limites[1])
        ax.set_zlim(*limites[2])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title(f"Representacao Vetorial de {titulo}")
        ax.view_init(elev=18, azim=35)

    _renderizar_grafico(fig, titulo, plt)


def _converter_para_float(valor):
    """Converte Fracoes ou decimais em float para plotagem."""
    try:
        return float(valor)
    except Exception:
        return 0.0


def _calcular_limites_componentes(vetores, dimensao: int):
    """Determina limites dos eixos com uma margem de seguranca."""
    limites = []
    for i in range(dimensao):
        valores = [vetor[i] for vetor in vetores] + [0.0]
        minimo = min(valores)
        maximo = max(valores)
        if minimo == maximo:
            margem = abs(maximo) * 0.3 if maximo != 0 else 1.0
        else:
            margem = max((maximo - minimo) * 0.15, 0.5)
        limites.append((minimo - margem, maximo + margem))
    return limites


def _formatar_componentes_legenda(componentes):
    """Formata uma sequencia numerica para ser exibida junto ao vetor."""
    if not componentes:
        return "0"
    return ", ".join(f"{valor:.2f}" for valor in componentes)


def _renderizar_grafico(fig, titulo: str, plt_module):
    """Define se o grafico deve ser exibido ou salvo em arquivo."""
    do_save = _should_save_plots(plt_module)
    if do_save:
        destino = _ensure_output_dir() / f'vetores_{_sanitize_filename(titulo)}_{_timestamp()}.png'
        fig.savefig(destino, dpi=150, bbox_inches='tight')
        plt_module.close(fig)
        print(f"{Cores.OKGREEN}Grafico salvo em: {destino}{Cores.ENDC}")
    else:
        plt_module.show()
        plt_module.close(fig)


def _ensure_output_dir() -> Path:
    """Garante que exista um diretorio padrao para salvar figuras."""
    destino = Path.cwd() / "outputs"
    destino.mkdir(parents=True, exist_ok=True)
    return destino


def _timestamp() -> str:
    """Timestamp simples para compor o nome do arquivo."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _sanitize_filename(texto: str) -> str:
    """Remove caracteres invalidos dos nomes dos arquivos."""
    base = texto.strip().replace(" ", "_")
    san = "".join(char if char.isalnum() or char in ("-", "_") else "_" for char in base)
    return san or "resultado"


def _should_save_plots(plt_module=None) -> bool:
    """Regras para decidir entre mostrar ou salvar o grafico."""
    backend = None
    if plt_module is not None:
        try:
            backend = plt_module.get_backend()
        except Exception:
            backend = None

    if backend:
        try:
            if "agg" in backend.lower():
                return True
        except Exception:
            pass
    else:
        try:
            import matplotlib
            backend_mat = matplotlib.get_backend()
            if "agg" in backend_mat.lower():
                return True
        except Exception:
            return True

    if os.environ.get("HEADLESS") or os.environ.get("CI"):
        return True
    if os.name != "nt" and not os.environ.get("DISPLAY"):
        return True
    return False


def _formatar_numero(valor: Fraction) -> str:
    """Formata Fraction para exibicao."""
    if valor.denominator == 1:
        return str(valor.numerator)
    return f"{valor.numerator}/{valor.denominator}"


def menu():
    """Alias de entrada do modulo."""
    menu_algebra_linear()


if __name__ == "__main__":
    menu()
