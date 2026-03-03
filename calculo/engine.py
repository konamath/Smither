"""
Engine Central de Cálculo - Smither
====================================
Motor base com funções e utilitários para operações de cálculo.
Utiliza SymPy para cálculo simbólico.
"""

import sympy as sp
from sympy import symbols, diff, integrate, limit, oo
from typing import Union, Tuple, Optional


class EngineCalculo:
    """Motor centralizado para operações de cálculo."""
    
    @staticmethod
    def criar_simbolos(nomes: Union[str, list]) -> Union[sp.Symbol, Tuple[sp.Symbol]]:
        """
        Cria símbolos SymPy a partir de nomes.
        
        Args:
            nomes: string com um símbolo ou lista de símbolos
        
        Returns:
            Symbol ou tupla de Symbols
        
        Exemplo:
            >>> x = EngineCalculo.criar_simbolos('x')
            >>> x, y = EngineCalculo.criar_simbolos(['x', 'y'])
        """
        if isinstance(nomes, str):
            return symbols(nomes)
        else:
            return symbols(nomes)

    @staticmethod
    def _parse(expr_str: str):
        """Parse expression using SymPy with implicit multiplication enabled.

        Accepts inputs like '3x' or '2xy' by interpreting them as '3*x' and '2*x*y'.
        """
        import re
        from sympy.parsing.sympy_parser import (
            parse_expr as _parse_expr,
            standard_transformations,
            implicit_multiplication_application,
        )

        # Preprocess common function names without parentheses, e.g. 'sinx' -> 'sin(x)'
        func_names = [
            'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
            'exp', 'log', 'sqrt'
        ]
        def _insert_parens(match):
            fn = match.group(1)
            arg = match.group(2)
            return f"{fn}({arg})"

        for fn in func_names:
            # Match fn followed by identifier/digits or a parenthesis-less expression
            pattern = rf"\b({fn})(?!\s*\()([A-Za-z0-9_]+)"
            expr_str = re.sub(pattern, _insert_parens, expr_str)

        transformations = standard_transformations + (implicit_multiplication_application,)
        local_dict = {
            'e': sp.E,
            'E': sp.E,
            'pi': sp.pi,
            'Pi': sp.pi,
        }
        return _parse_expr(expr_str, transformations=transformations, local_dict=local_dict)
    
    @staticmethod
    def validar_expressao(expr_str: str) -> Tuple[bool, Optional[str]]:
        """
        Valida se uma string é uma expressão matemática válida.
        
        Returns:
            (bool válida, mensagem de erro se houver)
        """
        try:
            EngineCalculo._parse(expr_str)
            return True, None
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def formatar_resultado(resultado) -> str:
        """Formata resultado SymPy para exibição legível."""
        return str(resultado)


class Derivada:
    """Classe para operações com derivadas."""
    
    @staticmethod
    def calcular(expressao_str: str, variavel: str, ordem: int = 1) -> Optional[Tuple[str, str]]:
        """
        Calcula derivada de uma expressão.
        
        Args:
            expressao_str: Expressão em string (ex: "x**2 + 3*x")
            variavel: Variável em relação à qual derivar (ex: "x")
            ordem: Ordem da derivada (1ª, 2ª, etc)
        
        Returns:
            (expressão original, derivada) ou None se erro
        """
        try:
            x = sp.symbols(variavel)
            expr = EngineCalculo._parse(expressao_str)
            derivada = diff(expr, x, ordem)
            return (str(expr), str(derivada))
        except Exception:
            return None
    
    @staticmethod
    def calcular_ponto(expressao_str: str, variavel: str, ponto: float, ordem: int = 1) -> Optional[float]:
        """
        Calcula valor da derivada em um ponto específico.
        
        Returns:
            Valor numérico da derivada no ponto
        """
        try:
            x = sp.symbols(variavel)
            expr = EngineCalculo._parse(expressao_str)
            derivada = diff(expr, x, ordem)
            resultado = derivada.subs(x, ponto)
            return float(resultado)
        except Exception:
            return None

    @staticmethod
    def calcular_reta_tangente(expressao_str: str, variavel: str,
                               ponto: Union[float, str]) -> Optional[dict]:
        """
        Calcula a reta tangente de f(x) em x = a.

        Returns:
            dict com a funcao, ponto, valor, coeficiente angular e equacao
        """
        try:
            x = sp.symbols(variavel)
            expr = EngineCalculo._parse(expressao_str)
            ponto_expr = EngineCalculo._parse(str(ponto))
            derivada = diff(expr, x)

            y0 = sp.simplify(expr.subs(x, ponto_expr))
            m = sp.simplify(derivada.subs(x, ponto_expr))
            reta = sp.expand(m * (x - ponto_expr) + y0)

            return {
                'funcao': str(expr),
                'ponto': str(ponto_expr),
                'valor_ponto': str(y0),
                'coef_angular': str(m),
                'equacao': str(reta),
            }
        except Exception:
            return None


