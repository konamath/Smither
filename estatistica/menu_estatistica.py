"""Menu e utilidades do módulo de Estatística do Smither."""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from math import comb
from textwrap import dedent
from datetime import datetime
from pathlib import Path
import math

import numpy as np
import pandas as pd
import scipy
from scipy import stats
import sympy as sp
import matplotlib
import matplotlib.pyplot as plt

try:  # OpenAI é opcional durante o desenvolvimento/local sem credenciais.
    from openai import OpenAI  # type: ignore
except ImportError:  # pragma: no cover - caminho apenas para ambientes sem openai
    OpenAI = None  # type: ignore


DEFAULT_OPENAI_MODEL = os.getenv("SMITHER_OPENAI_MODEL", "gpt-4.1-mini")
STAT_STACK = {
    "NumPy": np.__version__,
    "pandas": pd.__version__,
    "SciPy": scipy.__version__,
}
COMMON_DISTRIBUTIONS = {
    "Normal": stats.norm,
    "Binomial": stats.binom,
    "Poisson": stats.poisson,
    "Exponencial": stats.expon,
}
NUMBER_WORDS = {
    "uma": 1,
    "um": 1,
    "duas": 2,
    "dois": 2,
    "três": 3,
    "tres": 3,
    "quatro": 4,
    "cinco": 5,
    "seis": 6,
    "sete": 7,
    "oito": 8,
    "nove": 9,
    "dez": 10,
}
COLOR_ALIASES = {
    "amarel": "amarelas",
    "azul": "azuis",
    "verde": "verdes",
    "vermel": "vermelhas",
    "branc": "brancas",
    "pret": "pretas",
}
POISSON_KEYWORDS = (
    "por hora",
    "por minuto",
    "por segundo",
    "por dia",
    "por semana",
    "taxa media",
    "taxa média",
    "eventos por",
    "chegadas",
    "clientes por",
    "contagem por",
)
EXPONENTIAL_KEYWORDS = (
    "tempo ate",
    "tempo até",
    "tempo de espera",
    "vida util",
    "vida útil",
    "duracao ate",
    "duração até",
    "falha",
    "entre falhas",
)
BINOMIAL_KEYWORDS = (
    "com repos",
    "com reposição",
    "com reposicao",
    "independen",
    "tentativas identicas",
    "ensaios bernoulli",
)


def _resumo_distribuicoes_basicas() -> str:
    """Retorna uma string amigável com parâmetros das distribuições base."""

    descricoes = []
    for nome, dist in COMMON_DISTRIBUTIONS.items():
        parametros = getattr(dist, "shapes", None) or "loc, scale"
        descricoes.append(f"{nome} ({parametros})")
    return ", ".join(descricoes)


class Cores:
    """Cores para terminal."""

    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


@dataclass
class RespostaSmither:
    """Representa o retorno padronizado do Smither para o usuário."""

    sucesso: bool
    mensagem: str


def _converter_float(texto: str) -> float:
    """Converte string em float aceitando vírgula."""

    return float(texto.replace(",", "."))


def _ler_float(prompt: str, minimo: float | None = None, maximo: float | None = None) -> float:
    """Lê um float do usuário respeitando limites opcionais."""

    while True:
        entrada = input(prompt).strip()
        try:
            valor = _converter_float(entrada)
        except ValueError:
            print(f"{Cores.FAIL}Digite um número válido.{Cores.ENDC}")
            continue

        if minimo is not None and valor < minimo:
            print(f"{Cores.FAIL}O valor deve ser >= {minimo}.{Cores.ENDC}")
            continue
        if maximo is not None and valor > maximo:
            print(f"{Cores.FAIL}O valor deve ser <= {maximo}.{Cores.ENDC}")
            continue
        return valor


def _ler_float_opcional(
    prompt: str,
    padrao: float | None,
    minimo: float | None = None,
    maximo: float | None = None,
) -> float | None:
    """Lê um float opcional; Enter retorna o padrão."""

    while True:
        entrada = input(prompt).strip()
        if not entrada:
            return padrao
        try:
            valor = _converter_float(entrada)
        except ValueError:
            print(f"{Cores.FAIL}Digite um número válido ou deixe em branco para usar o padrão.{Cores.ENDC}")
            continue

        if minimo is not None and valor < minimo:
            print(f"{Cores.FAIL}O valor deve ser >= {minimo}.{Cores.ENDC}")
            continue
        if maximo is not None and valor > maximo:
            print(f"{Cores.FAIL}O valor deve ser <= {maximo}.{Cores.ENDC}")
            continue
        return valor


def _ler_int(prompt: str, minimo: int | None = None, maximo: int | None = None) -> int:
    """Lê um inteiro do usuário respeitando limites opcionais."""

    while True:
        entrada = input(prompt).strip()
        try:
            valor = int(entrada)
        except ValueError:
            print(f"{Cores.FAIL}Digite um inteiro válido.{Cores.ENDC}")
            continue

        if minimo is not None and valor < minimo:
            print(f"{Cores.FAIL}O valor deve ser >= {minimo}.{Cores.ENDC}")
            continue
        if maximo is not None and valor > maximo:
            print(f"{Cores.FAIL}O valor deve ser <= {maximo}.{Cores.ENDC}")
            continue
        return valor


def _ler_int_opcional(
    prompt: str,
    padrao: int | None,
    minimo: int | None = None,
    maximo: int | None = None,
) -> int | None:
    """Lê um inteiro opcional; Enter mantém o padrão."""

    while True:
        entrada = input(prompt).strip()
        if not entrada:
            return padrao
        try:
            valor = int(entrada)
        except ValueError:
            print(f"{Cores.FAIL}Digite um inteiro válido ou deixe em branco para usar o padrão.{Cores.ENDC}")
            continue

        if minimo is not None and valor < minimo:
            print(f"{Cores.FAIL}O valor deve ser >= {minimo}.{Cores.ENDC}")
            continue
        if maximo is not None and valor > maximo:
            print(f"{Cores.FAIL}O valor deve ser <= {maximo}.{Cores.ENDC}")
            continue
        return valor


