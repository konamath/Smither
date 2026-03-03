"""
Utilitários de Plotagem para o Módulo de Cálculo
================================================
Funções para visualizar funções, derivadas e análise de extremos.
"""

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sympy import parse_expr, lambdify
import sympy as sp
from datetime import datetime
from pathlib import Path


class GraficoDerivada:
    """Classe para plotar gráficos de funções e suas derivadas."""
    
    @staticmethod
    def plotar_funcao_1var(expr_str: str, var: str, intervalo: tuple = None, 
                          titulo: str = "Função", salvar: bool | None = None):
        """
        Plota uma função de uma variável.
        A expressão é exibida em LaTeX no título e na legenda (quando possível),
        para que apareça com notação matemática em vez de estilo Python.
        
        Args:
            expr_str: Expressão em string
            var: Variável
            intervalo: Tupla (min, max) do intervalo
            titulo: Título do gráfico
            salvar: Se True, salva a imagem
        """
        try:
            x = sp.symbols(var)
            expr = parse_expr(expr_str)
            expr_latex = sp.latex(expr)
            f = lambdify(x, expr, 'numpy')
            
            if intervalo is None:
                intervalo = (-10, 10)
            
            x_vals = np.linspace(intervalo[0], intervalo[1], 500)
            y_vals = f(x_vals)
            
            plt.figure(figsize=(10, 6))
            plt.plot(x_vals, y_vals, 'b-', linewidth=2,
                     label=f'$f({var}) = {expr_latex}$')
            plt.grid(True, alpha=0.3)
            plt.xlabel(var, fontsize=12)
            plt.ylabel(f'$f({var})$', fontsize=12)
            plt.title(titulo, fontsize=14, fontweight='bold')
            plt.legend(fontsize=10)
            plt.axhline(y=0, color='k', linewidth=0.5)
            plt.axvline(x=0, color='k', linewidth=0.5)
            
            # decide se deve salvar (autodetecta em ambientes headless)
            do_save = _should_save_plots() if salvar is None else bool(salvar)
            if do_save:
                out = _ensure_output_dir()
                fname = out / f'grafico_{_sanitize_filename(titulo)}_{_timestamp()}.png'
                plt.savefig(fname, dpi=150, bbox_inches='tight')
                plt.close()
                return str(fname)

            plt.show()
            
        except Exception as e:
            print(f"❌ Erro ao plotar gráfico: {e}")
    
    @staticmethod
    def plotar_funcao_derivada_1var(expr_str: str, var: str, intervalo: tuple = None,
                                   salvar: bool | None = None):
        """
        Plota uma função e sua derivada de 1ª ordem no mesmo gráfico.
        As fórmulas são convertidas para LaTeX nas legendas e títulos.
        
        Args:
            expr_str: Expressão em string
            var: Variável
            intervalo: Tupla (min, max) do intervalo
            salvar: Se True, salva a imagem
        """
        try:
            x = sp.symbols(var)
            expr = parse_expr(expr_str)
            expr_latex = sp.latex(expr)
            # Calcula derivada
            derivada = sp.diff(expr, x)
            derivada_latex = sp.latex(derivada)
            
            f = lambdify(x, expr, 'numpy')
            f_prime = lambdify(x, derivada, 'numpy')
            
            if intervalo is None:
                intervalo = (-10, 10)
            
            x_vals = np.linspace(intervalo[0], intervalo[1], 500)
            y_vals = f(x_vals)
            y_prime_vals = f_prime(x_vals)
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            
            # Gráfico da função
            ax1.plot(x_vals, y_vals, 'b-', linewidth=2.5)
            ax1.grid(True, alpha=0.3)
            ax1.set_xlabel(var, fontsize=11)
            ax1.set_ylabel(f'$f({var})$', fontsize=11)
            ax1.set_title(f'Função Original\n$f({var}) = {expr_latex}$', fontsize=12, fontweight='bold')
            ax1.axhline(y=0, color='k', linewidth=0.5)
            ax1.axvline(x=0, color='k', linewidth=0.5)
            
            # Gráfico da derivada
            ax2.plot(x_vals, y_prime_vals, 'r-', linewidth=2.5)
            ax2.grid(True, alpha=0.3)
            ax2.set_xlabel(var, fontsize=11)
            ax2.set_ylabel(f"$f'({var})$", fontsize=11)
            ax2.set_title(f"Derivada de 1ª Ordem\n$f'({var}) = {derivada_latex}$", 
                         fontsize=12, fontweight='bold')
            ax2.axhline(y=0, color='k', linewidth=0.5)
            ax2.axvline(x=0, color='k', linewidth=0.5)
            
            plt.tight_layout()
            
            do_save = _should_save_plots() if salvar is None else bool(salvar)
            if do_save:
                out = _ensure_output_dir()
                fname = out / f'grafico_funcao_derivada_{_timestamp()}.png'
                plt.savefig(fname, dpi=150, bbox_inches='tight')
                plt.close()
                return str(fname)

            plt.show()
            
        except Exception as e:
            print(f"❌ Erro ao plotar gráfico: {e}")
    
    @staticmethod
    def plotar_funcao_2var(expr_str: str, intervalo: tuple = None, 
                          tipo_plot: str = 'surface', salvar: bool | None = None):
        """
        Plota uma função de duas variáveis (superfície ou contorno).
        A expressão é mostrada em LaTeX no título do gráfico.
        
        Args:
            expr_str: Expressão em string (use 'x' e 'y' como variáveis)
            intervalo: Tupla (min, max) do intervalo para ambas as variáveis
            tipo_plot: 'surface' para gráfico 3D ou 'contour' para contorno
            salvar: Se True, salva a imagem
        """
        try:
            x, y = sp.symbols('x y')
            expr = parse_expr(expr_str)
            expr_latex = sp.latex(expr)
            f = lambdify((x, y), expr, 'numpy')
            
            if intervalo is None:
                intervalo = (-5, 5)
            
            x_vals = np.linspace(intervalo[0], intervalo[1], 100)
            y_vals = np.linspace(intervalo[0], intervalo[1], 100)
            X, Y = np.meshgrid(x_vals, y_vals)
            Z = f(X, Y)
            
            if tipo_plot == 'surface':
                from mpl_toolkits.mplot3d import Axes3D
                fig = plt.figure(figsize=(12, 8))
                ax = fig.add_subplot(111, projection='3d')
                surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
                ax.set_xlabel('x', fontsize=11)
                ax.set_ylabel('y', fontsize=11)
                ax.set_zlabel('$f(x,y)$', fontsize=11)
                ax.set_title(f'Superfície:\n$f(x,y) = {expr_latex}$', fontsize=12, fontweight='bold')
                fig.colorbar(surf, ax=ax)
            
            elif tipo_plot == 'contour':
                fig, ax = plt.subplots(figsize=(10, 8))
                contour = ax.contourf(X, Y, Z, levels=20, cmap='viridis')
                ax.contour(X, Y, Z, levels=10, colors='black', alpha=0.3, linewidths=0.5)
                ax.set_xlabel('x', fontsize=11)
                ax.set_ylabel('y', fontsize=11)
                ax.set_title(f'Mapa de Contorno:\n$f(x,y) = {expr_latex}$', fontsize=12, fontweight='bold')
                fig.colorbar(contour, ax=ax)
            
            do_save = _should_save_plots() if salvar is None else bool(salvar)
            if do_save:
                out = _ensure_output_dir()
                fname = out / f'grafico_{tipo_plot}_{_timestamp()}.png'
                plt.savefig(fname, dpi=150, bbox_inches='tight')
                plt.close()
                return str(fname)

            plt.show()
            
        except Exception as e:
            print(f"❌ Erro ao plotar gráfico: {e}")
    
    @staticmethod
    def plotar_extremos_1var(expr_str: str, var: str, extremos: dict, 
                            intervalo: tuple = None, salvar: bool | None = None):
        """
        Plota função com pontos de máximo e mínimo marcados.
        A função exibida na legenda utiliza LaTeX para a fórmula.
        
        Args:
            expr_str: Expressão em string
            var: Variável
            extremos: Dicionário com 'maximos' e 'minimos' (lista de tuplas (x, y))
            intervalo: Tupla (min, max) do intervalo
            salvar: Se True, salva a imagem
        """
        try:
            x = sp.symbols(var)
            expr = parse_expr(expr_str)
            expr_latex = sp.latex(expr)
            f = lambdify(x, expr, 'numpy')
            
            if intervalo is None:
                intervalo = (-10, 10)
            
            x_vals = np.linspace(intervalo[0], intervalo[1], 500)
            y_vals = f(x_vals)
            
            plt.figure(figsize=(12, 6))
            plt.plot(x_vals, y_vals, 'b-', linewidth=2.5, label=f'$f({var}) = {expr_latex}$')
            
            # Plotar máximos
            if extremos.get('maximos'):
                for x_max, y_max in extremos['maximos']:
                    plt.plot(x_max, y_max, 'go', markersize=12, label='Máximo' if x_max == extremos['maximos'][0][0] else '')
                    plt.annotate(f'Máx\n({x_max:.2f}, {y_max:.2f})', 
                               xy=(x_max, y_max), xytext=(5, 10),
                               textcoords='offset points', fontsize=9,
                               bbox=dict(boxstyle='round,pad=0.5', fc='lightgreen', alpha=0.7))
            
            # Plotar mínimos
            if extremos.get('minimos'):
                for x_min, y_min in extremos['minimos']:
                    plt.plot(x_min, y_min, 'rs', markersize=12, label='Mínimo' if x_min == extremos['minimos'][0][0] else '')
                    plt.annotate(f'Mín\n({x_min:.2f}, {y_min:.2f})', 
                               xy=(x_min, y_min), xytext=(5, -15),
                               textcoords='offset points', fontsize=9,
                               bbox=dict(boxstyle='round,pad=0.5', fc='lightcoral', alpha=0.7))
            
            plt.grid(True, alpha=0.3)
            plt.xlabel(var, fontsize=12)
            plt.ylabel(f'f({var})', fontsize=12)
            plt.title('Extremos Locais (Máximos e Mínimos)', fontsize=14, fontweight='bold')
            plt.legend(fontsize=10, loc='best')
            plt.axhline(y=0, color='k', linewidth=0.5)
            plt.axvline(x=0, color='k', linewidth=0.5)
            
            do_save = _should_save_plots() if salvar is None else bool(salvar)
            if do_save:
                out = _ensure_output_dir()
                fname = out / f'grafico_extremos_{_timestamp()}.png'
                plt.savefig(fname, dpi=150, bbox_inches='tight')
                plt.close()
                return str(fname)

            plt.show()
            
        except Exception as e:
            print(f"❌ Erro ao plotar gráfico: {e}")
    

