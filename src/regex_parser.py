from typing import List

# Precedencias: Kleene (*), concatenación (.), unión (| o +)
PREC = {'*': 3, '.': 2, '+': 1, '|': 1}


def is_symbol(c: str, epsilon_symbol='ε') -> bool:
    """Devuelve True si el carácter es un símbolo del alfabeto (no operador)."""
    return c not in {'|', '+', '*', '(', ')'}


def insert_concat(regex: str, epsilon_symbol='ε') -> str:
    """Inserta el operador explícito de concatenación '.' donde sea necesario.

    Reglas: insertar concatenación entre A y B cuando
      - A es: símbolo, '*', o ')'
      - B es: símbolo, '(', o epsilon
    """
    out = []
    for i, c in enumerate(regex):
        out.append(c)
        if i + 1 >= len(regex):
            continue
        d = regex[i + 1]
        if (is_symbol(c, epsilon_symbol) or c == '*' or c == ')') and (
            is_symbol(d, epsilon_symbol) or d == '(' or d == epsilon_symbol
        ):
            out.append('.')
    return ''.join(out)


def to_postfix(regex: str, epsilon_symbol='ε') -> str:
    """Algoritmo Shunting-yard: convierte una regex (infix con concat implícita) a postfix."""
    regex = insert_concat(regex, epsilon_symbol)
    output: List[str] = []
    stack: List[str] = []
    for token in regex:
        if token.isspace():
            continue
        if token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError('Paréntesis desbalanceados')
            stack.pop()
        elif token in PREC:
            # '*' es un operador unario posfijo; manejar precedencia
            while stack and stack[-1] != '(' and PREC.get(stack[-1], 0) >= PREC[token]:
                output.append(stack.pop())
            stack.append(token)
        else:
            output.append(token)
    while stack:
        if stack[-1] in '()':
            raise ValueError('Paréntesis desbalanceados')
        output.append(stack.pop())
    return ''.join(output)
