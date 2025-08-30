import argparse
from src.nfa import build_from_regex
from src.dfa import nfa_to_dfa, simulate
from src.minimizer import hopcroft_minimize
from src.visualize import visualize_dfa


def main():
    p = argparse.ArgumentParser()
    p.add_argument('regex')
    p.add_argument('--test', nargs='*', default=[])
    args = p.parse_args()
    nfa = build_from_regex(args.regex)
    dfa = nfa_to_dfa(nfa)
    m = hopcroft_minimize(dfa)
    print('Minimized DFA states:', len(m.states))
    for t in args.test:
        print(t, '->', 'SI' if simulate(m, t) else 'NO')

if __name__ == '__main__':
    main()
