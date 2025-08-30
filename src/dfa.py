from dataclasses import dataclass, field
from typing import Dict, Set, Tuple, Optional, List
from collections import deque
import json
from src.nfa import NFA, EPS

@dataclass
class DFA:
    start: int
    accepts: Set[int]
    states: Set[int]
    transitions: Dict[int, Dict[str, int]]
    symbols: Set[str]

    def to_dict(self):
        transitions = []
        for s, d in self.transitions.items():
            for sym, dst in d.items():
                transitions.append((s, sym, dst))
        return {
            'ESTADOS': sorted(list(self.states)),
            'SIMBOLOS': sorted(list(self.symbols)),
            'INICIO': [self.start],
            'ACEPTACION': sorted(list(self.accepts)),
            'TRANSICIONES': transitions,
        }


def epsilon_closure(states: Set[int], nfa: NFA) -> Set[int]:
    stack = list(states)
    closure = set(states)
    while stack:
        s = stack.pop()
        for t in nfa.transitions.get(s, []):
            sym, dst = t
            if sym is None and dst not in closure:
                closure.add(dst); stack.append(dst)
    return closure


def move(states: Set[int], symbol: str, nfa: NFA) -> Set[int]:
    res = set()
    for s in states:
        for sym, dst in nfa.transitions.get(s, []):
            if sym == symbol:
                res.add(dst)
    return res


def nfa_to_dfa(nfa: NFA) -> DFA:
    symbols = {s for src in nfa.transitions for s, _ in nfa.transitions[src] if s is not None}
    start_closure = frozenset(epsilon_closure({nfa.start}, nfa))
    states_map = {start_closure: 0}
    queue = deque([start_closure])
    transitions = {}
    accepts = set()
    state_id = 0
    while queue:
        current = queue.popleft()
        cid = states_map[current]
        transitions[cid] = {}
        if nfa.accept in current:
            accepts.add(cid)
        for sym in symbols:
            tgt = epsilon_closure(move(current, sym, nfa), nfa)
            if not tgt:
                continue
            tgt_f = frozenset(tgt)
            if tgt_f not in states_map:
                state_id += 1
                states_map[tgt_f] = state_id
                queue.append(tgt_f)
            transitions[cid][sym] = states_map[tgt_f]
    return DFA(start=0, accepts=accepts, states=set(transitions.keys()), transitions=transitions, symbols=symbols)


def simulate(dfa: DFA, w: str) -> bool:
    cur = dfa.start
    for ch in w:
        if ch not in dfa.symbols:
            return False
        cur = dfa.transitions.get(cur, {}).get(ch)
        if cur is None:
            return False
    return cur in dfa.accepts


def simulate_with_trace(dfa: DFA, w: str):
    """Simula el AFD y devuelve (aceptado: bool, traza: List[Tuple[estado_previo, símbolo, estado_siguiente]])

    La traza incluye el estado inicial como ('start', estado_inicial) y luego tuplas
    (estado_previo, símbolo, estado_siguiente) para cada símbolo de la cadena.
    """
    trace = []
    cur = dfa.start
    trace.append(('start', cur))
    for ch in w:
        if ch not in dfa.symbols:
            trace.append((cur, ch, None))
            return False, trace
        nxt = dfa.transitions.get(cur, {}).get(ch)
        trace.append((cur, ch, nxt))
        if nxt is None:
            return False, trace
        cur = nxt
    return (cur in dfa.accepts), trace


def save_dfa(dfa: DFA, path: str):
    with open(path, 'w') as f:
        json.dump(dfa.to_dict(), f, indent=2)