class Integral:
    """Classe para operações com integrais."""
    
    @staticmethod
    def calcular_indefinida(expressao_str: str, variavel: str) -> Optional[Tuple[str, str]]:
        """
                return pontos if pontos else []
        
                return []
            (expressão original, integral indefinida)
        """
        try:
            x = sp.symbols(variavel)
            expr = EngineCalculo._parse(expressao_str)
            integral = integrate(expr, x)
            return (str(expr), str(integral))
        except Exception:
            return None
    
    @staticmethod
    def calcular_definida(expressao_str: str, variavel: str, limite_inf: float, 
                         limite_sup: float) -> Optional[float]:
        """
        Calcula integral definida entre dois limites.
        
        Returns:
            Valor numérico da integral
        """
        try:
            x = sp.symbols(variavel)
            expr = EngineCalculo._parse(expressao_str)
            resultado = integrate(expr, (x, limite_inf, limite_sup))
            return float(resultado)
        except Exception:
            return None


class Limite:
    """Classe para operações com limites."""
    
    @staticmethod
    def calcular(expressao_str: str, variavel: str, ponto: Union[float, str]) -> Optional[Tuple[str, str]]:
        """
        Calcula o limite de uma expressão.
        
        Args:
            expressao_str: Expressão em string
            variavel: Variável
            ponto: Ponto onde calcular limite (número ou 'oo' para infinito)
        
        Returns:
            (expressão original, limite)
        """
        try:
            x = sp.symbols(variavel)
            expr = EngineCalculo._parse(expressao_str)
            
            # Converte 'oo' para infinito SymPy
            ponto_calcular = oo if ponto == 'oo' or ponto == 'inf' else float(ponto)
            
            resultado = limit(expr, x, ponto_calcular)
            return (str(expr), str(resultado))
        except Exception:
            return None


