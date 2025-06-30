# Simple Matlab to Python translator for SCAnS EV_charging directory
# This script provides a naive line-based translation of Matlab .m files
# to Python. The conversion is minimal and primarily converts function
# definitions and comments. Loops and indexing remain largely unchanged
# and may require manual editing.

import re
from pathlib import Path

src_dir = Path('EV_charging')

for m_file in src_dir.rglob('*.m'):
    py_lines = []
    with open(m_file, 'r') as f:
        for line in f:
            # Convert comments
            line = re.sub(r'%+', '#', line)
            # Convert function definitions
            match = re.match(r'^function\s+(\[?[^=]*\]?\s*=\s*)?(\w+)\s*\((.*)\)', line.strip())
            if match:
                outputs, name, args = match.groups()
                if outputs:
                    outputs = outputs.strip().rstrip('=')
                    outputs = outputs.strip('[] ')
                    out_vars = [v.strip() for v in outputs.split(',') if v]
                    if len(out_vars) == 1:
                        ret = out_vars[0]
                    else:
                        ret = ', '.join(out_vars)
                else:
                    ret = ''
                line = f"def {name}({args}):"
                if ret:
                    line += f"\n    # returns {ret}"
                py_lines.append(line + "\n")
                continue
            # Remove 'end' statements
            if line.strip() == 'end':
                continue
            py_lines.append(line)
    py_path = m_file.with_suffix('.py')
    with open(py_path, 'w') as pf:
        pf.writelines(py_lines)
    print(f'Translated {m_file} -> {py_path}')
