import os
import platform
from dataclasses import asdict
from itertools import cycle

from typing import List, Dict

__all__ = ('clear', 'Throbber', 'Table')


def clear():
    if os.name == 'nt' or platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


class Throbber:
    symbols = ('⠇', '⠏', '⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧')
    iter = iter(cycle(symbols))

    def __repr__(self):
        return next(self.iter)


class Table:
    columns: Dict[str, int]  # Dict[head, column size]
    rows: List[str]
    margin = 4

    def __init__(self, cls, data, weight=5):
        self.columns = {key: max(weight, len(key)) for key in cls.columns()}
        self.rows = []
        for i, ob in enumerate(data, start=1):
            ob_dict = asdict(ob)
            ob_dict['id'] = str(i)

            row: List[str] = []
            for head, w in self.columns.items():
                v = str(ob_dict.get(head, ''))
                self.columns[head] = max(w, len(v))
                row.append(v)
            self.rows.append(row)

    def __repr__(self):
        sizes = []
        header = []
        for c, w in self.columns.items():
            size = w + self.margin
            sizes.append(size)
            header.append(c.upper().ljust(size))

        resp = [''.join(header)]
        for row in self.rows:
            resp.append(''.join(
                cell.ljust(sizes[i]) for i, cell in enumerate(row)
            ))
        return '\n'.join(resp)