class DerivadaParcial:
    """Classe para operações com derivadas parciais."""
    
    @staticmethod
    def calcular(expressao_str: str, variavel: str, ordem: int = 1) -> Optional[Tuple[str, str]]:
        """
        Calcula derivada parcial em relação a uma variável.
        
        Args:
            expressao_str: Expressão em string (ex: "x**2 + 3*x*y + y**2")
            variavel: Variável em relação à qual derivar (ex: "x")
            ordem: Ordem da derivada
        
        Returns:
            (expressão original, derivada parcial)
        """
        try:
            var = sp.symbols(variavel)
            expr = EngineCalculo._parse(expressao_str)
            derivada_parcial = diff(expr, var, ordem)
            return (str(expr), str(derivada_parcial))
        except Exception:
            return None
    
    @staticmethod
    def calcular_ponto(expressao_str: str, variavel: str, valores: dict, 
                      ordem: int = 1) -> Optional[float]:
        """
        Calcula valor da derivada parcial em um ponto específico.
        
        Args:
            expressao_str: Expressão em string
            variavel: Variável em relação à qual derivar
            valores: Dicionário com {"x": 1.0, "y": 2.0, ...}
            ordem: Ordem da derivada
        
        Returns:
            Valor numérico da derivada parcial no ponto
        """
        try:
            var = sp.symbols(variavel)
            expr = EngineCalculo._parse(expressao_str)
            derivada_parcial = diff(expr, var, ordem)
            
            # Substitui os valores
            subs_dict = {sp.symbols(k): float(v) for k, v in valores.items()}
            resultado = derivada_parcial.subs(subs_dict)
            return float(resultado)
        except Exception:
            return None
    
    @staticmethod
    def calcular_gradiente(expressao_str: str) -> Optional[Tuple[str, list]]:
        """
        Calcula o gradiente (∇f) de uma função.
        
        Returns:
            (expressão original, [∂f/∂x, ∂f/∂y, ...])
        """
        try:
            x, y = sp.symbols('x y')
            expr = EngineCalculo._parse(expressao_str)
            
            df_dx = diff(expr, x)
            df_dy = diff(expr, y)
            
            return (str(expr), [str(df_dx), str(df_dy)])
        except Exception:
            return None
    
    @staticmethod
    def calcular_gradiente_ponto(expressao_str: str, valores: dict) -> Optional[Tuple[float, float]]:
        """Calcula o gradiente em um ponto específico (x, y)."""
        try:
            x, y = sp.symbols('x y')
            expr = EngineCalculo._parse(expressao_str)
            
            df_dx = diff(expr, x)
            df_dy = diff(expr, y)
            
            subs_dict = {x: valores['x'], y: valores['y']}
            
            df_dx_val = float(df_dx.subs(subs_dict))
            df_dy_val = float(df_dy.subs(subs_dict))
            
            return (df_dx_val, df_dy_val)
        except Exception:
            return None

    @staticmethod
    def calcular_plano_tangente(expressao_str: str, valores: dict) -> Optional[dict]:
        """
        Calcula o plano tangente de z = f(x, y) em um ponto (a, b).

        Returns:
            dict com o ponto, derivadas parciais no ponto e equacao do plano
        """
        try:
            x, y = sp.symbols('x y')
            expr = EngineCalculo._parse(expressao_str)

            a = EngineCalculo._parse(str(valores['x']))
            b = EngineCalculo._parse(str(valores['y']))

            df_dx = diff(expr, x)
            df_dy = diff(expr, y)

            subs_dict = {x: a, y: b}
            f0 = sp.simplify(expr.subs(subs_dict))
            fx0 = sp.simplify(df_dx.subs(subs_dict))
            fy0 = sp.simplify(df_dy.subs(subs_dict))
            plano = sp.expand(f0 + fx0 * (x - a) + fy0 * (y - b))

            return {
                'funcao': str(expr),
                'ponto_x': str(a),
                'ponto_y': str(b),
                'valor_ponto': str(f0),
                'df_dx_ponto': str(fx0),
                'df_dy_ponto': str(fy0),
                'equacao': str(plano),
            }
        except Exception:
            return None


class DerivadaDirecional:
    """Classe para operações com derivadas direcionais."""
    
    @staticmethod
    def calcular_direcional(expressao_str: str, direcao: list, valores: dict) -> Optional[float]:
        """
        Calcula derivada direcional: D_u(f) = ∇f · û
        
        Args:
            expressao_str: Expressão em string
            direcao: Vetor direção [dx, dy]
            valores: Ponto de avaliação {"x": 1.0, "y": 2.0}
        
        Returns:
            Valor da derivada direcional
        """
        try:
            import numpy as np
            
            x, y = sp.symbols('x y')
            expr = EngineCalculo._parse(expressao_str)
            
            # Calcula gradiente
            df_dx = diff(expr, x)
            df_dy = diff(expr, y)
            
            subs_dict = {sp.symbols(k): v for k, v in valores.items()}
            
            df_dx_val = float(df_dx.subs(subs_dict))
            df_dy_val = float(df_dy.subs(subs_dict))
            
            # Normaliza o vetor direção
            direcao_array = np.array(direcao, dtype=float)
            norma = np.linalg.norm(direcao_array)
            if norma == 0:
                return None
            
            u = direcao_array / norma
            gradiente = np.array([df_dx_val, df_dy_val])
            
            # Derivada direcional = gradiente · vetor unitário
            derivada_direcional = np.dot(gradiente, u)
            
            return float(derivada_direcional)
        except Exception:
            return None