class GraficoDerivadaParcial:
    """Classe para visualizar derivadas parciais em funções de 2 variáveis."""
    
    @staticmethod
    def plotar_derivada_parcial(expr_str: str, intervalo: tuple = None, salvar: bool | None = None):
        """
        Plota uma função de 2 variáveis como superfície e suas derivadas parciais.
        """
        try:
            x, y = sp.symbols('x y')
            expr = parse_expr(expr_str)
            expr_latex = sp.latex(expr)
            
            # Calcula derivadas parciais
            df_dx = sp.diff(expr, x)
            df_dy = sp.diff(expr, y)
            df_dx_latex = sp.latex(df_dx)
            df_dy_latex = sp.latex(df_dy)
            
            if intervalo is None:
                intervalo = (-5, 5)
            
            x_vals = np.linspace(intervalo[0], intervalo[1], 80)
            y_vals = np.linspace(intervalo[0], intervalo[1], 80)
            X, Y = np.meshgrid(x_vals, y_vals)
            
            f = lambdify((x, y), expr, 'numpy')
            f_x = lambdify((x, y), df_dx, 'numpy')
            f_y = lambdify((x, y), df_dy, 'numpy')
            
            Z = f(X, Y)
            Z_x = f_x(X, Y)
            Z_y = f_y(X, Y)
            
            from mpl_toolkits.mplot3d import Axes3D
            fig = plt.figure(figsize=(16, 5))
            
            # Superfície original
            ax1 = fig.add_subplot(131, projection='3d')
            surf1 = ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
            ax1.set_xlabel('x')
            ax1.set_ylabel('y')
            ax1.set_zlabel('$f(x,y)$')
            ax1.set_title(f'Função Original\n$f(x,y) = {expr_latex}$', fontweight='bold')
            
            # Derivada parcial em relação a x
            ax2 = fig.add_subplot(132, projection='3d')
            surf2 = ax2.plot_surface(X, Y, Z_x, cmap='coolwarm', alpha=0.8)
            ax2.set_xlabel('x')
            ax2.set_ylabel('y')
            ax2.set_zlabel(r'$\frac{\partial f}{\partial x}$')
            ax2.set_title(rf'Derivada Parcial\n$\displaystyle \frac{{\partial f}}{{\partial x}} = {df_dx_latex}$', fontweight='bold')
            
            # Derivada parcial em relação a y
            ax3 = fig.add_subplot(133, projection='3d')
            surf3 = ax3.plot_surface(X, Y, Z_y, cmap='plasma', alpha=0.8)
            ax3.set_xlabel('x')
            ax3.set_ylabel('y')
            ax3.set_zlabel(r'$\frac{\partial f}{\partial y}$')
            ax3.set_title(rf'Derivada Parcial\n$\displaystyle \frac{{\partial f}}{{\partial y}} = {df_dy_latex}$', fontweight='bold')
            
            plt.tight_layout()
            
            do_save = _should_save_plots() if salvar is None else bool(salvar)
            if do_save:
                out = _ensure_output_dir()
                fname = out / f'grafico_derivadas_parciais_{_timestamp()}.png'
                plt.savefig(fname, dpi=150, bbox_inches='tight')
                plt.close()
                return str(fname)

            plt.show()
            
        except Exception as e:
            print(f"❌ Erro ao plotar gráfico: {e}")

    @staticmethod
    def plotar_gradiente_no_ponto(expr_str: str, ponto: tuple, intervalo: tuple = None, salvar: bool | None = None):
        """
        Plota mapa de contorno da função de duas variáveis e desenha o vetor gradiente
        no ponto especificado.

        Args:
            expr_str: expressão em string (use 'x' e 'y')
            ponto: tupla (x0, y0)
            intervalo: (min, max) para x e y
            salvar: se True salva a figura como 'gradiente_no_ponto.png'
        """
        try:
            x, y = sp.symbols('x y')
            expr = parse_expr(expr_str)
            
            # Gradientes simbólicos e funções numéricas
            df_dx = sp.diff(expr, x)
            df_dy = sp.diff(expr, y)
            f = lambdify((x, y), expr, 'numpy')
            f_dx = lambdify((x, y), df_dx, 'numpy')
            f_dy = lambdify((x, y), df_dy, 'numpy')
            
            if intervalo is None:
                intervalo = (-5, 5)
            
            x_vals = np.linspace(intervalo[0], intervalo[1], 200)
            y_vals = np.linspace(intervalo[0], intervalo[1], 200)
            X, Y = np.meshgrid(x_vals, y_vals)
            Z = f(X, Y)
            
            x0, y0 = ponto
            # calcula componente do gradiente no ponto
            gx = float(f_dx(x0, y0))
            gy = float(f_dy(x0, y0))
            mag = np.hypot(gx, gy)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            contour = ax.contourf(X, Y, Z, levels=30, cmap='viridis')
            ax.contour(X, Y, Z, levels=10, colors='black', alpha=0.3, linewidths=0.4)
            fig.colorbar(contour, ax=ax)
            
            # Normaliza vetor para visualização, mantendo direção
            if mag == 0:
                ux, uy = 0, 0
            else:
                ux, uy = gx / mag, gy / mag
            
            # Escala do vetor para ficar visível no gráfico
            escala = max(intervalo[1] - intervalo[0], 1) * 0.15
            ax.quiver(x0, y0, ux, uy, angles='xy', scale_units='xy', scale=1, color='red', width=0.008)
            ax.plot(x0, y0, 'ro', label=f'Ponto ({x0}, {y0})')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(f'Gradiente em ({x0}, {y0}) | $\nabla f = ({gx:.3g}, {gy:.3g})$, $|\nabla f|={mag:.3g}$')
            ax.legend()
            ax.set_xlim(intervalo[0], intervalo[1])
            ax.set_ylim(intervalo[0], intervalo[1])
            
            do_save = _should_save_plots() if salvar is None else bool(salvar)
            if do_save:
                out = _ensure_output_dir()
                fname = out / f'gradiente_no_ponto_{_timestamp()}.png'
                plt.savefig(fname, dpi=150, bbox_inches='tight')
                plt.close()
                return str(fname)

            plt.show()
        except Exception as e:
            print(f"❌ Erro ao plotar gradiente no ponto: {e}")


