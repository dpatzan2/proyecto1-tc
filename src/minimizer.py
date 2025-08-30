from typing import Dict, Set
from src.dfa import DFA

# Algoritmo de Hopcroft para minimizar un AFD

def hopcroft_minimize(dfa: DFA) -> DFA:
    """Minimiza el DFA usando el algoritmo de Hopcroft.

    Devuelve un nuevo objeto `DFA` equivalente y mínimo.
    """
    # partición inicial: estados de aceptación y no aceptación
    all_states = set(dfa.states)
    P = [set(dfa.accepts), all_states - set(dfa.accepts)]
    W = [set(dfa.accepts), all_states - set(dfa.accepts)]
    symbols = list(dfa.symbols)
    while W:
        A = W.pop()
        for c in symbols:
            # X = estados que tienen una transición con c hacia A
            X = set()
            for q in all_states:
                dst = dfa.transitions.get(q, {}).get(c)
                if dst in A:
                    X.add(q)
            newP = []
            for Y in P:
                inter = Y & X
                diff = Y - X
                if inter and diff:
                    # Y se divide en inter y diff
                    newP.append(inter)
                    newP.append(diff)
                    if Y in W:
                        W.remove(Y)
                        W.append(inter)
                        W.append(diff)
                    else:
                        # añadir la parte más pequeña a W para eficiencia
                        if len(inter) <= len(diff):
                            W.append(inter)
                        else:
                            W.append(diff)
                else:
                    newP.append(Y)
            P = newP
    # build new DFA
    # construir el nuevo DFA a partir de la partición P
    reprs = [next(iter(s)) for s in P if s]
    mapping = {}
    for i, block in enumerate(P):
        for q in block:
            mapping[q] = i
    new_trans = {}
    new_accepts = set()
    for q in all_states:
        mq = mapping[q]
        new_trans.setdefault(mq, {})
        for c, dst in dfa.transitions.get(q, {}).items():
            new_trans[mq][c] = mapping[dst]
        if q in dfa.accepts:
            new_accepts.add(mapping[q])
    new_states = set(new_trans.keys())
    new_start = mapping[dfa.start]
    return DFA(start=new_start, accepts=new_accepts, states=new_states, transitions=new_trans, symbols=dfa.symbols)
