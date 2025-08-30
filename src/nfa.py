from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
import json

EPS = None  # transiciones epsilon representadas por None

@dataclass
class NFA:
    start: int
    accept: int
    states: Set[int]
    transitions: Dict[int, List[Tuple[Optional[str], int]]] = field(default_factory=dict)

    def add_transition(self, src: int, symbol: Optional[str], dst: int):
        self.transitions.setdefault(src, []).append((symbol, dst))
        self.states.add(src)
        self.states.add(dst)

    def to_dict(self):
        symbols = sorted({s for src in self.transitions for s, _ in self.transitions[src] if s is not None})
        transitions = []
        for src, lst in self.transitions.items():
            for s, dst in lst:
                transitions.append((src, s if s is not None else 'ε', dst))
        return {
            'ESTADOS': sorted(list(self.states)),
            'SIMBOLOS': symbols,
            'INICIO': [self.start],
            'ACEPTACION': [self.accept],
            'TRANSICIONES': transitions,
        }


# Construcción de Thompson
from src.regex_parser import to_postfix


def build_from_regex(regex: str, epsilon_symbol='ε') -> NFA:
    """Construye un AFN (NFA) a partir de una expresión regular usando Thompson.

    `epsilon_symbol` es el carácter usado en la regex para representar ε (por defecto 'ε').
    """
    postfix = to_postfix(regex, epsilon_symbol)
    stack: List[NFA] = []
    state_id = 0

    def new_state():
        nonlocal state_id
        sid = state_id
        state_id += 1
        return sid

    for c in postfix:
        if c == '*':
            nfa1 = stack.pop()
            s = new_state(); f = new_state()
            n = NFA(s, f, set())
            n.add_transition(s, None, nfa1.start)
            n.add_transition(s, None, f)
            n.add_transition(nfa1.accept, None, nfa1.start)
            n.add_transition(nfa1.accept, None, f)
            # copiar transiciones del sub-AFN
            for src, lst in nfa1.transitions.items():
                for sym, dst in lst:
                    n.add_transition(src, sym, dst)
            stack.append(n)
        elif c == '.':
            n2 = stack.pop(); n1 = stack.pop()
            # conectar n1.accept -> ε -> n2.start
            for src, lst in n1.transitions.items():
                for sym, dst in lst:
                    pass
            n = NFA(n1.start, n2.accept, set())
            # copiar transiciones de ambos AFNs
            for src, lst in n1.transitions.items():
                for sym, dst in lst:
                    n.add_transition(src, sym, dst)
            for src, lst in n2.transitions.items():
                for sym, dst in lst:
                    n.add_transition(src, sym, dst)
            n.add_transition(n1.accept, None, n2.start)
            stack.append(n)
        elif c == '|' or c == '+':
            n2 = stack.pop(); n1 = stack.pop()
            s = new_state(); f = new_state()
            n = NFA(s, f, set())
            n.add_transition(s, None, n1.start)
            n.add_transition(s, None, n2.start)
            n.add_transition(n1.accept, None, f)
            n.add_transition(n2.accept, None, f)
            # copy transitions
            for src, lst in n1.transitions.items():
                for sym, dst in lst:
                    n.add_transition(src, sym, dst)
            for src, lst in n2.transitions.items():
                for sym, dst in lst:
                    n.add_transition(src, sym, dst)
            stack.append(n)
        else:
            # símbolo
            s = new_state(); f = new_state()
            n = NFA(s, f, set())
            sym = None if c == 'ε' else c
            n.add_transition(s, sym, f)
            stack.append(n)

    if len(stack) != 1:
        raise ValueError('Invalid regex/postfix; stack != 1')
    return stack[0]


def save_nfa(nfa: NFA, path: str):
    with open(path, 'w') as f:
        json.dump(nfa.to_dict(), f, indent=2)