class Extremos:
    """Classe para análise de extremos (máximos e mínimos)."""

    @staticmethod
    def encontrar_pontos_criticos_1var(expressao_str: str, variavel: str) -> list:
        """
        Encontra pontos críticos (onde f'(x) = 0).

        Returns:
            Lista de valores de x onde a derivada é zero (pode ser vazia)
        """
        try:
            x = sp.symbols(variavel)
            expr = EngineCalculo._parse(expressao_str)
            derivada = diff(expr, x)

            pontos = sp.solve(derivada, x)
            return [float(p) for p in pontos if getattr(p, 'is_real', False)]
        except Exception:
            return []

    @staticmethod
    def classificar_extremos_1var(expressao_str: str, variavel: str,
                                 pontos_criticos: Optional[list]) -> dict:
        """
        Classifica pontos críticos como máximo, mínimo ou ponto de inflexão.

        Usa teste da segunda derivada: se f''(x) > 0 é mínimo, se f''(x) < 0 é máximo.

        Returns:
            dict com chaves 'maximos','minimos','inflexao' e listas de tuplas (x,y)
        """
        try:
            x = sp.symbols(variavel)
            expr = EngineCalculo._parse(expressao_str)

            primeira_derivada = diff(expr, x)
            segunda_derivada = diff(primeira_derivada, x)

            resultado = {'maximos': [], 'minimos': [], 'inflexao': []}

            if not pontos_criticos:
                return resultado

            for ponto in pontos_criticos:
                try:
                    y_valor = float(expr.subs(x, ponto))
                    f_segunda_val = float(segunda_derivada.subs(x, ponto))

                    if f_segunda_val > 0.001:
                        resultado['minimos'].append((ponto, y_valor))
                    elif f_segunda_val < -0.001:
                        resultado['maximos'].append((ponto, y_valor))
                    else:
                        resultado['inflexao'].append((ponto, y_valor))
                except Exception:
                    continue

            return resultado
        except Exception:
            return {'maximos': [], 'minimos': [], 'inflexao': []}

    @staticmethod
    def encontrar_pontos_criticos_2var(expressao_str: str) -> list:
        """
        Encontra pontos críticos de uma função de 2 variáveis.
        Resolve: ∂f/∂x = 0 e ∂f/∂y = 0

        Returns:
            Lista de tuplas [(x, y), ...] (pode ser vazia)
        """
        try:
            x, y = sp.symbols('x y')
            expr = EngineCalculo._parse(expressao_str)

            df_dx = diff(expr, x)
            df_dy = diff(expr, y)

            solucoes = sp.solve([df_dx, df_dy], [x, y])

            pontos = []
            if isinstance(solucoes, list):
                for sol in solucoes:
                    try:
                        if isinstance(sol, tuple):
                            x_val, y_val = sol
                            if getattr(x_val, 'is_real', False) and getattr(y_val, 'is_real', False):
                                pontos.append((float(x_val), float(y_val)))
                        elif isinstance(sol, dict):
                            x_val = sol.get(x)
                            y_val = sol.get(y)
                            if x_val is not None and y_val is not None and getattr(x_val, 'is_real', False) and getattr(y_val, 'is_real', False):
                                pontos.append((float(x_val), float(y_val)))
                    except Exception:
                        continue
            elif isinstance(solucoes, dict):
                x_val = solucoes.get(x)
                y_val = solucoes.get(y)
                if x_val is not None and y_val is not None and getattr(x_val, 'is_real', False) and getattr(y_val, 'is_real', False):
                    pontos.append((float(x_val), float(y_val)))

            return pontos
        except Exception:
            return []

    @staticmethod
    def teste_hessiana_2var(expressao_str: str, ponto: tuple) -> Optional[str]:
        """
        Classifica ponto crítico usando matriz Hessiana.

        Returns:
            'máximo', 'mínimo', 'sela' ou 'indeterminado'
        """
        try:
            import numpy as np
            x, y = sp.symbols('x y')
            expr = EngineCalculo._parse(expressao_str)

            # Calcula segunda derivadas
            f_xx = diff(diff(expr, x), x)
            f_yy = diff(diff(expr, y), y)
            f_xy = diff(diff(expr, x), y)

            # Avalia no ponto
            subs_dict = {x: ponto[0], y: ponto[1]}

            f_xx_val = float(f_xx.subs(subs_dict))
            f_yy_val = float(f_yy.subs(subs_dict))
            f_xy_val = float(f_xy.subs(subs_dict))

            # Matriz Hessiana
            H = np.array([[f_xx_val, f_xy_val],
                         [f_xy_val, f_yy_val]])

            det_H = np.linalg.det(H)

            if det_H > 0:
                if f_xx_val > 0:
                    return "mínimo"
                elif f_xx_val < 0:
                    return "máximo"
                else:
                    return "indeterminado"
            elif det_H < 0:
                return "sela"
            else:
                return "indeterminado"
        except Exception:
            return None


