import os
import re


def translate_matlab_to_python(matlab_code):
    python_lines = []
    for line in matlab_code.splitlines():
        stripped = line.strip()
        # comment conversion
        if '%' in line:
            parts = line.split('%', 1)
            code_part, comment_part = parts[0], parts[1]
            line = code_part + '#' + comment_part
        # remove trailing semicolons
        if line.rstrip().endswith(';'):
            line = line.rstrip()[:-1]
        # simple operators
        line = line.replace('~=', '!=')
        line = line.replace('&&', ' and ')
        line = line.replace('||', ' or ')
        # function definition
        m = re.match(r"\s*function\s+(?:\[(.*?)\]|(\w+))\s*=\s*(\w+)\((.*?)\)", stripped)
        if m:
            outputs = m.group(1) or m.group(2) or ''
            name = m.group(3)
            args = m.group(4)
            line = f'def {name}({args}):'
            python_lines.append(line)
            if outputs:
                python_lines.append(f'    # TODO: define outputs: {outputs}')
            continue
        if stripped == 'end':
            python_lines.append('# end')
            continue
        python_lines.append(line)
    return '\n'.join(python_lines) + '\n'


def convert_file(src_path, dst_root):
    with open(src_path, 'r') as f:
        code = f.read()
    py_code = translate_matlab_to_python(code)
    rel_path = os.path.splitext(os.path.relpath(src_path, '.'))[0] + '.py'
    dst_path = os.path.join(dst_root, rel_path)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w') as f:
        f.write(f"# Auto-translated from {src_path}\n\n")
        f.write(py_code)


def main():
    dst_root = 'python_version'
    for root, _, files in os.walk('.'):
        for name in files:
            if name.endswith('.m'):
                convert_file(os.path.join(root, name), dst_root)


if __name__ == '__main__':
    main()
