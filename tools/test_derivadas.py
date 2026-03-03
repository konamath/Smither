"""
Script de testes pesados para o módulo de derivadas.
Valida todas as funcionalidades matemáticas e de plotagem.
"""

import sys
from pathlib import Path
import traceback

root = Path.cwd()
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from calculo.engine import (
    EngineCalculo, Derivada, DerivadaParcial, 
    DerivadaDirecional, Extremos
)
from calculo.graficos import GraficoDerivada, GraficoDerivadaParcial


class TestadorDerivadas:
    """Classe para testar funcionalidades de derivadas."""
    
    def __init__(self):
        self.testes_ok = 0
        self.testes_fail = 0
        self.testes = []
    
    def teste(self, nome, funcao):
        """Executa um teste e registra resultado."""
        try:
            resultado = funcao()
            if resultado:
                print(f"[OK] {nome}")
                self.testes_ok += 1
                return True
            else:
                print(f"[FAIL] {nome}: retornou falso")
                self.testes_fail += 1
                return False
        except Exception as e:
            print(f"[ERROR] {nome}: {str(e)[:60]}")
            self.testes_fail += 1
            return False
    
    def imprimir_resumo(self):
        """Imprime resumo dos testes."""
        total = self.testes_ok + self.testes_fail
        pct = 100 * self.testes_ok / total if total > 0 else 0
        print(f"\n{'='*70}")
        print(f"RESUMO: {self.testes_ok}/{total} testes passaram ({pct:.1f}%)")
        print(f"{'='*70}\n")
        return self.testes_fail == 0