def _converter_limite_sympy(valor: float) -> sp.Expr:
    """Converte limites (incluindo infinito) para objetos SymPy."""

    if math.isinf(valor):
        return sp.oo if valor > 0 else -sp.oo
    return sp.Float(valor)


def _avaliar_positividade_amostral(expr: sp.Expr, var, inferior: float, superior: float, pontos: int = 25) -> bool | None:
    """Verifica se a fdp é não-negativa amostrando pontos (se intervalo finito)."""

    if math.isinf(inferior) or math.isinf(superior):
        return None

    xs = np.linspace(inferior, superior, pontos)
    for x in xs:
        try:
            valor = expr.subs(var, x)
            valor_float = float(sp.N(valor))
        except Exception:  # pylint: disable=broad-except
            return None
        if valor_float < -1e-9:
            return False
    return True


def _coletar_problema_usuario() -> str:
    """Captura um problema estatístico em formato livre."""

    print("\nDescreva o problema estatístico (ENTER em branco finaliza):")
    print(
        f"Distribuições básicas disponíveis para checagens rápidas: "
        f"{_resumo_distribuicoes_basicas()}"
    )
    linhas: list[str] = []

    while True:
        try:
            linha = input("  > ")
        except EOFError:  # Permite sair com Ctrl+D
            print("")
            break

        if not linha.strip():
            break

        linhas.append(linha.strip())

    return "\n".join(linhas).strip()


def _gerar_prompt_para_openai(problema: str) -> list[dict[str, str]]:
    """Constrói o prompt enviado para a API da OpenAI."""

    pilha_formatada = ", ".join(f"{nome} {versao}" for nome, versao in STAT_STACK.items())

    system_prompt = dedent(
        """
        Você é o Smither, um assistente especializado em estatística e inferência.
        Forneça sempre sua resposta em português, estruturando-a com:
        1. Distribuição recomendada.
        2. Justificativa curta (máximo 3 frases).
        3. Lista dos parâmetros necessários e dicas para estimá-los.
        Se o problema não tiver informação suficiente, explique o que falta.
        """
    ).strip()

    user_prompt = dedent(
        f"""
        Problema estatístico informado pelo usuário:
        {problema.strip()}

        Objetivo: Informe qual distribuição de probabilidade deve ser usada
        para modelar o problema e quais parâmetros são relevantes.
        Considerar que o ambiente possui bibliotecas estatísticas:
        {pilha_formatada}
        """
    ).strip()

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def _normalizar_categoria(palavra: str) -> str | None:
    """Mapeia palavras para categorias conhecidas (azul, verde, etc.)."""

    palavra = palavra.lower()
    for raiz, canonical in COLOR_ALIASES.items():
        if palavra.startswith(raiz):
            return canonical
    return None


def _extrair_contagens_por_categoria(texto: str) -> dict[str, int]:
    """Retorna um dicionário categoria->quantidade com base na descrição."""

    contagens: dict[str, int] = {}
    for numero, palavra in re.findall(r"(\d+)\s+(\w+)", texto):
        categoria = _normalizar_categoria(palavra)
        if categoria:
            contagens[categoria] = contagens.get(categoria, 0) + int(numero)
    return contagens


def _extrair_tamanho_amostra(texto: str) -> int | None:
    """Detecta quantas unidades serão retiradas/observadas."""

    match = re.search(r"(\d+)\s+bol", texto)
    if match:
        return int(match.group(1))

    for palavra, valor in NUMBER_WORDS.items():
        if re.search(rf"\b{palavra}\b\s+bol", texto):
            return valor

    for palavra, valor in NUMBER_WORDS.items():
        if re.search(rf"\b{palavra}\b", texto):
            return valor

    return None


def _comb_safe(n: int, k: int) -> int | None:
    """Versão segura de comb() para evitar ValueError."""

    if n < 0 or k < 0 or k > n:
        return None
    return comb(n, k)


def _resposta_local(problema: str) -> RespostaSmither:
    """Fornece recomendações heurísticas quando a OpenAI não está disponível."""

    texto = problema.lower()
    if not texto:
        return RespostaSmither(False, "Nenhum problema foi informado.")

    if "sem repos" in texto:
        return _resposta_hipergeometrica(problema)

    if any(keyword in texto for keyword in BINOMIAL_KEYWORDS):
        return _resposta_binomial(problema)

    if any(keyword in texto for keyword in POISSON_KEYWORDS):
        return _resposta_poisson(problema)

    if any(keyword in texto for keyword in EXPONENTIAL_KEYWORDS):
        return _resposta_exponencial(problema)

    return RespostaSmither(
        False,
        "Não foi possível identificar uma distribuição apenas com heurísticas locais.",
    )


