"""
Smoke tests for microeconomia consumer analysis.
"""

import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("HEADLESS", "1")
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".mplconfig_test"))
Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)

from microeconomia.consumidor import analisar_utilidade, calcular_cesta_otima, classificar_bens
from microeconomia.menu_micro import _plotar_cesta_otima_consumidor


class TestadorMicroeconomia:
    """Executor simples de testes de microeconomia."""

    def __init__(self):
        self.ok = 0
        self.fail = 0

    def teste(self, nome, funcao):
        try:
            if funcao():
                print(f"[OK] {nome}")
                self.ok += 1
            else:
                print(f"[FAIL] {nome}")
                self.fail += 1
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[ERROR] {nome}: {exc}")
            self.fail += 1

    def resumo(self):
        total = self.ok + self.fail
        print(f"\n{'='*70}")
        print(f"RESUMO: {self.ok}/{total} testes passaram")
        print(f"{'='*70}\n")
        return self.fail == 0


def _aprox(a, b, tol=1e-6):
    return abs(a - b) <= tol


def main():
    print("="*70)
    print("TESTES - MICROECONOMIA / TEORIA DO CONSUMIDOR")
    print("="*70)

    t = TestadorMicroeconomia()

    def test_cobb_douglas():
        analise = analisar_utilidade("x**0.5*y**0.5")
        cesta = calcular_cesta_otima(analise, 2, 4, 100)
        return (
            analise.metodo in {"lagrange", "cobb_douglas"}
            and "0.5*m/p_x" in analise.demanda_x_repr
            and _aprox(cesta["x"], 25.0)
            and _aprox(cesta["y"], 12.5)
        )

    t.teste("Cobb-Douglas com demanda fechada", test_cobb_douglas)

    def test_substitutos_perfeitos():
        analise = analisar_utilidade("x + y")
        cesta = calcular_cesta_otima(analise, 2, 4, 20)
        return (
            analise.metodo == "substitutos_perfeitos"
            and cesta["metodo"] == "substitutos_perfeitos"
            and _aprox(cesta["x"], 10.0)
            and _aprox(cesta["y"], 0.0)
        )

    t.teste("Substitutos perfeitos com canto", test_substitutos_perfeitos)

    def test_complementares_perfeitos():
        analise = analisar_utilidade("Min(x, y)")
        cesta = calcular_cesta_otima(analise, 2, 4, 20)
        classe_x = " ".join(classificar_bens(analise)["x"]).lower()
        return (
            analise.metodo == "complementares_perfeitos"
            and _aprox(cesta["x"], 10 / 3)
            and _aprox(cesta["y"], 10 / 3)
            and "complementares" in classe_x
        )

    t.teste("Complementares perfeitos com classificacao cruzada", test_complementares_perfeitos)

    def test_alias_leontief():
        analise = analisar_utilidade("Leontief(2*x, 3*y)")
        cesta = calcular_cesta_otima(analise, 2, 4, 20)
        return (
            analise.metodo == "complementares_perfeitos"
            and _aprox(cesta["x"], 30 / 7)
            and _aprox(cesta["y"], 20 / 7)
        )

    t.teste("Alias Leontief para complementares perfeitos", test_alias_leontief)

    def test_utilidade_parametrica():
        analise = analisar_utilidade("x**a*y**(1-a)")
        a_param = analise.parametros[0]
        cesta = calcular_cesta_otima(analise, 3, 4, 120, {a_param: 0.25})
        return (
            len(analise.parametros) == 1
            and _aprox(cesta["x"], 10.0)
            and _aprox(cesta["y"], 22.5)
        )

    t.teste("Utilidade parametrica com substituicao numerica", test_utilidade_parametrica)

    def test_aliases_maiusculos_e_prefixo_u():
        casos = [
            ("X**2*Y**3", "cobb_douglas"),
            ("X + Y", "substitutos_perfeitos"),
            ("Min(X, Y)", "complementares_perfeitos"),
            ("LEONTIEF(X, Y)", "complementares_perfeitos"),
            ("LOG(X) + LOG(Y)", "lagrange"),
            ("X + LOG(Y)", "lagrange"),
            ("U(X, Y) = X**0.5*Y**0.5", "cobb_douglas"),
        ]
        for expr, metodo_esperado in casos:
            analise = analisar_utilidade(expr)
            if analise.metodo != metodo_esperado or analise.parametros:
                return False
        return True

    t.teste("Parser aceita maiusculas e formato U(X,Y)=", test_aliases_maiusculos_e_prefixo_u)

    def test_canto_valida_borda():
        analise = analisar_utilidade("x**2 + y**2")
        cesta = calcular_cesta_otima(analise, 1, 1, 10)
        return (
            cesta["tipo_solucao"] == "canto"
            and (
                (_aprox(cesta["x"], 10.0) and _aprox(cesta["y"], 0.0))
                or (_aprox(cesta["x"], 0.0) and _aprox(cesta["y"], 10.0))
            )
        )

    t.teste("Validacao de canto quando tangencia nao e otima", test_canto_valida_borda)

    def test_grafico_cesta_otima():
        analise = analisar_utilidade("x**0.5*y**0.5")
        cesta = calcular_cesta_otima(analise, 2, 4, 100)
        saida = PROJECT_ROOT / "outputs"
        instante = time.time() - 1.0
        _plotar_cesta_otima_consumidor(analise, cesta, 2, 4, 100, {})
        if not saida.exists():
            return False
        arquivos = list(saida.glob("cesta_otima_consumidor_*.png"))
        return any(arquivo.stat().st_mtime >= instante for arquivo in arquivos)

    t.teste("Grafico da cesta otima em modo headless", test_grafico_cesta_otima)

    sucesso = t.resumo()
    raise SystemExit(0 if sucesso else 1)


if __name__ == "__main__":
    main()
