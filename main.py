from src.regex_parser import to_postfix
from src.nfa import build_from_regex, save_nfa
from src.dfa import nfa_to_dfa, save_dfa, simulate, simulate_with_trace
from src.minimizer import hopcroft_minimize
from src.visualize import visualize_nfa, visualize_dfa

import datetime
import os


def safe_folder_name(s: str, max_len=40) -> str:
    # Replace problematic chars with underscores and truncate
    import re
    name = re.sub(r'[^0-9A-Za-z\-_.]', '_', s)
    if len(name) > max_len:
        name = name[:max_len]
    return name


def process_regex(regex: str, base_outdir: str, tests: list):
    regex = regex.strip()
    if not regex:
        return
    safe = safe_folder_name(regex)
    outdir = os.path.join(base_outdir, safe)
    os.makedirs(outdir, exist_ok=True)

    print('=== Entrada ===')
    print('Regex:', regex)

    postfix = to_postfix(regex)
    print('\n=== Postfix ===')
    print(postfix)

    # Build NFA
    nfa = build_from_regex(regex)
    nfa_path = os.path.join(outdir, 'nfa.json')
    save_nfa(nfa, nfa_path)
    print('\n=== AFN (Thompson) ===')
    print('Estados:', sorted(list(nfa.states)))
    print('Inicio:', nfa.start)
    print('Aceptacion:', nfa.accept)
    print('Transiciones (muestra):')
    for src, lst in nfa.transitions.items():
        for sym, dst in lst:
            print(f'  ({src}, {sym if sym is not None else "ε"}, {dst})')
    try:
        visualize_nfa(nfa, os.path.join(outdir, 'nfa'))
        print('NFA renderizado en:', os.path.join(outdir, 'nfa.png'))
    except Exception:
        pass

    # Build DFA
    dfa = nfa_to_dfa(nfa)
    dfa_path = os.path.join(outdir, 'dfa.json')
    save_dfa(dfa, dfa_path)
    try:
        visualize_dfa(dfa, os.path.join(outdir, 'dfa'))
        print('DFA renderizado en:', os.path.join(outdir, 'dfa.png'))
    except Exception:
        pass

    # Minimize DFA
    md = hopcroft_minimize(dfa)
    mdf_path = os.path.join(outdir, 'mdfa.json')
    save_dfa(md, mdf_path)
    try:
        visualize_dfa(md, os.path.join(outdir, 'mdfa'))
        print('DFA minimizado renderizado en:', os.path.join(outdir, 'mdfa.png'))
    except Exception:
        pass

    print('\n=== Archivos guardados en ===')
    print('  ', nfa_path)
    print('  ', dfa_path)
    print('  ', mdf_path)

    # Use provided tests (list of strings)
    if not tests:
        tests = ['babbaaaaa', 'abb', 'a', '']
    print('\n=== Simulaciones (AFD minimizado) ===')
    for t in tests:
        accepted, trace = simulate_with_trace(md, t)
        print('\nCadena:', repr(t), '->', 'SI' if accepted else 'NO')
        print('Traza:')
        for step in trace:
            if step[0] == 'start':
                print(f'  start -> state {step[1]}')
            else:
                prev, sym, nxt = step
                print(f'  ({prev}) -{sym}-> ({nxt})')


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Procesar regex desde un archivo txt (una por línea)')
    parser.add_argument('file', nargs='?', default='regexes.txt', help='archivo de entrada (por defecto regexes.txt)')
    parser.add_argument('--tests', dest='tests_file', default='tests.txt', help='archivo con cadenas de prueba (una por línea), por defecto tests.txt')
    args = parser.parse_args()

    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    base_outdir = os.path.join('resultados', ts)
    os.makedirs(base_outdir, exist_ok=True)

    if not os.path.exists(args.file):
        print('Archivo', args.file, 'no existe. Crea un archivo con expresiones regulares, una por línea.')
        return

    # Read tests file
    tests = []
    if os.path.exists(args.tests_file):
        with open(args.tests_file, 'r') as tf:
            for l in tf:
                l = l.strip()
                if not l or l.startswith('#'):
                    continue
                tests.append(l)
    else:
        print('Archivo de tests', args.tests_file, 'no encontrado; se usarán tests por defecto')

    with open(args.file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        process_regex(line, base_outdir, tests)


if __name__ == '__main__':
    main()