def _resposta_hipergeometrica(problema: str) -> RespostaSmither:
    """Gera instruções para cenários sem reposição."""

    texto = problema.lower()
    contagens = _extrair_contagens_por_categoria(texto)
    total = sum(contagens.values()) or None
    interesse = None
    for chave, valor in contagens.items():
        if chave.startswith("amarel"):
            interesse = valor
            break
    amostra = _extrair_tamanho_amostra(texto)

    parametros = [
        f"- N (total de itens) = {total}." if total else "- N (total de itens) = informe a soma dos elementos disponíveis.",
        f"- K (itens de interesse, ex.: amarelas) = {interesse}." if interesse is not None else "- K (itens de interesse) = informe quantos itens atendem ao critério.",
        f"- n (quantidade de retiradas) = {amostra}." if amostra else "- n (quantidade de retiradas) = informe quantos itens serão retirados.",
    ]

    detalhes_prob = []
    if total and interesse is not None and amostra:
        denom = _comb_safe(total, amostra)
        if denom:
            sem_sucesso = _comb_safe(total - interesse, amostra) or 0
            prob_ao_menos_um = 1 - (sem_sucesso / denom)
            detalhes_prob.append(
                f"Probabilidade de pelo menos 1 sucesso: {prob_ao_menos_um:.4f} (~{prob_ao_menos_um * 100:.2f}%)."
            )

            if amostra >= 1:
                comb_sucesso = _comb_safe(interesse, 1) or 0
                comb_restante = _comb_safe(total - interesse, amostra - 1) or 0
                prob_exatamente_um = (comb_sucesso * comb_restante) / denom if denom else None
                if prob_exatamente_um is not None:
                    detalhes_prob.append(
                        f"Probabilidade de exatamente 1 sucesso: {prob_exatamente_um:.4f} (~{prob_exatamente_um * 100:.2f}%)."
                    )
        else:
            detalhes_prob.append("Verifique se n <= N para aplicar a distribuição hipergeométrica.")
    else:
        detalhes_prob.append("Use P(X = k) = [C(K, k) * C(N-K, n-k)] / C(N, n) e adapte k conforme o problema.")

    mensagem = (
        "Distribuição recomendada: Hipergeométrica (amostragem sem reposição).\n"
        "Justificativa: uma população finita é amostrada sem reposição, então a probabilidade muda a cada retirada.\n"
        "Parâmetros sugeridos:\n"
        + "\n".join(parametros)
        + "\n"
        + "\n".join(detalhes_prob)
        + "\nFórmula geral: P(X = k) = [C(K, k) * C(N-K, n-k)] / C(N, n).\n"
        "Esta resposta foi gerada localmente (sem consulta à OpenAI) com base em heurísticas.\n"
        "Configure OPENAI_API_KEY para que o Smither avalie casos mais complexos com o modelo completo."
    )

    return RespostaSmither(True, mensagem)


def _resposta_binomial(problema: str) -> RespostaSmither:
    """Sugestão de distribuição binomial para cenários com reposição/independência."""

    mensagem = (
        "Distribuição recomendada: Binomial.\n"
        "Justificativa: ensaios independentes com apenas dois resultados possíveis em cada tentativa.\n"
        "Parâmetros necessários:\n"
        "- n: número de tentativas (ex.: quantidade de retiradas com reposição ou experimentos idênticos).\n"
        "- p: probabilidade de sucesso em cada tentativa.\n"
        "Use P(X = k) = C(n, k) * p^k * (1-p)^(n-k).\n"
        "Para a probabilidade acumulada, some os termos desejados ou utilize funções CDF da distribuição binomial.\n"
        "Esta resposta foi gerada localmente (sem consulta à OpenAI).\n"
        "Configure OPENAI_API_KEY para obter análises completas do Smither."
    )
    return RespostaSmither(True, mensagem)


def _resposta_poisson(problema: str) -> RespostaSmither:
    """Sugestão de distribuição de Poisson para contagens em intervalos de tempo/área."""

    mensagem = (
        "Distribuição recomendada: Poisson.\n"
        "Justificativa: contagem de eventos raros em um intervalo fixo com taxa média lambda constante.\n"
        "Parâmetros necessários:\n"
        "- lambda: taxa média de ocorrências por intervalo (ex.: chegadas por hora).\n"
        "Use P(X = k) = exp(-lambda) * lambda^k / k! e ajuste o intervalo multiplicando lambda conforme a duração.\n"
        "Para probabilidades acumuladas, utilize a CDF da Poisson ou some os termos relevantes.\n"
        "Esta resposta foi gerada localmente (sem consulta à OpenAI).\n"
        "Configure OPENAI_API_KEY para obter análises completas do Smither."
    )
    return RespostaSmither(True, mensagem)


def _resposta_exponencial(problema: str) -> RespostaSmither:
    """Sugestão de distribuição exponencial para tempos de espera/vida útil."""

    mensagem = (
        "Distribuição recomendada: Exponencial.\n"
        "Justificativa: modelagem de tempo contínuo até o próximo evento em processos com taxa constante.\n"
        "Parâmetros necessários:\n"
        "- lambda: taxa média de ocorrência dos eventos (lambda = 1/tempo_medio).\n"
        "Função densidade: f(t) = lambda * exp(-lambda * t); Probabilidade acumulada: P(T <= t) = 1 - exp(-lambda * t).\n"
        "Esta resposta foi gerada localmente (sem consulta à OpenAI).\n"
        "Configure OPENAI_API_KEY para obter análises completas do Smither."
    )
    return RespostaSmither(True, mensagem)


def _consultar_smither_distribuicao(problema: str) -> RespostaSmither:
    """Encaminha o problema para a OpenAI e devolve a sugestão de distribuição."""

    if not problema:
        return RespostaSmither(False, "Nenhum problema foi informado.")

    if OpenAI is None:
        fallback = _resposta_local(problema)
        if fallback.sucesso:
            return fallback
        return RespostaSmither(
            False,
            "Biblioteca 'openai' não encontrada. Instale-a e configure o ambiente.",
        )

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        fallback = _resposta_local(problema)
        if fallback.sucesso:
            return fallback
        return RespostaSmither(
            False,
            "Defina a variável de ambiente OPENAI_API_KEY para usar o Smither.",
        )

    try:
        client = OpenAI(api_key=api_key)
    except Exception as exc:  # pragma: no cover - falha apenas em runtime
        fallback = _resposta_local(problema)
        if fallback.sucesso:
            return fallback
        return RespostaSmither(False, f"Não foi possível iniciar o cliente OpenAI: {exc}")

    mensagens = _gerar_prompt_para_openai(problema)

    try:
        resposta = client.responses.create(
            model=DEFAULT_OPENAI_MODEL,
            input=mensagens,
            max_output_tokens=400,
            temperature=0.2,
        )
    except Exception as exc:  # pragma: no cover - depende do runtime externo
        fallback = _resposta_local(problema)
        if fallback.sucesso:
            return fallback
        return RespostaSmither(False, f"Erro ao consultar a OpenAI: {exc}")

    mensagem = _extrair_texto_resposta(resposta)
    if not mensagem:
        fallback = _resposta_local(problema)
        if fallback.sucesso:
            return fallback
        return RespostaSmither(
            False,
            "Resposta vazia recebida da OpenAI. Tente novamente em instantes.",
        )

    return RespostaSmither(True, mensagem)


