"""Bytecode scorer.

MUST HAVE REQUIREMENTS
- Accept a Python file path argument or Python source from stdin.
- Compute a deterministic bytecode instruction count score.
- Print only the numeric score to keep it script-friendly.
"""

import dis
import pathlib
import sys
import types


def _score(code):
    n = sum(1 for _ in dis.get_instructions(code))
    for obj in code.co_consts:
        if type(obj) is types.CodeType:
            n += _score(obj)
    return n


def main():
    src = (
        pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else sys.stdin.read()
    )
    print(_score(compile(src, "<stdin>", "exec")))


if __name__ == "__main__":
    main()