class Integral:
    """Classe para calcular integrais indefinidas."""
    
    @staticmethod
    def calcular(expr_str: str, var: str) -> Optional[Tuple[str, str]]:
        """
        Calcula integral indefinida.
        
        Args:
            expr_str: expressão em string
            var: variável de integração
        
        Returns:
            (expressão original, integral indefinida)
        """
        try:
            x = sp.symbols(var)
            expr = EngineCalculo._parse(expr_str)
            resultado = integrate(expr, x)
            return (expr_str, str(resultado))
        except Exception:
            return None


class IntegralDefinida:
    """Classe para calcular integrais definidas."""
    
    @staticmethod
    def calcular(expr_str: str, var: str, a: float, b: float) -> Optional[Tuple[str, float]]:
        """
        Calcula integral definida entre a e b.
        
        Args:
            expr_str: expressão em string
            var: variável de integração
            a, b: limites (a < b)
        
        Returns:
            (expressão original, valor numérico)
        """
        try:
            x = sp.symbols(var)
            expr = EngineCalculo._parse(expr_str)
            resultado = integrate(expr, (x, a, b))
            # Tenta converter para float
            return (expr_str, float(resultado))
        except Exception:
            return None
    
    @staticmethod
    def calcular_simbolico(expr_str: str, var: str, a_str: str, b_str: str) -> Optional[Tuple[str, str]]:
        """
        Calcula integral definida com limites simbólicos.
        """
        try:
            x = sp.symbols(var)
            a = EngineCalculo._parse(a_str) if a_str else None
            b = EngineCalculo._parse(b_str) if b_str else None
            expr = EngineCalculo._parse(expr_str)
            resultado = integrate(expr, (x, a, b))
            return (expr_str, str(resultado))
        except Exception:
            return None


