"""
Menu de Microeconomia - Smither
===============================
Interface interativa para ferramentas de microeconomia.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import matplotlib

def _sem_sessao_grafica_unix() -> bool:
    if os.name == "nt":
        return False
    if sys.platform == "darwin":
        return False
    return not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def _terminal_interativo_disponivel() -> bool:
    try:
        return bool(sys.stdin.isatty() and sys.stdout.isatty())
    except Exception:
        return False


def _deve_forcar_backend_agg() -> bool:
    if os.environ.get("HEADLESS") or os.environ.get("CI"):
        return True
    if not _terminal_interativo_disponivel():
        return True
    return _sem_sessao_grafica_unix()


if _deve_forcar_backend_agg():
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import sympy as sp

try:
    from .consumidor import (
        AnaliseUtilidade,
        analisar_utilidade,
        calcular_cesta_otima,
        classificar_bens,
        criar_avaliador_utilidade,
        formatar_expr,
        substituir_utilidade,
    )
except ImportError:
    from consumidor import (
        AnaliseUtilidade,
        analisar_utilidade,
        calcular_cesta_otima,
        classificar_bens,
        criar_avaliador_utilidade,
        formatar_expr,
        substituir_utilidade,
    )


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
    sessao_consumidor = None

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
            _plotar_restricoes_orcamentarias()
        elif escolha == '3':
            sessao_consumidor = _menu_consumidor(sessao_consumidor)
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


def _menu_consumidor(analise_atual: AnaliseUtilidade | None) -> AnaliseUtilidade | None:
    """Submenu de teoria do consumidor baseado em funcao utilidade."""
    analise = analise_atual

    while True:
        print("\n" + "-"*70)
        print("ANALISE DE UTILIDADE E ESCOLHA OTIMA")
        print("-"*70)
        if analise is None:
            print("Utilidade atual: nenhuma funcao carregada.")
        else:
            print(f"Utilidade atual: U(x, y) = {formatar_expr(analise.utilidade)}")

        print("\n  1. Informar/atualizar funcao utilidade")
        print("  2. Exibir demandas marshallianas")
        print("  3. Classificar bens")
        print("  4. Calcular cesta otima para precos e renda")
        print("  5. Limpar utilidade atual")
        print(f"\n  {Cores.OKBLUE}0{Cores.ENDC}. Voltar\n")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == '0':
            return analise
        if escolha == '1':
            texto = input("Informe U(x, y): ").strip()
            if not texto:
                print(f"{Cores.WARNING}Informe uma utilidade valida.{Cores.ENDC}")
                continue
            try:
                analise = analisar_utilidade(texto)
            except ValueError as exc:
                print(f"{Cores.FAIL}{exc}{Cores.ENDC}")
                continue
            _exibir_analise_utilidade(analise)
        elif escolha == '2':
            if analise is None:
                print(f"{Cores.WARNING}Primeiro informe uma funcao utilidade.{Cores.ENDC}")
                continue
            _exibir_analise_utilidade(analise)
        elif escolha == '3':
            if analise is None:
                print(f"{Cores.WARNING}Primeiro informe uma funcao utilidade.{Cores.ENDC}")
                continue
            _exibir_classificacao_bens(analise)
        elif escolha == '4':
            if analise is None:
                print(f"{Cores.WARNING}Primeiro informe uma funcao utilidade.{Cores.ENDC}")
                continue
            _exibir_cesta_otima(analise)
        elif escolha == '5':
            analise = None
            print(f"{Cores.OKGREEN}Funcao utilidade removida da sessao atual.{Cores.ENDC}")
        else:
            print(f"{Cores.FAIL}[Erro] Opcao invalida!{Cores.ENDC}")


def _exibir_analise_utilidade(analise: AnaliseUtilidade):
    """Exibe utilidade, metodo e demandas marshallianas."""
    print("\n" + "-"*70)
    print("RESULTADO DA ANALISE DA UTILIDADE")
    print("-"*70)
    print(f"U(x, y) = {formatar_expr(analise.utilidade)}")
    print(f"Metodo: {_rotulo_metodo_consumidor(analise.metodo)}")
    if analise.parametros:
        parametros = ", ".join(simbolo.name for simbolo in analise.parametros)
        print(f"Parametros livres: {parametros}")
    print(f"x*(p_x, p_y, m) = {analise.demanda_x_repr}")
    print(f"y*(p_x, p_y, m) = {analise.demanda_y_repr}")
    if analise.notas:
        print("\nObservacoes:")
        for nota in analise.notas:
            print(f"  - {nota}")


def _exibir_classificacao_bens(analise: AnaliseUtilidade):
    """Mostra as classificacoes economicas inferidas das demandas."""
    classificacoes = classificar_bens(analise)
    print("\n" + "-"*70)
    print("CLASSIFICACAO DOS BENS")
    print("-"*70)
    for bem in ("x", "y"):
        print(f"\nBem {bem}:")
        for linha in classificacoes[bem]:
            print(f"  - {linha}")


def _exibir_cesta_otima(analise: AnaliseUtilidade):
    """Solicita precos/renda e calcula uma cesta otima."""
    print("\n" + "-"*70)
    print("CALCULO DE CESTA OTIMA")
    print("-"*70)
    preco_x = _ler_float_positivo("Preco do bem x (p_x): ")
    preco_y = _ler_float_positivo("Preco do bem y (p_y): ")
    renda = _ler_float_positivo("Renda do consumidor (m): ")

    valores_parametros = {}
    if analise.parametros:
        print("\nInforme valores numericos para os parametros da utilidade:")
        valores_parametros = _ler_valores_parametros(analise.parametros)

    resultado = calcular_cesta_otima(
        analise=analise,
        preco_x=preco_x,
        preco_y=preco_y,
        renda=renda,
        valores_parametros=valores_parametros,
    )

    status = resultado.get("status")
    if status == "erro":
        print(f"{Cores.FAIL}{resultado['mensagem']}{Cores.ENDC}")
        return

    if status == "multiplas":
        print(f"{Cores.WARNING}{resultado['mensagem']}{Cores.ENDC}")
        if "intervalo_x" in resultado and "intervalo_y" in resultado:
            print(
                "Representacao pratica: x pode variar em "
                f"[0, {resultado['intervalo_x']:.6f}] e y = (m - p_x*x) / p_y."
            )
        return

    print(f"{Cores.OKGREEN}Metodo usado:{Cores.ENDC} {_rotulo_metodo_cesta(resultado['metodo'])}")
    if "x_exato" in resultado:
        print(f"x* = {resultado['x_exato']}  ≈  {resultado['x']:.6f}")
    else:
        print(f"x* = {resultado['x']:.6f}")
    if "y_exato" in resultado:
        print(f"y* = {resultado['y_exato']}  ≈  {resultado['y']:.6f}")
    else:
        print(f"y* = {resultado['y']:.6f}")
    print(f"Orcamento usado = {resultado['orcamento_usado']:.6f}")
    print(f"Folga orcamentaria = {resultado['folga_orcamentaria']:.6f}")
    if resultado.get("tipo_solucao") == "canto":
        local = resultado.get("canto_em") or "fronteira"
        print(
            f"{Cores.WARNING}Solucao de canto detectada:{Cores.ENDC} "
            f"a cesta otima esta no {local}, entao a regra de tangencia nao e valida nesse caso."
        )
    else:
        print(f"{Cores.OKCYAN}Tipo de solucao:{Cores.ENDC} interior")
    if resultado.get("utilidade_expr") is not None:
        print(f"U(x*, y*) = {resultado['utilidade_expr']}")
    if resultado.get("utilidade_num") is not None:
        print(f"Valor numerico de U(x*, y*) = {resultado['utilidade_num']:.6f}")

    if _ler_sim_nao("Deseja gerar o grafico da RO com a curva de indiferenca no otimo? (s/n): "):
        _plotar_cesta_otima_consumidor(
            analise=analise,
            resultado=resultado,
            preco_x=preco_x,
            preco_y=preco_y,
            renda=renda,
            valores_parametros=valores_parametros,
        )


def _ler_valores_parametros(parametros: tuple[sp.Symbol, ...]) -> dict[sp.Symbol, float]:
    """Solicita valores numericos para parametros livres da utilidade."""
    valores = {}
    for simbolo in parametros:
        valores[simbolo] = _ler_float(f"Valor de {simbolo}: ")
    return valores


def _rotulo_metodo_consumidor(metodo: str) -> str:
    rotulos = {
        "lagrange": "Condicoes de primeira ordem de Lagrange",
        "cobb_douglas": "Forma Cobb-Douglas reconhecida diretamente",
        "substitutos_perfeitos": "Utilidade linear / solucao de canto",
        "complementares_perfeitos": "Complementos perfeitos (Min)",
        "nao_fechado": "Sem forma fechada simbolica",
    }
    return rotulos.get(metodo, metodo)


def _rotulo_metodo_cesta(metodo: str) -> str:
    rotulos = {
        "substituicao_da_demanda": "Substituicao direta das demandas marshallianas",
        "substitutos_perfeitos": "Regra analitica de substitutos perfeitos",
        "otimizacao_na_reta_orcamentaria": "Busca numerica sobre a reta orcamentaria",
        "otimizacao_numerica": "Otimizacao numerica com restricao orcamentaria",
    }
    return rotulos.get(metodo, metodo)


def _plotar_cesta_otima_consumidor(
    analise: AnaliseUtilidade,
    resultado: dict[str, object],
    preco_x: float,
    preco_y: float,
    renda: float,
    valores_parametros: dict[sp.Symbol, float],
):
    """Plota reta orcamentaria, curva de indiferenca no otimo e cesta escolhida."""
    utilidade = substituir_utilidade(analise, valores_parametros)
    avaliador = criar_avaliador_utilidade(utilidade)

    intercepto_x = renda / preco_x
    intercepto_y = renda / preco_y
    x_otimo = float(resultado["x"])
    y_otimo = float(resultado["y"])

    x_lim = max(1.0, intercepto_x, x_otimo) * 1.15
    y_lim = max(1.0, intercepto_y, y_otimo) * 1.15
    x_linha = np.linspace(0.0, intercepto_x, 300)
    y_linha = np.maximum(0.0, (renda - preco_x * x_linha) / preco_y)

    x_grid = np.linspace(0.0, x_lim, 240)
    y_grid = np.linspace(0.0, y_lim, 240)
    xx, yy = np.meshgrid(x_grid, y_grid)
    z = np.vectorize(lambda a, b: avaliador(float(a), float(b)), otypes=[float])(xx, yy)
    z = np.ma.masked_invalid(z)

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.fill_between(x_linha, 0, y_linha, color="#4c72b0", alpha=0.10, label="Conjunto orcamentario")
    ax.plot(x_linha, y_linha, color="#1f4e79", linewidth=2.5, label="Restricao orcamentaria")
    ax.scatter([intercepto_x], [0], color="#1f4e79", s=35)
    ax.scatter([0], [intercepto_y], color="#1f4e79", s=35)

    nivel = resultado.get("utilidade_num")
    curva_plotada = False
    if nivel is not None and np.isfinite(float(nivel)) and z.count() > 0:
        z_min = float(z.min())
        z_max = float(z.max())
        if z_min <= float(nivel) <= z_max:
            try:
                contorno = ax.contour(
                    xx,
                    yy,
                    z,
                    levels=[float(nivel)],
                    colors=["#c0392b"],
                    linewidths=2.0,
                )
                if getattr(contorno, "collections", None):
                    contorno.collections[0].set_label("Curva de indiferenca")
                curva_plotada = True
            except Exception:
                curva_plotada = False

    if not curva_plotada:
        print(
            f"{Cores.WARNING}Nao foi possivel desenhar automaticamente a curva de indiferenca "
            "nesse nivel, mas a cesta otima e a restricao orcamentaria foram plotadas."
            f"{Cores.ENDC}"
        )

    cor_ponto = "#d35400" if resultado.get("tipo_solucao") == "canto" else "#2e8b57"
    legenda_ponto = "Cesta otima (canto)" if resultado.get("tipo_solucao") == "canto" else "Cesta otima"
    ax.scatter([x_otimo], [y_otimo], color=cor_ponto, s=70, zorder=5, label=legenda_ponto)
    ax.annotate(
        f"E* = ({x_otimo:.2f}, {y_otimo:.2f})",
        (x_otimo, y_otimo),
        xytext=(8, 8),
        textcoords="offset points",
        color=cor_ponto,
        fontweight="bold",
    )

    ax.set_xlim(0, x_lim)
    ax.set_ylim(0, y_lim)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Escolha Otima do Consumidor")
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(loc="best")

    _renderizar_grafico(fig, "cesta_otima_consumidor", plt)


def _plotar_restricoes_orcamentarias():
    """Coleta dados do usuario e gera as retas orcamentarias correspondentes."""
    print("\n" + "-"*70)
    print("VISUALIZACAO DE RESTRICOES ORCAMENTARIAS")
    print("-"*70)
    print("Para cada cenario informe renda disponivel e precos dos bens.")
    print("O programa gera a reta p_x*x + p_y*y = R e marca as intersecoes.\n")

    bem_x = _ler_texto("Nome do bem no eixo X (padr\u00e3o Bem X): ", default="Bem X")
    bem_y = _ler_texto("Nome do bem no eixo Y (padr\u00e3o Bem Y): ", default="Bem Y")
    qtd = _ler_inteiro_intervalo("Quantos cenarios deseja comparar (1-4)? ", minimo=1, maximo=4)

    cenarios = []
    for idx in range(1, qtd + 1):
        print(f"\nCENARIO {idx}")
        rotulo = _ler_texto("Nome/rotulo do cenario (pressione Enter para padrao): ", default=f"Cenario {idx}")
        renda = _ler_float_positivo("Renda disponivel (R): ")
        preco_x = _ler_float_positivo(f"Preco do {bem_x} (p_{bem_x}): ")
        preco_y = _ler_float_positivo(f"Preco do {bem_y} (p_{bem_y}): ")

        intercepto_x = renda / preco_x
        intercepto_y = renda / preco_y
        incl = preco_x / preco_y

        cenarios.append({
            "label": rotulo,
            "renda": renda,
            "px": preco_x,
            "py": preco_y,
            "intercepto_x": intercepto_x,
            "intercepto_y": intercepto_y,
            "incl": incl,
        })

        print(f"{Cores.OKGREEN}Equacao:{Cores.ENDC} {preco_x:.2f}*{bem_x} + {preco_y:.2f}*{bem_y} = {renda:.2f}")
        print(f"Interceptos -> {bem_x}: {intercepto_x:.2f} | {bem_y}: {intercepto_y:.2f}")

    x_max = max(c["intercepto_x"] for c in cenarios)
    y_max = max(c["intercepto_y"] for c in cenarios)
    x_lim = max(1.0, x_max) * 1.1
    y_lim = max(1.0, y_max) * 1.1

    fig, ax = plt.subplots(figsize=(9, 6))
    cores = plt.cm.get_cmap('tab10', max(3, len(cenarios)))

    for idx, c in enumerate(cenarios):
        x_vals = np.linspace(0, c["intercepto_x"], 200)
        y_vals = (c["renda"] - c["px"] * x_vals) / c["py"]
        y_vals = np.clip(y_vals, 0, y_lim)
        cor = cores(idx)
        ax.plot(x_vals, y_vals, color=cor, label=c["label"], linewidth=2)
        ax.scatter([c["intercepto_x"]], [0], color=cor)
        ax.scatter([0], [c["intercepto_y"]], color=cor)
        ax.text(c["intercepto_x"], 0, f"  {c['intercepto_x']:.1f}", color=cor, va='bottom')
        ax.text(0, c["intercepto_y"], f"{c['intercepto_y']:.1f}", color=cor, ha='left', va='bottom')

    ax.set_xlim(0, x_lim)
    ax.set_ylim(0, y_lim)
    ax.set_xlabel(bem_x)
    ax.set_ylabel(bem_y)
    ax.set_title("Retas Orçamentarias")
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend()

    _renderizar_grafico(fig, "retas_orcamentarias", plt)


def _ler_texto(prompt: str, default: str) -> str:
    """Le um texto do usuario e usa default quando vazio."""
    resposta = input(prompt).strip()
    return resposta if resposta else default


def _ler_sim_nao(prompt: str) -> bool:
    """Le uma confirmacao simples do usuario."""
    return input(prompt).strip().lower().startswith("s")


def _ler_float(prompt: str) -> float:
    """Le um valor float qualquer."""
    while True:
        texto = input(prompt).strip().replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            print(f"{Cores.FAIL}Valor invalido. Tente novamente.{Cores.ENDC}")


def _ler_float_positivo(prompt: str) -> float:
    """Le um valor float estritamente positivo."""
    while True:
        texto = input(prompt).strip().replace(",", ".")
        try:
            valor = float(texto)
        except ValueError:
            print(f"{Cores.FAIL}Valor invalido. Tente novamente.{Cores.ENDC}")
            continue
        if valor <= 0:
            print(f"{Cores.WARNING}Informe um numero maior que zero.{Cores.ENDC}")
            continue
        return valor


def _ler_inteiro_intervalo(prompt: str, minimo: int, maximo: int) -> int:
    """Le um inteiro dentro do intervalo informado."""
    while True:
        resposta = input(prompt).strip()
        if not resposta:
            print(f"{Cores.WARNING}Informe um inteiro entre {minimo} e {maximo}.{Cores.ENDC}")
            continue
        if not resposta.isdigit():
            print(f"{Cores.FAIL}Somente inteiros positivos.{Cores.ENDC}")
            continue
        valor = int(resposta)
        if not (minimo <= valor <= maximo):
            print(f"{Cores.WARNING}Valor precisa estar entre {minimo} e {maximo}.{Cores.ENDC}")
            continue
        return valor


def _renderizar_grafico(fig, nome_base: str, plt_module):
    """Decide entre salvar ou exibir o grafico conforme o ambiente."""
    destino = None
    if _should_save_plots():
        destino = _ensure_output_dir() / f"{nome_base}_{_timestamp()}.png"
        fig.savefig(destino, dpi=150, bbox_inches='tight')
        print(f"{Cores.OKGREEN}Grafico salvo em: {destino}{Cores.ENDC}")
    else:
        plt_module.show()
    plt_module.close(fig)


def _ensure_output_dir() -> Path:
    destino = Path.cwd() / "outputs"
    destino.mkdir(parents=True, exist_ok=True)
    return destino


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _should_save_plots() -> bool:
    """Retorna True em ambientes headless/backends Agg."""
    try:
        backend = plt.get_backend()
        if backend and "agg" in backend.lower():
            return True
    except Exception:
        pass

    return _deve_forcar_backend_agg()


def menu():
    """Alias de entrada para compatibilidade com o launcher principal."""
    menu_micro()


if __name__ == "__main__":
    menu_micro()