def _extrair_texto_resposta(payload) -> str:
    """Extrai o texto principal do payload retornado pela API Responses."""

    try:
        conteudo = payload.output[0].content  # type: ignore[index]
        if conteudo and hasattr(conteudo[0], "text"):
            return conteudo[0].text.strip()  # type: ignore[attr-defined]
    except (AttributeError, IndexError, KeyError, TypeError):
        return ""

    return ""


def _pergunte_ao_smither():
    """Fluxo principal da opção 'Pergunte ao Smither'."""

    problema = _coletar_problema_usuario()
    resultado = _consultar_smither_distribuicao(problema)

    if resultado.sucesso:
        print(f"\n{Cores.OKGREEN}Sugestão do Smither:{Cores.ENDC}\n")
        print(resultado.mensagem)
    else:
        print(f"\n{Cores.FAIL}Não foi possível obter uma recomendação:{Cores.ENDC}")
        print(resultado.mensagem)


def _menu_distribuicoes():
    """Menu intermediário para cálculos de distribuições."""

    while True:
        print("\n" + "-" * 70)
        print("                   DISTRIBUIÇÕES PROBABILÍSTICAS")
        print("-" * 70)
        print("  1. Distribuições discretas")
        print("  2. Distribuições contínuas")
        print(f"\n  {Cores.OKBLUE}0{Cores.ENDC}. Voltar\n")

        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            break
        if escolha == "1":
            _menu_discretas()
            continue
        if escolha == "2":
            _menu_continuas()
            continue
        print(f"{Cores.FAIL}[Erro] Opção inválida!{Cores.ENDC}")


def _menu_discretas():
    """Submenu com distribuições discretas suportadas."""

    while True:
        print("\n  -- Distribuições Discretas --")
        print("    1. Binomial")
        print("    2. Poisson")
        print("    3. Hipergeométrica")
        print(f"    {Cores.OKBLUE}0{Cores.ENDC}. Voltar\n")

        escolha = input("Selecione a distribuição: ").strip()
        if escolha == "0":
            break
        if escolha == "1":
            _calcular_binomial()
            continue
        if escolha == "2":
            _calcular_poisson()
            continue
        if escolha == "3":
            _calcular_hipergeometrica()
            continue
        print(f"{Cores.FAIL}[Erro] Opção inválida!{Cores.ENDC}")


def _menu_continuas():
    """Submenu com distribuições contínuas suportadas."""

    while True:
        print("\n  -- Distribuições Contínuas --")
        print("    1. Normal")
        print("    2. Exponencial")
        print("    3. Uniforme")
        print(f"    {Cores.OKBLUE}0{Cores.ENDC}. Voltar\n")

        escolha = input("Selecione a distribuição: ").strip()
        if escolha == "0":
            break
        if escolha == "1":
            _calcular_normal()
            continue
        if escolha == "2":
            _calcular_exponencial()
            continue
        if escolha == "3":
            _calcular_uniforme()
            continue
        print(f"{Cores.FAIL}[Erro] Opção inválida!{Cores.ENDC}")


def _calcular_binomial():
    """Calcula probabilidades para a distribuição binomial."""

    print(f"\n{Cores.OKCYAN}Distribuição Binomial{Cores.ENDC}")
    n = _ler_int("Número de tentativas (n): ", minimo=0)
    p = _ler_float("Probabilidade de sucesso (p, entre 0 e 1): ", minimo=0.0, maximo=1.0)
    k_min = _ler_int("Número mínimo de sucessos (k_min): ", minimo=0, maximo=n)
    k_max = _ler_int_opcional(
        "Número máximo de sucessos (k_max) [ENTER para usar o mesmo valor]: ",
        padrao=k_min,
        minimo=k_min,
        maximo=n,
    )
    if k_max is None:
        k_max = k_min

    dist = stats.binom(n=n, p=p)
    prob = float(sum(dist.pmf(k) for k in range(k_min, k_max + 1)))
    media = n * p
    variancia = n * p * (1 - p)

    print(f"\n{Cores.OKGREEN}Resultados:{Cores.ENDC}")
    print(f"P({k_min} ≤ X ≤ {k_max}) = {prob:.6f} ({prob*100:.4f}%)")
    print(f"Média: {media:.4f} | Variância: {variancia:.4f}")


def _calcular_poisson():
    """Calcula probabilidades para a distribuição de Poisson."""

    print(f"\n{Cores.OKCYAN}Distribuição de Poisson{Cores.ENDC}")
    lam = _ler_float("Taxa média (lambda > 0): ", minimo=0.0)
    k_min = _ler_int("Contagem mínima (k_min): ", minimo=0)
    k_max = _ler_int_opcional(
        "Contagem máxima (k_max) [ENTER para usar o mesmo valor]: ",
        padrao=k_min,
        minimo=k_min,
    )
    if k_max is None:
        k_max = k_min

    dist = stats.poisson(mu=lam)
    prob = float(sum(dist.pmf(k) for k in range(k_min, k_max + 1)))
    print(f"\n{Cores.OKGREEN}Resultados:{Cores.ENDC}")
    print(f"P({k_min} ≤ X ≤ {k_max}) = {prob:.6f} ({prob*100:.4f}%)")
    print(f"Média = Variância = {lam:.4f}")