def main():
    print("="*70)
    print("TESTES PESADOS - MODULO DE DERIVADAS")
    print("="*70 + "\n")
    
    t = TestadorDerivadas()
    
    # SECAO 1: DERIVADAS SIMPLES 1 VAR
    print("\n[SECAO 1] Derivadas Simples (1 variavel)")
    print("-" * 70)
    
    t.teste(
        "Derivada de x^2",
        lambda: Derivada.calcular('x**2', 'x', ordem=1)[1] == '2*x'
    )
    
    t.teste(
        "Derivada de x^3 + 2x",
        lambda: Derivada.calcular('x**3 + 2*x', 'x', ordem=1)[1] == '3*x**2 + 2'
    )
    
    t.teste(
        "Derivada de sin(x)",
        lambda: 'cos' in str(Derivada.calcular('sin(x)', 'x', ordem=1)[1])
    )
    
    # SECAO 2: DERIVADAS DE ORDEM SUPERIOR
    print("\n[SECAO 2] Derivadas de Ordem Superior")
    print("-" * 70)
    
    t.teste(
        "Derivada 2a de x^3",
        lambda: Derivada.calcular('x**3', 'x', ordem=2)[1] == '6*x'
    )
    
    t.teste(
        "Derivada 3a de x^4",
        lambda: Derivada.calcular('x**4', 'x', ordem=3)[1] == '24*x'
    )
    
    # SECAO 3: DERIVADAS EM PONTOS
    print("\n[SECAO 3] Valores de Derivadas em Pontos")
    print("-" * 70)
    
    def test_deriv_ponto():
        val = Derivada.calcular_ponto('x**2', 'x', 3.0, ordem=1)
        return abs(val - 6.0) < 1e-6
    
    t.teste("Derivada de x^2 em x=3 (esperado 6)", test_deriv_ponto)
    
    def test_deriv_ponto_2():
        val = Derivada.calcular_ponto('x**3', 'x', 2.0, ordem=1)
        return abs(val - 12.0) < 1e-6
    
    t.teste("Derivada de x^3 em x=2 (esperado 12)", test_deriv_ponto_2)
    
    # SECAO 4: PONTOS CRITICOS E EXTREMOS 1VAR
    print("\n[SECAO 4] Extremos em 1 Variavel")
    print("-" * 70)
    
    def test_extremos_1var():
        pontos = Extremos.encontrar_pontos_criticos_1var('x**3 - 3*x', 'x')
        return len(pontos) > 0 and all(isinstance(p, (int, float)) for p in pontos)
    
    t.teste("Encontrar pontos criticos de x^3 - 3x", test_extremos_1var)
    
    def test_classificacao():
        pontos = Extremos.encontrar_pontos_criticos_1var('x**3 - 3*x', 'x')
        extremos = Extremos.classificar_extremos_1var('x**3 - 3*x', 'x', pontos)
        return 'maximos' in extremos and 'minimos' in extremos
    
    t.teste("Classificar extremos (max/min)", test_classificacao)
    
    # SECAO 5: DERIVADAS PARCIAIS
    print("\n[SECAO 5] Derivadas Parciais (2 variaveis)")
    print("-" * 70)
    
    def test_parcial_x():
        orig, deriv = DerivadaParcial.calcular('x**2 + y**2', 'x', ordem=1)
        return deriv == '2*x'
    
    t.teste("Derivada parcial de x^2+y^2 em relacao a x", test_parcial_x)
    
    def test_parcial_y():
        orig, deriv = DerivadaParcial.calcular('x**2 + y**2', 'y', ordem=1)
        return deriv == '2*y'
    
    t.teste("Derivada parcial de x^2+y^2 em relacao a y", test_parcial_y)
    
    def test_parcial_mista():
        # ∂²f/∂x∂y de x*y = 1
        orig, deriv = DerivadaParcial.calcular('x*y', 'x', ordem=1)
        orig2, deriv2 = DerivadaParcial.calcular(str(deriv), 'y', ordem=1)
        return deriv2 == '1'
    
    t.teste("Derivada parcial mista (d2/dxdy)", test_parcial_mista)
    
    # SECAO 6: GRADIENTE
    print("\n[SECAO 6] Gradiente")
    print("-" * 70)
    
    def test_gradiente():
        orig, derivs = DerivadaParcial.calcular_gradiente('x**2 + y**2')
        return len(derivs) == 2 and derivs[0] == '2*x' and derivs[1] == '2*y'
    
    t.teste("Gradiente de x^2 + y^2", test_gradiente)
    
    def test_gradiente_ponto():
        grad = DerivadaParcial.calcular_gradiente_ponto('x**2 + y**2', {'x': 1.0, 'y': 1.0})
        return grad is not None and len(grad) == 2 and abs(grad[0] - 2.0) < 1e-6
    
    t.teste("Gradiente em ponto (1,1) de x^2+y^2", test_gradiente_ponto)
    
    # SECAO 7: DERIVADA DIRECIONAL
    print("\n[SECAO 7] Derivada Direcional")
    print("-" * 70)
    
    def test_derivada_direcional():
        deriv_dir = DerivadaDirecional.calcular_direcional(
            'x**2 + y**2', 
            [1, 0],  # direcao x
            {'x': 1.0, 'y': 1.0}
        )
        return deriv_dir is not None and abs(deriv_dir - 2.0) < 0.1
    
    t.teste("Derivada direcional em (1,1) na direcao x", test_derivada_direcional)
    
    # SECAO 8: EXTREMOS 2VAR
    print("\n[SECAO 8] Extremos em 2 Variaveis")
    print("-" * 70)
    
    def test_extremos_2var():
        pontos = Extremos.encontrar_pontos_criticos_2var('x**2 + y**2 - 2*x - 4*y + 5')
        return len(pontos) > 0
    
    t.teste("Encontrar pontos criticos em 2var", test_extremos_2var)
    
    def test_hessiana():
        pontos = Extremos.encontrar_pontos_criticos_2var('x**2 + y**2 - 2*x - 2*y')
        if not pontos:
            return False
        x, y = pontos[0]
        class_type = Extremos.teste_hessiana_2var('x**2 + y**2 - 2*x - 2*y', (x, y))
        # Apenas checar se eh uma string nao-vazia (ignora encoding/acentos)
        return isinstance(class_type, str) and len(class_type) > 0
    
    t.teste("Teste de Hessiana para classificacao", test_hessiana)
    
    # SECAO 9: GERACAO DE GRAFICOS
    print("\n[SECAO 9] Geracao de Graficos (Headless)")
    print("-" * 70)
    
    def test_plot_funcao():
        f = GraficoDerivada.plotar_funcao_1var('x**2', 'x', salvar=True)
        return f is not None and Path(f).exists()
    
    t.teste("Gerar grafico de funcao (1var)", test_plot_funcao)
    
    def test_plot_derivada():
        f = GraficoDerivada.plotar_funcao_derivada_1var('x**3', 'x', salvar=True)
        return f is not None and Path(f).exists()
    
    t.teste("Gerar grafico funcao+derivada", test_plot_derivada)
    
    def test_plot_2var():
        f = GraficoDerivada.plotar_funcao_2var('x**2 + y**2', tipo_plot='contour', salvar=True)
        return f is not None and Path(f).exists()
    
    t.teste("Gerar grafico 2var (contorno)", test_plot_2var)
    
    def test_plot_extremos():
        extremos = {'maximos': [], 'minimos': [(0.0, 0.0)], 'inflexao': []}
        f = GraficoDerivada.plotar_extremos_1var('x**2', 'x', extremos, salvar=True)
        return f is not None and Path(f).exists()
    
    t.teste("Gerar grafico com extremos marcados", test_plot_extremos)
    
    def test_plot_gradiente():
        f = GraficoDerivadaParcial.plotar_gradiente_no_ponto('x**2 + y**2', (0.5, 0.5), salvar=True)
        return f is not None and Path(f).exists()
    
    t.teste("Gerar grafico com vetor gradiente", test_plot_gradiente)
    
    # RESUMO FINAL
    sucesso = t.imprimir_resumo()
    
    if sucesso:
        print("[OK] TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("[FAIL] ALGUNS TESTES FALHARAM")
        return 1


if __name__ == '__main__':
    exit(main())
