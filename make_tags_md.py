import re
from pathlib import Path
bp=breakpoint
left_embrace = "{"
right_embrace = "}"
OK = [
"L'échiquier du diable",
"La part du trésor",
"La prison circulaire de taille inconnue",
"Le défi des trois dés",
"Les trois dieux",
"Les âges des trois enfants",
]

def extract_tags(tex):
    tags = []
    before_section = tex.split(r'\section')[0]
    for line in before_section.splitlines():
        line = line.strip()
        if line.startswith("%"):
            tag = line[1:].strip()
            if tag:
                tags.append(tag)
    return tags

def format_number(x):
    if abs(x - round(x)) < 1e-12:
        return str(int(round(x)))
    s = f"{x:.1f}"
    s = s.rstrip('0').rstrip('.') if '.' in s else s
    return s

def extract_indicators(text):
    difficulties = []
    computers = []
    for line in text.splitlines():
        m = re.search(r'\\indicators\{([0-9.]+)\}\{([0-9.]+)\}', line)
        if m:
            difficulty, computer = m.groups()
            difficulties.append(float(difficulty))
            computers.append(float(computer))
    return max(difficulties), max(computers)


# .md

def unwrap_newlines_latex(text: str) -> str:

    placeholder_end = "__END_ITEMIZE_NL__"
    text = re.sub(fr'(\\end\{left_embrace}itemize\{right_embrace})([ \t]*)\n', r'\1\2' + placeholder_end, text)
    
    pattern = re.compile(r'(?<!\n)\n(?!\n|\s*\\item|' + placeholder_end + r')')
    text = pattern.sub(' ', text)

    text = text.replace(placeholder_end, '\n\n')

    return text

def latex_itemize_to_md(text: str) -> str:
    pattern = re.compile(
        r"\\begin\{itemize\}([\s\S]*?)\\end\{itemize\}",
        re.MULTILINE
    )

    def convert_block(block: str, indent_level: int = 0) -> str:
        lines = block.strip().split("\n")
        md = []
        indent = "\n   " * indent_level

        nested_content = []

        for line in lines:
            # Look for nested itemize environments
            if "\\begin{itemize}" in line:
                # Start capturing nested block
                nested_content.append(line)
                continue

            if nested_content:
                nested_content.append(line)
                # Check if this closes the nested environment
                if "\\end{itemize}" in line:
                    nested_block = "\n".join(nested_content)
                    # Recursively convert nested block
                    nested_md = replace_nested(nested_block, indent_level + 1)
                    md.append(nested_md)
                    nested_content = []
                continue

            # Detect items
            if "\\item" in line:
                content = re.sub(r"\\item\s*", "", line).strip()
                md.append(f"{indent}- {content}")
            else:
                # Continuation of previous item (rare)
                stripped = line.strip()
                if stripped:
                    md.append(f"{indent}  {stripped}")
        return "\n".join(md)

    def replace_nested(match, level=0):
        content = match.group(1)
        return convert_block(content, level)

    # Repeatedly replace the innermost itemize blocks
    while pattern.search(text):
        text = pattern.sub(lambda m: replace_nested(m, 1), text)
    return text

def string_to_md(text, outfile="output.md"):
    Path(outfile).write_text(text, encoding="utf-8")
    print(f"Wrote {outfile}")


def convert2md(t):
    t = t.replace('\n\\medskip\n\\textbf', '')
    t = t.replace("*{Énoncé}\n", "## Énoncé\n\n")
    t = t.replace(r'\(', '$').replace(r'\)', '$')
    t = t.replace(r'\og ', '"').replace(r' \fg{}', '"')
    t = t.replace(r'---', '—')
    t = t.replace(r'~', '')
    t = re.sub(r'^[ \t]+', '', t, flags=re.MULTILINE)
    t = unwrap_newlines_latex(t)
    t = latex_itemize_to_md(t)
    return t

def process_indicators(q):
    q = q.split(right_embrace)
    difficulty, computer = float(q[0][1:]), float(q[1][1:])
    out = f"🌶️${left_embrace}{right_embrace}^{left_embrace}{difficulty}{right_embrace}$"
    if computer >0:
        out += f"💻${left_embrace}{right_embrace}^{left_embrace}{computer}{right_embrace}$"
    return out, convert2md(f"{right_embrace}".join(q[2:]))

def main():
    base = Path("public/enigmas")
    if not base.exists():
        raise SystemExit("Error: public/enigmas/ does not exist")

    # find all public/enigmas/*/text.tex
    tex_files = list(base.glob("*/text.tex"))
    if not tex_files:
        raise SystemExit("No text.tex files found under public/enigmas/*/")

    for tex_path in tex_files:
        out_path = tex_path.parent / "tags.txt"
        tex = tex_path.read_text(encoding='utf-8')
        text = tex.split(r'\subsection')[1]

        # tags
        tags = extract_tags(tex)

        # indicators
        hotpep, laptop = extract_indicators(text)

        # create the .md
        text = re.sub(r'\\item\s+\\indicators', r'\\item\\indicators', text)
        S,Q = text.split("{Questions}")
        out = convert2md(S)
        out += '\n\n**Questions :**\n\n'
        for e, q in enumerate(Q.split("\item\indicators")[1:]):
            indicators, q = process_indicators(q)
            out += f"{e+1}. {indicators} {q}\n\n"
        out = f"\end{left_embrace}enumerate{right_embrace}".join(out.split(f"\end{left_embrace}enumerate{right_embrace}")[:-1])
        out += "\n\n&nbsp;\n\n---"
        check = sum(r in str(tex_path) for r in OK)
        if check:
            string_to_md(out, str(tex_path).replace(tex_path.suffix,'.md'))
        else:
            string_to_md(out)
            print(tex_path)
            exit()
        
        out_lines = []
        out_lines.append(format_number(hotpep))
        out_lines.append(format_number(laptop))
        out_lines.extend(tags)

        out_path.write_text("\n".join(out_lines) + "\n", encoding='utf-8')

        print(f"Wrote {out_path} hotpep={hotpep}, laptop={laptop})")

if __name__ == '__main__':
    main()