def _calcular_hipergeometrica():
    """Calcula probabilidades para a distribuição hipergeométrica."""

    print(f"\n{Cores.OKCYAN}Distribuição Hipergeométrica{Cores.ENDC}")
    populacao = _ler_int("Tamanho da população (N): ", minimo=1)
    sucesso_total = _ler_int("Número de itens de interesse na população (K): ", minimo=0, maximo=populacao)
    amostra = _ler_int("Tamanho da amostra (n): ", minimo=1, maximo=populacao)
    k_min = _ler_int("Sucessos mínimos desejados (k_min): ", minimo=0, maximo=amostra)
    k_max = _ler_int_opcional(
        "Sucessos máximos desejados (k_max) [ENTER para usar o mesmo valor]: ",
        padrao=k_min,
        minimo=k_min,
        maximo=amostra,
    )
    if k_max is None:
        k_max = k_min

    dist = stats.hypergeom(M=populacao, n=sucesso_total, N=amostra)
    prob = float(sum(dist.pmf(k) for k in range(k_min, k_max + 1)))

    print(f"\n{Cores.OKGREEN}Resultados:{Cores.ENDC}")
    print(f"P({k_min} ≤ X ≤ {k_max}) = {prob:.6f} ({prob*100:.4f}%)")
    esperanca = amostra * (sucesso_total / populacao)
    if populacao > 1:
        variancia = esperanca * ((populacao - sucesso_total) / (populacao - 1)) * ((populacao - amostra) / populacao)
    else:
        variancia = 0.0
    print(f"Média: {esperanca:.4f}")
    print(f"Variância: {variancia:.4f}")


def _solicitar_limites_continuos() -> tuple[float, float]:
    """Solicita limites inferior/superior para integrações em distribuições contínuas."""

    while True:
        inferior_txt = input("Limite inferior (ENTER para -inf): ").strip()
        superior_txt = input("Limite superior (ENTER para +inf): ").strip()
        try:
            inferior = -float("inf") if not inferior_txt else _converter_float(inferior_txt)
            superior = float("inf") if not superior_txt else _converter_float(superior_txt)
        except ValueError:
            print(f"{Cores.FAIL}Informe números válidos ou deixe em branco para infinito.{Cores.ENDC}")
            continue

        if superior < inferior:
            print(f"{Cores.FAIL}O limite superior deve ser maior ou igual ao inferior.{Cores.ENDC}")
            continue
        return inferior, superior


def _calcular_normal():
    """Calcula probabilidade acumulada para a normal."""

    print(f"\n{Cores.OKCYAN}Distribuição Normal{Cores.ENDC}")
    media = _ler_float("Média (μ): ")
    desvio = _ler_float("Desvio padrão (σ > 0): ", minimo=0.0)
    while desvio <= 0:
        print(f"{Cores.FAIL}O desvio padrão deve ser positivo.{Cores.ENDC}")
        desvio = _ler_float("Desvio padrão (σ > 0): ", minimo=0.0)

    limite_inferior, limite_superior = _solicitar_limites_continuos()
    dist = stats.norm(loc=media, scale=desvio)
    prob = float(dist.cdf(limite_superior) - dist.cdf(limite_inferior))
    print(f"\n{Cores.OKGREEN}Resultados:{Cores.ENDC}")
    print(f"P({limite_inferior} ≤ X ≤ {limite_superior}) = {prob:.6f} ({prob*100:.4f}%)")


def _calcular_exponencial():
    """Calcula probabilidade acumulada para a exponencial."""

    print(f"\n{Cores.OKCYAN}Distribuição Exponencial{Cores.ENDC}")
    lam = _ler_float("Taxa lambda (> 0): ", minimo=0.0)
    while lam <= 0:
        print(f"{Cores.FAIL}Lambda deve ser maior que zero.{Cores.ENDC}")
        lam = _ler_float("Taxa lambda (> 0): ", minimo=0.0)

    limite_inferior, limite_superior = _solicitar_limites_continuos()
    if limite_superior <= 0 and limite_inferior <= 0:
        # Ambos negativos => probabilidade zero
        prob = 0.0
    else:
        inferior = max(0.0, limite_inferior)
        dist = stats.expon(scale=1 / lam)
        prob = float(dist.cdf(limite_superior) - dist.cdf(inferior))

    print(f"\n{Cores.OKGREEN}Resultados:{Cores.ENDC}")
    print(f"P({limite_inferior} ≤ X ≤ {limite_superior}) = {prob:.6f} ({prob*100:.4f}%)")
    print("Observação: a distribuição exponencial é definida para valores >= 0.")


def _calcular_uniforme():
    """Calcula probabilidade para a distribuição uniforme contínua."""

    print(f"\n{Cores.OKCYAN}Distribuição Uniforme Contínua{Cores.ENDC}")
    while True:
        a = _ler_float("Limite inferior da distribuição (a): ")
        b = _ler_float("Limite superior da distribuição (b): ")
        if b <= a:
            print(f"{Cores.FAIL}É necessário que b > a.{Cores.ENDC}")
            continue
        break

    limite_inferior, limite_superior = _solicitar_limites_continuos()
    inferior = max(limite_inferior, a)
    superior = min(limite_superior, b)
    if superior < inferior:
        prob = 0.0
    else:
        dist = stats.uniform(loc=a, scale=b - a)
        prob = float(dist.cdf(superior) - dist.cdf(inferior))

    print(f"\n{Cores.OKGREEN}Resultados:{Cores.ENDC}")
    print(f"P({limite_inferior} ≤ X ≤ {limite_superior}) = {prob:.6f} ({prob*100:.4f}%)")
    print(f"Suporte da distribuição: [{a}, {b}]")