def _ensure_output_dir() -> Path:
    out = Path.cwd() / 'outputs'
    out.mkdir(parents=True, exist_ok=True)
    return out


def _timestamp() -> str:
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def _sanitize_filename(s: str) -> str:
    return ''.join(c if c.isalnum() or c in ('-', '_') else '_' for c in s)


def _should_save_plots() -> bool:
    """Decide se os plots devem ser salvos automaticamente.

    Regras simples:
    - Se a backend do matplotlib for 'agg' (sem display) -> True
    - Se variável de ambiente 'HEADLESS' ou 'CI' estiver setada -> True
    - Se não houver DISPLAY no Unix -> True
    Caso contrário, retorna False (mostra com plt.show()).
    """
    try:
        backend = matplotlib.get_backend().lower()
        if 'agg' in backend:
            return True
    except Exception:
        pass

    if os.environ.get('HEADLESS') or os.environ.get('CI'):
        return True

    # No Unix, ausência de DISPLAY normalmente indica headless
    if os.name != 'nt' and not os.environ.get('DISPLAY'):
        return True

    return False


class GraficoIntegral:
    """Classe para plotar integrais definidas com area sombreada."""
    
    @staticmethod
    def plotar_area_integral(expr_str: str, var: str, a: float, b: float, salvar: bool | None = None):
        """
        Plota uma funcao com area de integracao sombreada.
        
        Args:
            expr_str: Expressao em string
            var: Variavel
            a, b: Limites de integracao
            salvar: Se None, usa autodeteccao; se True/False, salva ou mostra
        """
        try:
            x = sp.symbols(var)
            expr = parse_expr(expr_str)
            expr_latex = sp.latex(expr)
            f = lambdify(x, expr, 'numpy')
            
            # Define intervalo maior que [a, b] para melhor visualizacao
            margem = (b - a) * 0.2
            x_min = a - margem
            x_max = b + margem
            
            x_vals = np.linspace(x_min, x_max, 500)
            y_vals = f(x_vals)
            
            # Pontos dentro dos limites para o preenchimento
            x_area = np.linspace(a, b, 300)
            y_area = f(x_area)
            
            plt.figure(figsize=(10, 6))
            
            # Plota a funcao
            expr_latex = sp.latex(expr)
            plt.plot(x_vals, y_vals, 'b-', linewidth=2.5, label=f'$f({var}) = {expr_latex}$')
            
            # Preenche a area
            plt.fill_between(x_area, 0, y_area, alpha=0.3, color='blue', label=f'Area de integracao')
            
            # Marca os limites
            plt.axvline(x=a, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
            plt.axvline(x=b, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
            
            plt.grid(True, alpha=0.3)
            plt.xlabel(var, fontsize=12)
            plt.ylabel(f'f({var})', fontsize=12)
            # format limits: try numeric, otherwise leave as-is
            try:
                a_fmt = f"{float(a):.2f}"
            except Exception:
                a_fmt = str(a)
            try:
                b_fmt = f"{float(b):.2f}"
            except Exception:
                b_fmt = str(b)
            plt.title(f'Integral Definida de {a_fmt} a {b_fmt}', fontsize=14, fontweight='bold')
            plt.legend(fontsize=10)
            plt.axhline(y=0, color='k', linewidth=0.5)
            plt.axvline(x=0, color='k', linewidth=0.5)
            
            do_save = _should_save_plots() if salvar is None else bool(salvar)
            if do_save:
                out = _ensure_output_dir()
                fname = out / f'integral_area_{_timestamp()}.png'
                plt.savefig(fname, dpi=150, bbox_inches='tight')
                plt.close()
                return str(fname)
            
            plt.show()
        except Exception as e:
            print(f"Erro ao plotar area de integracao: {e}")
    
    @staticmethod
    def plotar_integral_dupla_volume(expr_str: str, x_min: float, x_max: float, 
                                     y_min: float, y_max: float, salvar: bool | None = None):
        """
        Plota uma superficie 3D para integral dupla (mostra o volume).
        """
        try:
            x, y = sp.symbols('x y')
            expr = parse_expr(expr_str)
            f = lambdify((x, y), expr, 'numpy')
            
            x_vals = np.linspace(x_min, x_max, 100)
            y_vals = np.linspace(y_min, y_max, 100)
            X, Y = np.meshgrid(x_vals, y_vals)
            Z = f(X, Y)
            
            from mpl_toolkits.mplot3d import Axes3D
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
            
            ax.set_xlabel('x', fontsize=11)
            ax.set_ylabel('y', fontsize=11)
            ax.set_zlabel('$f(x,y)$', fontsize=11)
            expr_latex = sp.latex(expr)
            ax.set_title(f'Volume sob a superficie:\n$f(x,y) = {expr_latex}$', fontsize=12, fontweight='bold')
            fig.colorbar(surf, ax=ax)
            
            do_save = _should_save_plots() if salvar is None else bool(salvar)
            if do_save:
                out = _ensure_output_dir()
                fname = out / f'integral_dupla_volume_{_timestamp()}.png'
                plt.savefig(fname, dpi=150, bbox_inches='tight')
                plt.close()
                return str(fname)
            
            plt.show()
        except Exception as e:
            print(f"Erro ao plotar volume: {e}")
