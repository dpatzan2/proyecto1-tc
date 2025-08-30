from typing import Iterable
try:
    from graphviz import Digraph
    _HAS_GRAPHVIZ = True
except Exception:
    _HAS_GRAPHVIZ = False


def visualize_nfa(nfa, path='nfa'):
    if not _HAS_GRAPHVIZ:
        print('graphviz no instalado: omitiendo renderizado de NFA (instala paquete graphviz)')
        return
    dot = Digraph()
    for s in sorted(nfa.states):
        shape = 'doublecircle' if s == nfa.accept else 'circle'
        dot.node(str(s), shape=shape)
    for src, lst in nfa.transitions.items():
        for sym, dst in lst:
            label = sym if sym is not None else 'ε'
            dot.edge(str(src), str(dst), label=label)
    dot.render(path, format='png', cleanup=True)


def visualize_dfa(dfa, path='dfa'):
    if not _HAS_GRAPHVIZ:
        print('graphviz no instalado: omitiendo renderizado de DFA (instala paquete graphviz)')
        return
    dot = Digraph()
    for s in sorted(dfa.states):
        shape = 'doublecircle' if s in dfa.accepts else 'circle'
        dot.node(str(s), shape=shape)
    for src, trans in dfa.transitions.items():
        for sym, dst in trans.items():
            dot.edge(str(src), str(dst), label=sym)
    dot.render(path, format='png', cleanup=True)