def _verificar_funcao_pdf():
    """Verifica se uma função é uma fdp válida ou resolve K."""

    print(f"\n{Cores.OKCYAN}Verificação de Função Densidade de Probabilidade{Cores.ENDC}")
    var_nome = input("Variável (default = x): ").strip() or "x"
    funcao_txt = input("Informe f(x): ").strip()
    if not funcao_txt:
        print(f"{Cores.FAIL}É necessário informar uma função.{Cores.ENDC}")
        return

    tem_k = input("A função possui constante K? (s/n): ").strip().lower().startswith("s")
    limite_inferior, limite_superior = _solicitar_limites_continuos()

    var = sp.symbols(var_nome, real=True)
    k_sym = sp.symbols("K", real=True)

    try:
        expr = sp.sympify(
            funcao_txt,
            locals={
                var_nome: var,
                "K": k_sym,
                "k": k_sym,
            },
        )
    except (sp.SympifyError, ValueError) as exc:
        print(f"{Cores.FAIL}Não foi possível interpretar a função: {exc}{Cores.ENDC}")
        return

    if not tem_k and k_sym in expr.free_symbols:
        print(f"{Cores.WARNING}A função contém 'K', mas você indicou que não existe constante. Considere responder 's'.{Cores.ENDC}")

    limite_inf_sym = _converter_limite_sympy(limite_inferior)
    limite_sup_sym = _converter_limite_sympy(limite_superior)

    try:
        integral_expr = sp.integrate(expr, (var, limite_inf_sym, limite_sup_sym))
    except Exception as exc:  # pylint: disable=broad-except
        print(f"{Cores.FAIL}Não foi possível integrar a função: {exc}{Cores.ENDC}")
        return

    if tem_k:
        equacao = sp.Eq(sp.simplify(integral_expr), 1)
        try:
            solucoes = sp.solve(equacao, k_sym, dict=True)
        except Exception as exc:  # pylint: disable=broad-except
            print(f"{Cores.FAIL}Não foi possível resolver para K: {exc}{Cores.ENDC}")
            return

        if not solucoes:
            print(f"{Cores.FAIL}Nenhum valor de K satisfaz a condição de integral igual a 1.{Cores.ENDC}")
            print(f"Integral obtida: {sp.simplify(integral_expr)}")
            return

        print(f"\n{Cores.OKGREEN}Valores possíveis para K:{Cores.ENDC}")
        for idx, sol in enumerate(solucoes, start=1):
            valor_k = sol.get(k_sym)
            print(f"  {idx}. K = {valor_k}")
        print("Verifique adicionalmente a não negatividade da função no suporte informado.")
        return

    integral_val = sp.N(integral_expr)

    if not integral_val.is_real:
        print(f"{Cores.FAIL}A integral resultou em um valor não real: {integral_expr}{Cores.ENDC}")
        return

    tolerancia = 1e-6
    integral_ok = abs(float(integral_val) - 1.0) <= tolerancia

    analise_positiva = _avaliar_positividade_amostral(expr, var, limite_inferior, limite_superior)
    if integral_ok:
        print(f"{Cores.OKGREEN}A integral da função no intervalo informado é 1 (valor calculado: {float(integral_val):.6f}).{Cores.ENDC}")
    else:
        print(f"{Cores.FAIL}A integral calculada foi {float(integral_val):.6f}, diferente de 1.{Cores.ENDC}")

    if analise_positiva is True:
        print(f"{Cores.OKGREEN}Amostragem numérica indica que a função é não negativa no intervalo.{Cores.ENDC}")
    elif analise_positiva is False:
        print(f"{Cores.FAIL}Foram encontrados valores negativos na função dentro do intervalo.{Cores.ENDC}")
    else:
        print(f"{Cores.WARNING}Não foi possível verificar numericamente a não negatividade (intervalo infinito ou função complexa).{Cores.ENDC}")

    if integral_ok and (analise_positiva in (True, None)):
        print(f"{Cores.OKGREEN}Conclusão: a função atende aos requisitos de uma fdp (assumindo não negatividade).{Cores.ENDC}")
    else:
        print(f"{Cores.WARNING}Conclusão: a função NÃO atende totalmente aos critérios de fdp. Revise os requisitos acima.{Cores.ENDC}")


def _coletar_dados_tabela() -> list[float]:
    """Coleta dados numéricos livres digitados pelo usuário."""

    print("\nDigite os valores (use vírgula ou espaço como separador).")
    print("Pressione ENTER em branco para finalizar a entrada.")
    valores: list[float] = []

    while True:
        linha = input("  Linha de dados: ").strip()
        if not linha:
            break

        for pedaco in re.split(r"[;,\s]+", linha):
            texto = pedaco.strip()
            if not texto:
                continue
            try:
                valores.append(_converter_float(texto))
            except ValueError:
                print(f"{Cores.WARNING}Valor ignorado (não numérico): '{texto}'{Cores.ENDC}")

    return valores


def _interpretar_skewness(valor: float) -> str:
    """Classifica a assimetria com base na skewness."""

    if math.isnan(valor):
        return "Indefinida (todos os valores são iguais)."
    if valor > 0.5:
        return "Assimetria positiva (cauda à direita)."
    if valor < -0.5:
        return "Assimetria negativa (cauda à esquerda)."
    return "Distribuição aproximadamente simétrica."


def _interpretar_kurtosis(valor: float) -> str:
    """Classifica a curtose com base no excesso de Fisher."""

    if math.isnan(valor):
        return "Indefinida (todos os valores são iguais)."
    if valor > 0.5:
        return "Leptocúrtica (caudas pesadas/afunilada)."
    if valor < -0.5:
        return "Platicúrtica (achatada)."
    return "Mesocúrtica (similar à Normal)."