class IntegralDupla:
    """Classe para calcular integrais duplas.

    Agora suportamos tanto formas definidas (com limites numéricos) quanto
    indefinidas (sem limites)."""
    
    @staticmethod
    def calcular(expr_str: str, var1: str, a1: float, b1: float,
                 var2: str, a2: float, b2: float) -> Optional[Tuple[str, float]]:
        """
        Calcula integral dupla definida ∫∫ f(x,y) dx dy
        
        Args:
            expr_str: expressão em x,y
            var1: primeira variável (integra-se primeiro)
            a1, b1: limites de var1
            var2: segunda variável
            a2, b2: limites de var2
        
        Returns:
            (expressão original, valor numérico)
        """
        try:
            var1_sym = sp.symbols(var1)
            var2_sym = sp.symbols(var2)
            expr = EngineCalculo._parse(expr_str)
            # Ordem: integra-se primeiro em var1, depois var2
            resultado = integrate(expr, (var1_sym, a1, b1), (var2_sym, a2, b2))
            return (expr_str, float(resultado))
        except Exception:
            return None

    @staticmethod
    def calcular_ordenada(expr_str: str, ordem: str,
                          limite_inf_interno: str, limite_sup_interno: str,
                          limite_inf_externo: str, limite_sup_externo: str) -> Optional[Tuple[str, str]]:
        """
        Calcula integral dupla definida com ordem explicita de integracao.

        Para ``dxdy``, os limites de ``x`` podem depender de ``y``.
        Para ``dydx``, os limites de ``y`` podem depender de ``x``.
        Os limites externos devem ser constantes.
        """
        try:
            ordem_norm = ordem.replace(' ', '').lower()
            if ordem_norm not in ('dxdy', 'dydx'):
                return None

            x, y = sp.symbols('x y')
            expr = EngineCalculo._parse(expr_str)

            if ordem_norm == 'dxdy':
                var_interno = x
                var_externo = y
            else:
                var_interno = y
                var_externo = x

            a_interno = EngineCalculo._parse(limite_inf_interno)
            b_interno = EngineCalculo._parse(limite_sup_interno)
            a_externo = EngineCalculo._parse(limite_inf_externo)
            b_externo = EngineCalculo._parse(limite_sup_externo)

            if a_externo.free_symbols or b_externo.free_symbols:
                return None

            simbolos_internos = a_interno.free_symbols | b_interno.free_symbols
            if simbolos_internos - {var_externo}:
                return None

            resultado = integrate(
                expr,
                (var_interno, a_interno, b_interno),
                (var_externo, a_externo, b_externo),
            )
            return (str(expr), str(sp.simplify(resultado)))
        except Exception:
            return None
    
    @staticmethod
    def calcular_indefinida(expr_str: str, var1: str, var2: str) -> Optional[Tuple[str, str]]:
        """
        Calcula a integral dupla indefinida de uma função em duas variáveis.

        A integral é feita primeiro em ``var1`` e depois em ``var2``
        sem limites, retornando uma expressão simbólica.

        Args:
            expr_str: expressão em x,y
            var1: primeira variável (integra-se primeiro)
            var2: segunda variável

        Returns:
            (expressão original, resultado simbólico em string)
        """
        try:
            v1 = sp.symbols(var1)
            v2 = sp.symbols(var2)
            expr = EngineCalculo._parse(expr_str)
            # integrar sucessivamente
            resultado = integrate(integrate(expr, v1), v2)
            return (expr_str, str(resultado))
        except Exception:
            return None
    
    @staticmethod
    def calcular_com_simbolos(expr_str: str, var1: str, a1: float, b1: float,
                              var2: str, a2_str: str, b2_str: str) -> Optional[Tuple[str, float]]:
        """
        Calcula integral dupla com segundo limite simbólico (ex: y de 0 a x).
        """
        try:
            resultado = IntegralDupla.calcular_ordenada(
                expr_str,
                f'd{var1}d{var2}',
                str(a1),
                str(b1),
                a2_str,
                b2_str,
            )
            if not resultado:
                return None

            orig, valor = resultado
            return (orig, float(sp.N(EngineCalculo._parse(valor))))
        except Exception:
            return None


# Triple integrals have been removed per user request.
