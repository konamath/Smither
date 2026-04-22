"""
Ferramentas de teoria do consumidor para o modulo de microeconomia.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import numpy as np
import sympy as sp
from scipy import optimize
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

X = sp.symbols("x", nonnegative=True, real=True)
Y = sp.symbols("y", nonnegative=True, real=True)
PX = sp.symbols("p_x", positive=True, real=True)
PY = sp.symbols("p_y", positive=True, real=True)
M = sp.symbols("m", positive=True, real=True)
LAMBDA = sp.symbols("lambda", real=True)

TRANSFORMACOES = standard_transformations + (implicit_multiplication_application,)
LOCAL_DICT = {
    "x": X,
    "y": Y,
    "X": X,
    "Y": Y,
    "p_x": PX,
    "p_y": PY,
    "m": M,
    "P_X": PX,
    "P_Y": PY,
    "M": M,
    "e": sp.E,
    "E": sp.E,
    "pi": sp.pi,
    "Pi": sp.pi,
    "PI": sp.pi,
    "oo": sp.oo,
    "inf": sp.oo,
    "sin": sp.sin,
    "SIN": sp.sin,
    "cos": sp.cos,
    "COS": sp.cos,
    "tan": sp.tan,
    "TAN": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "tanh": sp.tanh,
    "exp": sp.exp,
    "EXP": sp.exp,
    "log": sp.log,
    "LOG": sp.log,
    "ln": sp.log,
    "LN": sp.log,
    "sqrt": sp.sqrt,
    "SQRT": sp.sqrt,
    "abs": sp.Abs,
    "Abs": sp.Abs,
    "ABS": sp.Abs,
    "sign": sp.sign,
    "Min": sp.Min,
    "min": sp.Min,
    "MIN": sp.Min,
    "Leontief": sp.Min,
    "leontief": sp.Min,
    "LEONTIEF": sp.Min,
    "Max": sp.Max,
    "max": sp.Max,
    "MAX": sp.Max,
    "Piecewise": sp.Piecewise,
    "Heaviside": sp.Heaviside,
}


@dataclass
class AnaliseUtilidade:
    """Estado da utilidade e dos resultados analiticos da sessao."""

    texto_original: str
    utilidade: sp.Expr
    metodo: str
    parametros: tuple[sp.Symbol, ...] = ()
    demanda_x: sp.Expr | None = None
    demanda_y: sp.Expr | None = None
    demanda_x_repr: str = ""
    demanda_y_repr: str = ""
    solucao_unica: bool = True
    notas: list[str] = field(default_factory=list)
    detalhes: dict[str, object] = field(default_factory=dict)


def analisar_utilidade(texto: str) -> AnaliseUtilidade:
    """Interpreta uma utilidade U(x, y) e tenta derivar as demandas marshallianas."""
    utilidade = _parse_utilidade(texto)
    parametros = tuple(sorted(utilidade.free_symbols - {X, Y}, key=lambda simbolo: simbolo.name))
    notas: list[str] = []

    if parametros:
        lista = ", ".join(simbolo.name for simbolo in parametros)
        notas.append(
            f"A utilidade contem parametros simbolicos ({lista}). "
            "A classificacao pode ficar condicional ate que esses valores sejam fixados."
        )

    resultado = _resolver_complementos_perfeitos(utilidade)
    if resultado is None:
        resultado = _resolver_substitutos_perfeitos(utilidade)
    if resultado is None:
        resultado = _resolver_cobb_douglas(utilidade)
    if resultado is None:
        resultado = _resolver_lagrange(utilidade)

    if resultado is None:
        notas.append(
            "Nao foi possivel obter demanda marshalliana fechada por simbolos. "
            "Ainda assim, a rotina numerica de cesta otima permanece disponivel."
        )
        return AnaliseUtilidade(
            texto_original=texto,
            utilidade=utilidade,
            metodo="nao_fechado",
            parametros=parametros,
            demanda_x_repr="Nao disponivel em forma fechada.",
            demanda_y_repr="Nao disponivel em forma fechada.",
            solucao_unica=False,
            notas=notas,
        )

    resultado.notas = notas + resultado.notas
    resultado.texto_original = texto
    resultado.utilidade = utilidade
    resultado.parametros = parametros
    return resultado


def classificar_bens(analise: AnaliseUtilidade) -> dict[str, list[str]]:
    """Classifica os bens a partir das demandas marshallianas obtidas."""
    if analise.metodo == "substitutos_perfeitos":
        return _classificar_substitutos_perfeitos(analise)

    if analise.demanda_x is None or analise.demanda_y is None:
        return {
            "x": [
                "Nao ha demanda marshalliana fechada para classificar o bem x.",
                "Use a rotina numerica de cesta otima para avaliar casos especificos de precos e renda.",
            ],
            "y": [
                "Nao ha demanda marshalliana fechada para classificar o bem y.",
                "Use a rotina numerica de cesta otima para avaliar casos especificos de precos e renda.",
            ],
        }

    return {
        "x": _classificar_demanda_generica("x", analise.demanda_x, PX, PY),
        "y": _classificar_demanda_generica("y", analise.demanda_y, PY, PX),
    }


def calcular_cesta_otima(
    analise: AnaliseUtilidade,
    preco_x: float,
    preco_y: float,
    renda: float,
    valores_parametros: dict[sp.Symbol, float] | None = None,
) -> dict[str, object]:
    """Calcula uma cesta otima para precos e renda dados."""
    substituicoes = valores_parametros or {}
    utilidade = substituir_utilidade(analise, substituicoes)
    parametros_restantes = utilidade.free_symbols - {X, Y}
    if parametros_restantes:
        faltantes = ", ".join(sorted(simbolo.name for simbolo in parametros_restantes))
        return {
            "status": "erro",
            "mensagem": f"Faltam valores numericos para: {faltantes}.",
        }

    candidatos: list[dict[str, object]] = []

    if analise.metodo == "substitutos_perfeitos":
        resultado_linear = _calcular_cesta_substitutos_perfeitos(
            analise, preco_x, preco_y, renda, substituicoes
        )
        if resultado_linear is not None:
            if resultado_linear.get("status") == "multiplas":
                return resultado_linear
            candidatos.append(resultado_linear)

    if analise.demanda_x is not None and analise.demanda_y is not None and analise.solucao_unica:
        cesta_exata = _avaliar_demanda_exata(
            analise, preco_x, preco_y, renda, substituicoes, utilidade
        )
        if cesta_exata is not None:
            candidatos.append(cesta_exata)

    cesta_reta = _otimizar_na_restricao_orcamentaria(utilidade, preco_x, preco_y, renda)
    if cesta_reta is not None:
        candidatos.append(cesta_reta)

    cesta_numerica = _otimizar_cesta_numericamente(utilidade, preco_x, preco_y, renda)
    if cesta_numerica is not None:
        candidatos.append(cesta_numerica)

    melhor = _selecionar_melhor_cesta(candidatos)
    if melhor is None:
        return {
            "status": "erro",
            "mensagem": "Nao foi possivel encontrar uma cesta otima numericamente.",
        }

    return melhor


def formatar_expr(expr: sp.Expr | None) -> str:
    """Formata uma expressao simbólica para exibicao simples."""
    if expr is None:
        return "indisponivel"
    return str(sp.simplify(expr))


def substituir_utilidade(
    analise: AnaliseUtilidade,
    valores_parametros: dict[sp.Symbol, float] | None = None,
) -> sp.Expr:
    """Substitui parametros numericos na utilidade atual."""
    return sp.simplify(analise.utilidade.subs(valores_parametros or {}))


def criar_avaliador_utilidade(utilidade: sp.Expr):
    """Cria um avaliador numerico escalar para U(x, y)."""
    funcao = sp.lambdify((X, Y), utilidade, modules=["numpy"])

    def _avaliar(x_val: float, y_val: float) -> float:
        try:
            with np.errstate(all="ignore"):
                valor = funcao(x_val, y_val)
        except Exception:  # pylint: disable=broad-except
            return np.nan
        if isinstance(valor, np.ndarray):
            valor = np.asarray(valor).reshape(-1)[0]
        if np.iscomplexobj(valor):
            if abs(np.imag(valor)) > 1e-8:
                return np.nan
            valor = np.real(valor)
        try:
            return float(valor)
        except (TypeError, ValueError):
            return np.nan

    return _avaliar


def _parse_utilidade(texto: str) -> sp.Expr:
    texto_limpo = _normalizar_texto_utilidade(texto)
    if not texto_limpo:
        raise ValueError("E necessario informar uma funcao utilidade.")

    funcoes = [
        "sin", "cos", "tan", "asin", "acos", "atan",
        "sinh", "cosh", "tanh", "exp", "log", "sqrt",
        "Min", "Max", "min", "max", "abs", "Abs",
        "Leontief", "leontief", "LEONTIEF",
    ]

    def _inserir_parenteses(match: re.Match[str]) -> str:
        return f"{match.group(1)}({match.group(2)})"

    for funcao in funcoes:
        padrao = rf"\b({funcao})(?!\s*\()([A-Za-z0-9_]+)"
        texto_limpo = re.sub(padrao, _inserir_parenteses, texto_limpo)

    try:
        return parse_expr(
            texto_limpo,
            transformations=TRANSFORMACOES,
            local_dict=LOCAL_DICT,
        )
    except Exception as exc:  # pylint: disable=broad-except
        raise ValueError(f"Nao foi possivel interpretar a utilidade: {exc}") from exc


def _normalizar_texto_utilidade(texto: str) -> str:
    texto_limpo = texto.strip()
    padrao_utilidade = re.compile(r"^\s*[Uu](\s*\(\s*[Xx]\s*,\s*[Yy]\s*\))?\s*=")
    if padrao_utilidade.match(texto_limpo):
        texto_limpo = texto_limpo.split("=", 1)[1].strip()

    aliases = {
        r"\bX\b": "x",
        r"\bY\b": "y",
        r"\bP_X\b": "p_x",
        r"\bP_Y\b": "p_y",
        r"\bM\b": "m",
        r"\bLOG\b": "log",
        r"\bLN\b": "ln",
        r"\bEXP\b": "exp",
        r"\bSQRT\b": "sqrt",
        r"\bMIN\b": "Min",
        r"\bLEONTIEF\b": "Leontief",
        r"\bMAX\b": "Max",
        r"\bABS\b": "Abs",
    }
    for padrao, substituicao in aliases.items():
        texto_limpo = re.sub(padrao, substituicao, texto_limpo)

    return texto_limpo


def _resolver_substitutos_perfeitos(utilidade: sp.Expr) -> AnaliseUtilidade | None:
    if not _eh_linear_em_x_y(utilidade):
        return None

    coef_x = sp.simplify(sp.diff(utilidade, X))
    coef_y = sp.simplify(sp.diff(utilidade, Y))

    if coef_x.has(X, Y) or coef_y.has(X, Y):
        return None

    taxa_x = sp.simplify(coef_x / PX) if coef_x != 0 else sp.Integer(0)
    taxa_y = sp.simplify(coef_y / PY) if coef_y != 0 else sp.Integer(0)

    if coef_x == 0 and coef_y == 0:
        notas = [
            "Utilidade constante detectada: qualquer cesta factivel maximiza a utilidade.",
        ]
        return AnaliseUtilidade(
            texto_original="",
            utilidade=utilidade,
            metodo="substitutos_perfeitos",
            demanda_x_repr="Qualquer x >= 0 com p_x*x + p_y*y <= m.",
            demanda_y_repr="Qualquer y >= 0 com p_x*x + p_y*y <= m.",
            solucao_unica=False,
            notas=notas,
            detalhes={"coef_x": coef_x, "coef_y": coef_y},
        )

    notas = [
        "Utilidade linear detectada: a solucao tende a cestas de canto.",
        f"Compare MUx/p_x = {formatar_expr(taxa_x)} com MUy/p_y = {formatar_expr(taxa_y)}.",
    ]
    return AnaliseUtilidade(
        texto_original="",
        utilidade=utilidade,
        metodo="substitutos_perfeitos",
        demanda_x_repr=(
            f"{formatar_expr(M / PX)} se {formatar_expr(taxa_x)} > {formatar_expr(taxa_y)}; "
            f"0 se {formatar_expr(taxa_x)} < {formatar_expr(taxa_y)}; "
            f"qualquer x em [0, {formatar_expr(M / PX)}] se houver empate."
        ),
        demanda_y_repr=(
            f"0 se {formatar_expr(taxa_x)} > {formatar_expr(taxa_y)}; "
            f"{formatar_expr(M / PY)} se {formatar_expr(taxa_x)} < {formatar_expr(taxa_y)}; "
            f"qualquer y na reta orcamentaria se houver empate."
        ),
        solucao_unica=False,
        notas=notas,
        detalhes={"coef_x": coef_x, "coef_y": coef_y},
    )


def _resolver_complementos_perfeitos(utilidade: sp.Expr) -> AnaliseUtilidade | None:
    _, parte_dependente = utilidade.as_independent(X, Y, as_Add=True)
    base = parte_dependente if parte_dependente != 0 else utilidade
    if base.func != sp.Min or len(base.args) != 2:
        return None

    for arg_x, arg_y in ((base.args[0], base.args[1]), (base.args[1], base.args[0])):
        coef_x = _coef_linear_homogeneo(arg_x, X, Y)
        coef_y = _coef_linear_homogeneo(arg_y, Y, X)
        if coef_x is None or coef_y is None:
            continue

        try:
            solucoes = sp.solve(
                [sp.Eq(coef_x * X, coef_y * Y), sp.Eq(PX * X + PY * Y, M)],
                [X, Y],
                dict=True,
            )
        except Exception:  # pylint: disable=broad-except
            continue

        if not solucoes:
            continue

        x_demanda = sp.simplify(solucoes[0][X])
        y_demanda = sp.simplify(solucoes[0][Y])
        return AnaliseUtilidade(
            texto_original="",
            utilidade=utilidade,
            metodo="complementares_perfeitos",
            demanda_x=x_demanda,
            demanda_y=y_demanda,
            demanda_x_repr=formatar_expr(x_demanda),
            demanda_y_repr=formatar_expr(y_demanda),
            solucao_unica=True,
            notas=[
                "Complementos perfeitos detectados a partir de uma utilidade do tipo Min(a*x, b*y).",
                f"A condicao de proporcao otima usada foi {formatar_expr(coef_x * X)} = {formatar_expr(coef_y * Y)}.",
            ],
            detalhes={"coef_x": coef_x, "coef_y": coef_y},
        )

    return None


def _resolver_cobb_douglas(utilidade: sp.Expr) -> AnaliseUtilidade | None:
    expoente_x, expoente_y = _extrair_expoentes_cobb_douglas(utilidade)
    if expoente_x is None or expoente_y is None:
        return None

    soma = sp.simplify(expoente_x + expoente_y)
    if soma == 0:
        return None

    x_demanda = sp.simplify((expoente_x / soma) * M / PX)
    y_demanda = sp.simplify((expoente_y / soma) * M / PY)
    return AnaliseUtilidade(
        texto_original="",
        utilidade=utilidade,
        metodo="cobb_douglas",
        demanda_x=x_demanda,
        demanda_y=y_demanda,
        demanda_x_repr=formatar_expr(x_demanda),
        demanda_y_repr=formatar_expr(y_demanda),
        solucao_unica=True,
        notas=[
            "Forma Cobb-Douglas detectada: U(x, y) = A*x**a*y**b.",
            f"Participacoes de gasto: a/(a+b) = {formatar_expr(expoente_x / soma)} e "
            f"b/(a+b) = {formatar_expr(expoente_y / soma)}.",
        ],
        detalhes={"expoente_x": expoente_x, "expoente_y": expoente_y},
    )


def _resolver_lagrange(utilidade: sp.Expr) -> AnaliseUtilidade | None:
    try:
        solucoes = sp.solve(
            [
                sp.Eq(sp.diff(utilidade, X), LAMBDA * PX),
                sp.Eq(sp.diff(utilidade, Y), LAMBDA * PY),
                sp.Eq(PX * X + PY * Y, M),
            ],
            [X, Y, LAMBDA],
            dict=True,
        )
    except Exception:  # pylint: disable=broad-except
        return None

    pares: list[tuple[sp.Expr, sp.Expr]] = []
    vistos: set[tuple[str, str]] = set()
    for solucao in solucoes:
        if X not in solucao or Y not in solucao:
            continue
        x_demanda = sp.simplify(solucao[X])
        y_demanda = sp.simplify(solucao[Y])
        chave = (str(x_demanda), str(y_demanda))
        if chave in vistos:
            continue
        vistos.add(chave)
        pares.append((x_demanda, y_demanda))

    if len(pares) != 1:
        return None

    x_demanda, y_demanda = pares[0]
    return AnaliseUtilidade(
        texto_original="",
        utilidade=utilidade,
        metodo="lagrange",
        demanda_x=x_demanda,
        demanda_y=y_demanda,
        demanda_x_repr=formatar_expr(x_demanda),
        demanda_y_repr=formatar_expr(y_demanda),
        solucao_unica=True,
        notas=[
            "Demandas obtidas pelas condicoes de primeira ordem de Lagrange.",
        ],
    )


def _classificar_demanda_generica(
    nome_bem: str,
    demanda: sp.Expr,
    preco_proprio: sp.Symbol,
    preco_cruzado: sp.Symbol,
) -> list[str]:
    deriv_renda = sp.simplify(sp.diff(demanda, M))
    deriv_preco = sp.simplify(sp.diff(demanda, preco_proprio))
    deriv_cruzado = sp.simplify(sp.diff(demanda, preco_cruzado))

    linhas = [f"Demanda marshalliana de {nome_bem}: {formatar_expr(demanda)}."]
    linhas.append(
        _rotulo_por_sinal(
            deriv_renda,
            positivo=f"Renda: bem normal/comum (d{nome_bem}*/dm = {formatar_expr(deriv_renda)} > 0).",
            negativo=f"Renda: bem inferior (d{nome_bem}*/dm = {formatar_expr(deriv_renda)} < 0).",
            nulo=f"Renda: bem neutro em relacao a m (d{nome_bem}*/dm = 0).",
            indefinido=f"Renda: classificacao indeterminada (d{nome_bem}*/dm = {formatar_expr(deriv_renda)}).",
        )
    )

    elasticidade_renda = _elasticidade(demanda, deriv_renda, M)
    if elasticidade_renda is not None:
        linhas.append(
            _classificar_elasticidade_renda(nome_bem, elasticidade_renda)
        )

    linhas.append(
        _rotulo_por_sinal(
            deriv_preco,
            positivo=(
                f"Preco proprio: bem de Giffen "
                f"(d{nome_bem}*/d{preco_proprio} = {formatar_expr(deriv_preco)} > 0)."
            ),
            negativo=(
                f"Preco proprio: bem comum/ordinario "
                f"(d{nome_bem}*/d{preco_proprio} = {formatar_expr(deriv_preco)} < 0)."
            ),
            nulo=(
                f"Preco proprio: demanda neutra ao proprio preco "
                f"(d{nome_bem}*/d{preco_proprio} = 0)."
            ),
            indefinido=(
                f"Preco proprio: classificacao indeterminada "
                f"(d{nome_bem}*/d{preco_proprio} = {formatar_expr(deriv_preco)})."
            ),
        )
    )

    linhas.append(
        _rotulo_por_sinal(
            deriv_cruzado,
            positivo=(
                f"Preco cruzado: {nome_bem} e o outro bem sao substitutos "
                f"(d{nome_bem}*/d{preco_cruzado} = {formatar_expr(deriv_cruzado)} > 0)."
            ),
            negativo=(
                f"Preco cruzado: {nome_bem} e o outro bem sao complementares "
                f"(d{nome_bem}*/d{preco_cruzado} = {formatar_expr(deriv_cruzado)} < 0)."
            ),
            nulo=(
                f"Preco cruzado: os bens sao independentes na demanda marshalliana "
                f"(d{nome_bem}*/d{preco_cruzado} = 0)."
            ),
            indefinido=(
                f"Preco cruzado: classificacao indeterminada "
                f"(d{nome_bem}*/d{preco_cruzado} = {formatar_expr(deriv_cruzado)})."
            ),
        )
    )
    return linhas


def _classificar_substitutos_perfeitos(analise: AnaliseUtilidade) -> dict[str, list[str]]:
    coef_x = formatar_expr(analise.detalhes.get("coef_x"))
    coef_y = formatar_expr(analise.detalhes.get("coef_y"))
    return {
        "x": [
            f"Utilidade linear com MUx = {coef_x} e MUy = {coef_y}.",
            "Renda: bem normal quando a solucao escolhe x; fora dessa regiao, a demanda pode ficar zerada por canto.",
            "Preco proprio: bem comum/ordinario, nunca Giffen na regiao em que x e consumido.",
            "Preco cruzado: x e y sao substitutos perfeitos, com descontinuidade na fronteira MUx/p_x = MUy/p_y.",
        ],
        "y": [
            f"Utilidade linear com MUx = {coef_x} e MUy = {coef_y}.",
            "Renda: bem normal quando a solucao escolhe y; fora dessa regiao, a demanda pode ficar zerada por canto.",
            "Preco proprio: bem comum/ordinario, nunca Giffen na regiao em que y e consumido.",
            "Preco cruzado: y e x sao substitutos perfeitos, com descontinuidade na fronteira MUx/p_x = MUy/p_y.",
        ],
    }


def _classificar_elasticidade_renda(nome_bem: str, elasticidade: sp.Expr) -> str:
    elasticidade = sp.simplify(elasticidade)
    if elasticidade == 0:
        return f"Elasticidade-renda: nula (epsilon_m de {nome_bem} = 0)."
    if elasticidade.is_negative:
        return (
            f"Elasticidade-renda: negativa, reforcando classificacao de bem inferior "
            f"(epsilon_m de {nome_bem} = {formatar_expr(elasticidade)})."
        )
    if elasticidade.is_positive:
        comparacao = sp.simplify(elasticidade - 1)
        if comparacao == 0:
            return f"Elasticidade-renda: unitária (epsilon_m de {nome_bem} = 1)."
        if comparacao.is_positive:
            return (
                f"Elasticidade-renda: maior que 1, sugerindo bem de luxo/superior "
                f"(epsilon_m de {nome_bem} = {formatar_expr(elasticidade)})."
            )
        if comparacao.is_negative:
            return (
                f"Elasticidade-renda: entre 0 e 1, sugerindo bem necessario/normal "
                f"(epsilon_m de {nome_bem} = {formatar_expr(elasticidade)})."
            )
    return (
        f"Elasticidade-renda: classificacao indeterminada "
        f"(epsilon_m de {nome_bem} = {formatar_expr(elasticidade)})."
    )


def _elasticidade(demanda: sp.Expr, derivada: sp.Expr, variavel: sp.Symbol) -> sp.Expr | None:
    if sp.simplify(demanda) == 0:
        return None
    try:
        return sp.simplify(derivada * variavel / demanda)
    except Exception:  # pylint: disable=broad-except
        return None


def _rotulo_por_sinal(
    expr: sp.Expr,
    positivo: str,
    negativo: str,
    nulo: str,
    indefinido: str,
) -> str:
    expr = sp.simplify(expr)
    if expr == 0:
        return nulo
    if expr.is_positive:
        return positivo
    if expr.is_negative:
        return negativo
    return indefinido


def _eh_linear_em_x_y(expr: sp.Expr) -> bool:
    try:
        return (
            sp.simplify(sp.diff(expr, X, 2)) == 0
            and sp.simplify(sp.diff(expr, Y, 2)) == 0
            and sp.simplify(sp.diff(expr, X, Y)) == 0
        )
    except Exception:  # pylint: disable=broad-except
        return False


def _extrair_expoentes_cobb_douglas(utilidade: sp.Expr) -> tuple[sp.Expr | None, sp.Expr | None]:
    try:
        expr = sp.simplify(utilidade)
        potencias = expr.as_powers_dict()
        expoente_x = potencias.get(X)
        expoente_y = potencias.get(Y)
        if expoente_x is None or expoente_y is None:
            return None, None
        resto = sp.simplify(expr / (X**expoente_x * Y**expoente_y))
        if resto.has(X, Y):
            return None, None
        return sp.simplify(expoente_x), sp.simplify(expoente_y)
    except Exception:  # pylint: disable=broad-except
        return None, None


def _coef_linear_homogeneo(expr: sp.Expr, variavel: sp.Symbol, outra: sp.Symbol) -> sp.Expr | None:
    expr = sp.simplify(sp.expand(expr))
    if expr.has(outra):
        return None
    try:
        if sp.simplify(expr.subs(variavel, 0)) != 0:
            return None
    except Exception:  # pylint: disable=broad-except
        return None
    coeficiente = sp.simplify(sp.diff(expr, variavel))
    if coeficiente.has(variavel, outra):
        return None
    if sp.simplify(expr - coeficiente * variavel) != 0:
        return None
    return coeficiente


def _calcular_cesta_substitutos_perfeitos(
    analise: AnaliseUtilidade,
    preco_x: float,
    preco_y: float,
    renda: float,
    substituicoes: dict[sp.Symbol, float],
) -> dict[str, object] | None:
    coef_x = sp.simplify(analise.detalhes.get("coef_x", 0)).subs(substituicoes)
    coef_y = sp.simplify(analise.detalhes.get("coef_y", 0)).subs(substituicoes)
    if (coef_x.free_symbols - {X, Y}) or (coef_y.free_symbols - {X, Y}):
        return None

    coef_x_num = _expr_para_float(coef_x)
    coef_y_num = _expr_para_float(coef_y)
    if coef_x_num is None or coef_y_num is None:
        return None

    tol = 1e-9
    taxa_x = coef_x_num / preco_x if preco_x > 0 else np.inf
    taxa_y = coef_y_num / preco_y if preco_y > 0 else np.inf

    if abs(taxa_x) <= tol and abs(taxa_y) <= tol:
        return {
            "status": "multiplas",
            "metodo": "substitutos_perfeitos",
            "mensagem": "A utilidade e constante. Toda cesta factivel e otima.",
        }

    if abs(taxa_x - taxa_y) <= tol:
        return {
            "status": "multiplas",
            "metodo": "substitutos_perfeitos",
            "mensagem": (
                "Ha infinitas cestas otimas: qualquer ponto com "
                f"{preco_x:.4f}*x + {preco_y:.4f}*y = {renda:.4f}, x >= 0 e y >= 0."
            ),
            "intervalo_x": renda / preco_x,
            "intervalo_y": renda / preco_y,
        }

    if taxa_x > taxa_y:
        x_otimo = renda / preco_x
        y_otimo = 0.0
    else:
        x_otimo = 0.0
        y_otimo = renda / preco_y

    return _montar_resultado_numerico(
        utilidade=sp.simplify(analise.utilidade.subs(substituicoes)),
        x_otimo=x_otimo,
        y_otimo=y_otimo,
        preco_x=preco_x,
        preco_y=preco_y,
        renda=renda,
        metodo="substitutos_perfeitos",
    )


def _avaliar_demanda_exata(
    analise: AnaliseUtilidade,
    preco_x: float,
    preco_y: float,
    renda: float,
    substituicoes: dict[sp.Symbol, float],
    utilidade: sp.Expr,
) -> dict[str, object] | None:
    substituicoes_completas = {
        PX: preco_x,
        PY: preco_y,
        M: renda,
        **substituicoes,
    }
    x_exato = sp.simplify(analise.demanda_x.subs(substituicoes_completas))
    y_exato = sp.simplify(analise.demanda_y.subs(substituicoes_completas))
    if (x_exato.free_symbols - {X, Y}) or (y_exato.free_symbols - {X, Y}):
        return None

    x_otimo = _expr_para_float(x_exato)
    y_otimo = _expr_para_float(y_exato)
    if x_otimo is None or y_otimo is None:
        return None
    if x_otimo < -1e-9 or y_otimo < -1e-9:
        return None
    if preco_x * x_otimo + preco_y * y_otimo > renda + 1e-6:
        return None

    resultado = _montar_resultado_numerico(
        utilidade=utilidade,
        x_otimo=max(0.0, x_otimo),
        y_otimo=max(0.0, y_otimo),
        preco_x=preco_x,
        preco_y=preco_y,
        renda=renda,
        metodo="substituicao_da_demanda",
    )
    resultado["x_exato"] = x_exato
    resultado["y_exato"] = y_exato
    return resultado


def _otimizar_na_restricao_orcamentaria(
    utilidade: sp.Expr,
    preco_x: float,
    preco_y: float,
    renda: float,
) -> dict[str, object] | None:
    avaliador = criar_avaliador_utilidade(utilidade)
    limite_x = renda / preco_x
    x_grade = np.linspace(0.0, limite_x, 801)
    melhor: tuple[float, float, float] | None = None

    for x_otimo in x_grade:
        y_otimo = max(0.0, (renda - preco_x * float(x_otimo)) / preco_y)
        valor = avaliador(float(x_otimo), float(y_otimo))
        if np.isfinite(valor) and (melhor is None or valor > melhor[2]):
            melhor = (float(x_otimo), float(y_otimo), float(valor))

    if melhor is None:
        return None

    indice_melhor = int(np.argmin(np.abs(x_grade - melhor[0])))
    esquerda = float(x_grade[max(0, indice_melhor - 1)])
    direita = float(x_grade[min(len(x_grade) - 1, indice_melhor + 1)])

    if direita > esquerda:
        def _objetivo(x_val: float) -> float:
            y_val = max(0.0, (renda - preco_x * x_val) / preco_y)
            valor = avaliador(float(x_val), float(y_val))
            if not np.isfinite(valor):
                return 1e12
            return -valor

        try:
            refinado = optimize.minimize_scalar(
                _objetivo,
                bounds=(esquerda, direita),
                method="bounded",
            )
            if refinado.success:
                x_ref = float(refinado.x)
                y_ref = max(0.0, (renda - preco_x * x_ref) / preco_y)
                valor_ref = avaliador(x_ref, y_ref)
                if np.isfinite(valor_ref) and valor_ref > melhor[2]:
                    melhor = (x_ref, y_ref, float(valor_ref))
        except Exception:  # pylint: disable=broad-except
            pass

    x_otimo, y_otimo, _ = melhor
    return _montar_resultado_numerico(
        utilidade=utilidade,
        x_otimo=x_otimo,
        y_otimo=y_otimo,
        preco_x=preco_x,
        preco_y=preco_y,
        renda=renda,
        metodo="otimizacao_na_reta_orcamentaria",
    )


def _otimizar_cesta_numericamente(
    utilidade: sp.Expr,
    preco_x: float,
    preco_y: float,
    renda: float,
) -> dict[str, object] | None:
    avaliador = criar_avaliador_utilidade(utilidade)
    limite_x = renda / preco_x
    limite_y = renda / preco_y

    def _objetivo(vetor: np.ndarray) -> float:
        valor = avaliador(float(vetor[0]), float(vetor[1]))
        if not np.isfinite(valor):
            return 1e12
        return -valor

    restricao = {
        "type": "ineq",
        "fun": lambda vetor: renda - preco_x * vetor[0] - preco_y * vetor[1],
    }
    pontos_iniciais = [
        np.array([0.0, 0.0]),
        np.array([limite_x, 0.0]),
        np.array([0.0, limite_y]),
        np.array([limite_x / 2, limite_y / 2]),
        np.array([limite_x / 3, max(0.0, (renda - preco_x * (limite_x / 3)) / preco_y)]),
    ]

    melhor: tuple[float, float, float] | None = None
    for ponto in pontos_iniciais:
        try:
            resultado = optimize.minimize(
                _objetivo,
                ponto,
                method="SLSQP",
                bounds=[(0.0, limite_x), (0.0, limite_y)],
                constraints=[restricao],
            )
        except Exception:  # pylint: disable=broad-except
            continue
        if not resultado.success:
            continue
        x_otimo = float(resultado.x[0])
        y_otimo = float(resultado.x[1])
        utilidade_valor = avaliador(x_otimo, y_otimo)
        if not np.isfinite(utilidade_valor):
            continue
        if melhor is None or utilidade_valor > melhor[2]:
            melhor = (x_otimo, y_otimo, utilidade_valor)

    if melhor is None:
        melhor = _buscar_em_grade(avaliador, preco_x, preco_y, renda)

    if melhor is None:
        return None

    x_otimo, y_otimo, _ = melhor
    return _montar_resultado_numerico(
        utilidade=utilidade,
        x_otimo=x_otimo,
        y_otimo=y_otimo,
        preco_x=preco_x,
        preco_y=preco_y,
        renda=renda,
        metodo="otimizacao_numerica",
    )


def _buscar_em_grade(
    avaliador,
    preco_x: float,
    preco_y: float,
    renda: float,
) -> tuple[float, float, float] | None:
    limite_x = renda / preco_x
    melhor: tuple[float, float, float] | None = None
    for x_otimo in np.linspace(0.0, limite_x, 161):
        y_max = max(0.0, (renda - preco_x * x_otimo) / preco_y)
        for y_otimo in np.linspace(0.0, y_max, 161):
            valor = avaliador(float(x_otimo), float(y_otimo))
            if np.isfinite(valor) and (melhor is None or valor > melhor[2]):
                melhor = (float(x_otimo), float(y_otimo), float(valor))
    return melhor


def _selecionar_melhor_cesta(candidatos: list[dict[str, object]]) -> dict[str, object] | None:
    candidatos_validos = [
        candidato for candidato in candidatos
        if candidato.get("status") == "ok" and candidato.get("utilidade_num") is not None
    ]
    if not candidatos_validos:
        return None

    melhor = candidatos_validos[0]
    tol = 1e-7
    prioridade = {
        "substitutos_perfeitos": 0,
        "substituicao_da_demanda": 1,
        "otimizacao_na_reta_orcamentaria": 2,
        "otimizacao_numerica": 3,
    }
    for candidato in candidatos_validos[1:]:
        utilidade_candidato = float(candidato["utilidade_num"])
        utilidade_melhor = float(melhor["utilidade_num"])
        if utilidade_candidato > utilidade_melhor + tol:
            melhor = candidato
            continue
        if abs(utilidade_candidato - utilidade_melhor) <= tol:
            if prioridade.get(str(candidato.get("metodo")), 99) < prioridade.get(str(melhor.get("metodo")), 99):
                melhor = candidato
    return melhor


def _montar_resultado_numerico(
    utilidade: sp.Expr,
    x_otimo: float,
    y_otimo: float,
    preco_x: float,
    preco_y: float,
    renda: float,
    metodo: str,
) -> dict[str, object]:
    tol = 1e-8
    x_limpo = 0.0 if abs(x_otimo) <= tol else float(x_otimo)
    y_limpo = 0.0 if abs(y_otimo) <= tol else float(y_otimo)
    utilidade_otima_expr = sp.simplify(utilidade.subs({X: x_limpo, Y: y_limpo}))
    utilidade_otima_num = _expr_para_float(utilidade_otima_expr)
    tipo_solucao = "interior"
    canto_em = None
    if x_limpo == 0.0 and y_limpo == 0.0:
        tipo_solucao = "canto"
        canto_em = "origem"
    elif x_limpo == 0.0:
        tipo_solucao = "canto"
        canto_em = "eixo y"
    elif y_limpo == 0.0:
        tipo_solucao = "canto"
        canto_em = "eixo x"
    return {
        "status": "ok",
        "metodo": metodo,
        "tipo_solucao": tipo_solucao,
        "canto_em": canto_em,
        "x": max(0.0, x_limpo),
        "y": max(0.0, y_limpo),
        "orcamento_usado": preco_x * max(0.0, x_limpo) + preco_y * max(0.0, y_limpo),
        "folga_orcamentaria": renda - (preco_x * max(0.0, x_limpo) + preco_y * max(0.0, y_limpo)),
        "utilidade_expr": utilidade_otima_expr,
        "utilidade_num": utilidade_otima_num,
    }


def _expr_para_float(expr: sp.Expr) -> float | None:
    try:
        valor = complex(sp.N(expr))
    except Exception:  # pylint: disable=broad-except
        return None
    if abs(valor.imag) > 1e-8:
        return None
    return float(valor.real)