def _formatar_valor_metrica(valor) -> str:
    """Converte métricas em strings amigáveis."""

    if isinstance(valor, (list, tuple, np.ndarray, pd.Series)):
        return ", ".join(_formatar_valor_metrica(v) for v in valor)
    if isinstance(valor, (int, np.integer)):
        return str(int(valor))
    if isinstance(valor, (float, np.floating)):
        if math.isnan(float(valor)):
            return "—"
        return f"{float(valor):.6g}"
    return str(valor)


def _gerar_resumo_metricas(serie: pd.Series) -> list[tuple[str, str]]:
    """Retorna uma lista com métricas resumidas formatadas."""

    desc = serie.describe()
    amplitude = float(serie.max() - serie.min())
    variancia = float(serie.var(ddof=1)) if len(serie) > 1 else float("nan")
    desvio = float(serie.std(ddof=1)) if len(serie) > 1 else float("nan")
    coef_var = (
        (desvio / float(desc["mean"])) * 100
        if len(serie) > 1 and not math.isclose(float(desc["mean"]), 0.0)
        else float("nan")
    )
    moda = serie.mode().tolist()
    skew = float(serie.skew()) if len(serie) > 2 else float("nan")
    kurt = float(serie.kurtosis()) if len(serie) > 3 else float("nan")
    q1 = float(serie.quantile(0.25))
    q3 = float(serie.quantile(0.75))
    iqr = q3 - q1

    metricas = [
        ("Quantidade de observações", int(desc["count"])),
        ("Valores únicos", int(serie.nunique())),
        ("Mínimo", float(desc["min"])),
        ("Q1 (25%)", q1),
        ("Mediana (50%)", float(desc["50%"])),
        ("Q3 (75%)", q3),
        ("Máximo", float(desc["max"])),
        ("Amplitude", amplitude),
        ("Média", float(desc["mean"])),
        ("Moda", moda or ["—"]),
        ("Variância amostral", variancia),
        ("Desvio padrão amostral", desvio),
        ("Coeficiente de variação (%)", coef_var),
        ("Assimetria (skewness)", skew),
        ("Classificação da assimetria", _interpretar_skewness(skew)),
        ("Curtose (excesso de Fisher)", kurt),
        ("Classificação da curtose", _interpretar_kurtosis(kurt)),
        ("Intervalo interquartílico (IQR)", iqr),
        ("Soma", float(serie.sum())),
    ]

    return [(nome, _formatar_valor_metrica(valor)) for nome, valor in metricas]


def _gerar_tabela_frequencias(serie: pd.Series, discreto: bool) -> pd.DataFrame:
    """Gera tabela de frequências (discreta ou contínua)."""

    n = len(serie)
    if discreto:
        freq_abs = serie.value_counts().sort_index()
        df = freq_abs.to_frame(name="Frequência")
        df["Frequência Relativa (%)"] = (df["Frequência"] / n * 100).round(2)
        df["Freq. Acumulada (%)"] = df["Frequência Relativa (%)"].cumsum().round(2)
        df.index.name = "Valor"
        return df.reset_index()

    bins = max(5, min(15, int(np.ceil(np.log2(n) + 1))))
    minimo = float(serie.min())
    maximo = float(serie.max())
    if math.isclose(minimo, maximo):
        largura = max(abs(minimo) * 0.1, 1.0)
        edges = np.array([minimo - largura / 2, maximo + largura / 2])
    else:
        edges = np.histogram_bin_edges(serie, bins=bins)

    contagens, edges = np.histogram(serie, bins=edges)
    linhas: list[dict[str, object]] = []
    acumulada = 0.0
    for idx, freq in enumerate(contagens):
        if freq == 0:
            continue
        limite_inf = edges[idx]
        limite_sup = edges[idx + 1]
        largura = limite_sup - limite_inf
        freq_rel = (freq / n) * 100
        acumulada += freq_rel
        densidade = freq / (n * largura) if largura > 0 else float("nan")
        classe = f"[{limite_inf:.6g}, {limite_sup:.6g}" + ("]" if idx == len(contagens) - 1 else ")")
        linhas.append(
            {
                "Classe": classe,
                "Frequência": freq,
                "Frequência Relativa (%)": round(freq_rel, 2),
                "Freq. Acumulada (%)": round(acumulada, 2),
                "Densidade": round(densidade, 4) if not math.isnan(densidade) else "—",
            }
        )

    return pd.DataFrame(linhas)


def _ensure_output_dir_estatistica() -> Path:
    out = Path.cwd() / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    return out


def _unix_display_session_available_estatistica() -> bool:
    return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def _should_save_plots_estatistica() -> bool:
    """Replica a lógica de detecção headless usada nos demais módulos."""

    try:
        backend = matplotlib.get_backend().lower()
        if "agg" in backend:
            return True
    except Exception:  # pragma: no cover
        pass

    if os.environ.get("HEADLESS") or os.environ.get("CI"):
        return True
    if os.name != "nt" and sys.platform != "darwin" and not _unix_display_session_available_estatistica():
        return True
    return False


def _finalizar_figura_estatistica(fig, nome_base: str, salvar: bool | None):
    """Salva ou mostra figura conforme configuração."""

    do_save = _should_save_plots_estatistica() if salvar is None else bool(salvar)
    fig.tight_layout()
    if do_save:
        destino = _ensure_output_dir_estatistica() / f"{nome_base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig.savefig(destino, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"{Cores.OKGREEN}Gráfico salvo em: {destino}{Cores.ENDC}")
    else:
        plt.show()


def _gerar_graficos_tabela(serie: pd.Series, discreto: bool, salvar: bool | None):
    """Cria gráficos de distribuição, boxplot e ECDF."""

    if discreto:
        freq = serie.value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.bar(freq.index.astype(str), freq.values, color="#4C72B0", alpha=0.85)
        ax.set_title("Distribuição Discreta (Frequências)")
        ax.set_xlabel("Valor")
        ax.set_ylabel("Frequência absoluta")
        ax.grid(axis="y", alpha=0.2)
        _finalizar_figura_estatistica(fig, "distribuicao_discreta", salvar)
    else:
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.hist(serie, bins="auto", color="#55A868", alpha=0.7, edgecolor="black", density=True)
        if serie.nunique() > 1:
            try:
                kde = stats.gaussian_kde(serie)
                xs = np.linspace(float(serie.min()), float(serie.max()), 200)
                ax.plot(xs, kde(xs), color="#C44E52", linewidth=2, label="KDE")
                ax.legend()
            except Exception:  # pragma: no cover - pode falhar com dados degenerados
                pass
        ax.set_title("Distribuição Contínua (Histograma + KDE)")
        ax.set_xlabel("Valor")
        ax.set_ylabel("Densidade")
        ax.grid(alpha=0.2)
        _finalizar_figura_estatistica(fig, "distribuicao_continua", salvar)

    fig_box, ax_box = plt.subplots(figsize=(9, 2.8))
    ax_box.boxplot(serie, vert=False, patch_artist=True, boxprops=dict(facecolor="#9C9EFE", alpha=0.6))
    ax_box.set_title("Boxplot / Quartis")
    ax_box.set_xlabel("Valores")
    ax_box.grid(axis="x", alpha=0.2)
    _finalizar_figura_estatistica(fig_box, "boxplot_dados", salvar)

    valores_ordenados = np.sort(serie)
    probs = np.arange(1, len(valores_ordenados) + 1) / len(valores_ordenados)
    fig_ecdf, ax_ecdf = plt.subplots(figsize=(9, 4))
    ax_ecdf.step(valores_ordenados, probs, where="post", color="#DD8452")
    ax_ecdf.set_ylim(0, 1.05)
    ax_ecdf.set_title("Função Distribuição Empírica (ECDF)")
    ax_ecdf.set_xlabel("Valor")
    ax_ecdf.set_ylabel("Probabilidade acumulada")
    ax_ecdf.grid(alpha=0.3)
    _finalizar_figura_estatistica(fig_ecdf, "ecdf_dados", salvar)


def _analise_tabela_dados():
    """Fluxo principal da nova opção Tabela em Estatística."""

    print("\n" + "-" * 70)
    print("ANÁLISE ESTATÍSTICA DE TABELA / SÉRIE DE DADOS")
    print("-" * 70)

    tipo = input("Os dados são (d)iscretos ou (c)ontínuos? [c]: ").strip().lower()
    discreto = tipo.startswith("d")

    dados = _coletar_dados_tabela()
    if len(dados) < 2:
        print(f"{Cores.FAIL}São necessários ao menos 2 valores numéricos para a análise.{Cores.ENDC}")
        return

    serie = pd.Series(dados, dtype=float)
    print(f"\n{Cores.BOLD}Resumo Estatístico ({'Discreto' if discreto else 'Contínuo'}):{Cores.ENDC}\n")

    metricas = _gerar_resumo_metricas(serie)
    df_metricas = pd.DataFrame(metricas, columns=["Métrica", "Valor"])
    print(df_metricas.to_string(index=False))

    freq_df = _gerar_tabela_frequencias(serie, discreto)
    if not freq_df.empty:
        print(f"\n{Cores.BOLD}Tabela de Frequências:{Cores.ENDC}\n")
        print(freq_df.to_string(index=False))

    skew_val = float(serie.skew()) if serie.nunique() > 1 else float("nan")
    kurt_val = float(serie.kurtosis()) if serie.nunique() > 1 else float("nan")
    print(f"\nAssimetria: {_formatar_valor_metrica(skew_val)} -> {_interpretar_skewness(skew_val)}")
    print(f"Curtose: {_formatar_valor_metrica(kurt_val)} -> {_interpretar_kurtosis(kurt_val)}")

    plotar = input(f"\n{Cores.OKCYAN}Como exibir os gráficos? (v)er / (s)alvar / (a)uto [padrão v]: {Cores.ENDC}").strip().lower()
    if plotar in ("", "v"):
        salvar = False
    elif plotar == "s":
        salvar = True
    else:
        salvar = None

    try:
        _gerar_graficos_tabela(serie, discreto, salvar)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"{Cores.WARNING}Não foi possível gerar os gráficos: {exc}{Cores.ENDC}")


def menu_estatistica():
    """Menu principal de estatística (fase inicial focada em inferência)."""

    while True:
        print("\n" + "=" * 70)
        print("                        ESTATÍSTICA")
        print("=" * 70)
        print("\n  Ferramentas disponíveis:")
        print("    1. Pergunte ao Smither (qual distribuição usar?)")
        print("    2. Distribuições (discretas e contínuas)")
        print("    3. Verificar função fdp")
        print("    4. Análise de tabela/dados amostrais")
        print(f"\n  {Cores.OKBLUE}0{Cores.ENDC}. Voltar ao Menu Anterior\n")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == '0':
            break
        if escolha == '1':
            _pergunte_ao_smither()
            continue
        if escolha == '2':
            _menu_distribuicoes()
            continue
        if escolha == '3':
            _verificar_funcao_pdf()
            continue
        if escolha == '4':
            _analise_tabela_dados()
            continue

        print(f"{Cores.FAIL}[Erro] Opção inválida!{Cores.ENDC}")


def menu():
    """Compatibilidade com o carregador principal do Smither."""
    menu_estatistica()
