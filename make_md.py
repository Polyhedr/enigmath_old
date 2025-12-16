from pathlib import Path
import re

def display_math(text, indent_step=3):
    """
    Normalize LaTeX display math blocks and indent all following lines.

    Supported input blocks:
      - \[ ... \]
      - $$ ... $$
      - \begin{equation*} ... \end{equation*}
      - \begin{align*} ... \end{align*}
    """
    indent = " " * indent_step

    # Unified regex for all display math blocks
    BLOCK_RE = re.compile(
        r"""
        \\\[.*?\\\] |
        \$\$.*?\$\$ |
        \\begin\{equation\*\}.*?\\end\{equation\*\} |
        \\begin\{align\*\}.*?\\end\{align\*\}
        """,
        re.DOTALL | re.VERBOSE
    )

    lines = text.splitlines()
    result = []
    i = 0
    indent_after = False

    # Helper to normalize a math block
    def normalize_block(block_text):
        # Remove outer delimiters
        block_text = re.sub(
            r'^\\\[|\\\]$|^\$\$|\$\$$|'
            r'^\\begin\{(?:equation|align)\*\}|'
            r'\\end\{(?:equation|align)\*\}$',
            '',
            block_text.strip(),
            flags=re.DOTALL
        )

        content = block_text.strip().splitlines()

        out = [
            indent + "$$",
            indent + r"\begin{align*}"
        ]
        out.extend(indent + line for line in content)
        out.append(indent + r"\end{align*}")
        out.append(indent + "$$")
        return out

    while i < len(lines):
        remaining = "\n".join(lines[i:])
        m = BLOCK_RE.search(remaining)

        if m and m.start() == 0:
            block = m.group(0)
            block_lines = block.count("\n") + 1

            result.extend(normalize_block(block))

            indent_after = True
            i += block_lines
            continue

        line = lines[i]

        if indent_after and line.strip():
            result.append(indent + line)
        else:
            result.append(line)

        i += 1

    return "\n".join(result)

def latex_lists(text, indent_step=3):
    """
    Transform LaTeX lists (itemize, enumerate, description) into indented text.
    - \item[label] Text -> - **Label:** Text
    - Nested lists increase indentation
    - All lines following a block inherit the block's indentation
    """
    BEGIN_RE = re.compile(r"\\begin\{(itemize|enumerate|description)\}")
    END_RE   = re.compile(r"\\end\{(itemize|enumerate|description)\}")
    ITEM_RE  = re.compile(r"\\item(?:\[(.*?)\])?\s*")

    result_lines = []
    i = 0
    n = len(text)
    indent_stack = []
    current_indent = 0
    inside_block = False
    post_block_indent = 0

    while i < n:
        # Begin of list
        m_begin = BEGIN_RE.match(text, i)
        if m_begin:
            indent_stack.append(current_indent)
            current_indent += indent_step
            inside_block = True
            i = m_begin.end()
            continue

        # End of list
        m_end = END_RE.match(text, i)
        if m_end:
            # After a block, remember its indentation
            post_block_indent = current_indent
            current_indent = indent_stack.pop() if indent_stack else 0
            inside_block = False
            i = m_end.end()
            continue

        # Item
        m_item = ITEM_RE.match(text, i)
        if m_item:
            i = m_item.end()
            label = m_item.group(1)
            start = i
            while i < n:
                if ITEM_RE.match(text, i) or BEGIN_RE.match(text, i) or END_RE.match(text, i):
                    break
                i += 1
            item_text = text[start:i].strip()
            prefix = " " * current_indent + "- "
            if label:
                line_prefix = f"{prefix}**{label}** "
            else:
                line_prefix = prefix
            result_lines.append(line_prefix + ' '.join(item_text.splitlines()))
            continue

        # Free text
        start = i
        while i < n:
            if ITEM_RE.match(text, i) or BEGIN_RE.match(text, i) or END_RE.match(text, i):
                break
            i += 1
        snippet = text[start:i]
        for line in snippet.splitlines():
            if line.strip():  # skip empty lines
                # If we just exited a block, use post_block_indent
                indent_to_use = post_block_indent if not inside_block else current_indent
                result_lines.append(" " * indent_to_use + line)
            else:
                # Preserve empty line
                result_lines.append("")

    return "\n".join(result_lines)

class MD:
    le, re = r'{', r'}'

    def __init__(self, tex_path):
        self.tex_path = tex_path
        self.done_list = [
"l-echiquier-du-diable",
"l-enigme-de-freudenthal",
"la-part-du-tresor",
"la-prison-circulaire-de-taille-inconnue",
"le-defi-des-trois-des",
"les-ages-des-trois-enfants",
"les-trois-dieux",
"manger-un-max-de-pizza",
"plus-rien-sur-la-ligne",
"probleme-de-pesee",
"quadrivillage",
"recruter-un-stagiaire",
]
        self.done = sum(p in str(self.tex_path) for p in self.done_list)
        self.raw_text = self.remove_comments(tex_path.read_text(encoding='utf-8').split(r'\subsection')[1])
        self.structured_text = self.split(re.sub(r'\\item\s+\\indicators', r'\\item\\indicators', self.raw_text))

    def remove_comments(self, t):
        return '\n'.join([l.split('%')[0] for l in t.split('\n')])
    
    def process(self, t, indent_math):
        t = re.sub(r'^[ \t]+', '', t, flags=re.MULTILINE)
        t = latex_lists(t)
        t = t.replace(r'\og ', '"').replace(r' \fg{}', '"')
        t = t.replace("\medskip", "\n\n")
        t = t.replace(r'\(', '$').replace(r'\)', '$')
        t = t.replace(r'---', '—')
        t = t.replace(r'~', '')
        t = display_math(t, indent_math)
        # if quad is in t, and if we split by begin, the first chunck do not contain a &, then we replace quad by //&
        # new line with a sigle ponctuation...
        return t
    
    def build(self):
        out = "## Énoncé\n\n"
        out += self.process(self.structured_text['statement'], 0)
        out += '\n\n**Questions :**\n\n'
        for e, q in enumerate(self.structured_text["questions"]):
            out += f"{e+1}. {q['indicators']} {self.process(q['text'], 4)}\n\n"
        out += "\n\n&nbsp;\n\n---"
        self.out = out
    
    def split(self, t):
        S, Q = t.split(r"\textbf{Questions}")
        out = {'statement' : S.split("{Énoncé}")[1], "questions" : []}
        for q in Q.split("\item\indicators")[1:]:
            indicators, text = self.process_q(q)
            out["questions"].append({'indicators' : indicators, 'text' : text})
        out["questions"][-1]['text'] = f"\end{self.le}enumerate{self.re}".join(out["questions"][-1]['text'].split(f"\end{self.le}enumerate{self.re}")[:-1])
        return out

    def export(self, outfile="output.md"):
        Path(outfile).write_text(self.out, encoding="utf-8")
        print(f"Wrote {outfile}")

    def process_q(self, q):
        q_split = q.split(self.re)
        difficulty, computer, text = float(q_split[0][1:]), float(q_split[1][1:]), self.re.join(q_split[2:])

        indicators = f"🌶️${self.le}{self.re}^{self.le}\color{self.le}red{self.re}{difficulty}{self.re}$"
        if computer >0:
            indicators += f"💻${self.le}{self.re}^{self.le}\color{self.le}blue{self.re}{computer}{self.re}$"

        return indicators, text














bp=breakpoint
left_embrace = "{"
right_embrace = "}"
OK = [
# "L'échiquier du diable",
# "La part du trésor",
# "La prison circulaire de taille inconnue",
# "Le défi des trois dés",
# "Les trois dieux",
# "Les âges des trois enfants",
# "L’énigme de Freudenthal",
# "Manger un max de pizza",
]

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



def convert2md(t):
    t = t.replace('\n\\medskip\n\\textbf', '')
    t = t.replace("*{Énoncé}", "## Énoncé\n\n")
    t = t.replace(r'\(', '$').replace(r'\)', '$')
    t = re.compile(r'\$\$(.+?)\$\$', re.DOTALL).sub(r'$$\\begin{equation*}\1\\end{equation*}$$', t)
    t = t.replace(r'\[', f'$$\\begin{left_embrace}equation*{right_embrace}').replace(r'\]', f'\\end{left_embrace}equation*{right_embrace}$$')
    t = t.replace(r'\og ', '"').replace(r' \fg{}', '"')
    t = t.replace(r'---', '—')
    t = t.replace(r'~', '')
    t = re.sub(r'^[ \t]+', '', t, flags=re.MULTILINE)
    t = unwrap_newlines_latex(t)
    t = latex_itemize_to_md(t)
    t = re.sub(fr'$$\begin{left_embrace}equation*{right_embrace}', fr'\n$$\n\begin{left_embrace}equation*{right_embrace}\n', t)
    # t = re.sub(fr'\\end{left_embrace}equation*{right_embrace}$$', fr'\n\\end{left_embrace}equation*{right_embrace}\n$$\n', t)
    # t = re.sub(fr'$$\\begin{right_embrace}equation*{left_embrace}',fr"\n$$\n\\begin{right_embrace}equation*{left_embrace}\n",t)
    return t








def main():
    base = Path("public/enigmas")
    if not base.exists():
        raise SystemExit("Error: public/enigmas/ does not exist")

    # find all public/enigmas/*/text.tex
    tex_files = list(base.glob("*/text.tex"))
    if not tex_files:
        raise SystemExit("No text.tex files found under public/enigmas/*/")

    for tex_path in tex_files:
        check = sum(r in str(tex_path) for r in OK)
        out_path = tex_path.parent / "tags.txt"
        tex = tex_path.read_text(encoding='utf-8')
        text = tex.split(r'\subsection')[1]



        # create the .md
        text = re.sub(r'\\item\s+\\indicators', r'\\item\\indicators', text)
        text = re.sub(fr'\\begin{left_embrace}description{right_embrace}', fr'\\begin{left_embrace}itemize{right_embrace}', text)
        text = re.sub(fr'\\begin{left_embrace}align*{right_embrace}', fr'$$\\begin{left_embrace}align*{right_embrace}', text)
        text = re.sub(fr'\\end{left_embrace}description{right_embrace}', fr'\\end{left_embrace}itemize{right_embrace}', text)
        text = re.sub(fr'\\end{left_embrace}align*{right_embrace}', fr'\\end{left_embrace}align*{right_embrace}$$', text)
        S,Q = text.split("{Questions}")
        out = convert2md(S)
        # if not check:
        #     bp()

        out += '\n\n**Questions :**\n\n'
        for e, q in enumerate(Q.split("\item\indicators")[1:]):
            indicators, q = process_indicators(q)
            out += f"{e+1}. {indicators} {q}\n\n"
        out = f"\end{left_embrace}enumerate{right_embrace}".join(out.split(f"\end{left_embrace}enumerate{right_embrace}")[:-1])
        out += "\n\n&nbsp;\n\n---"
        
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
    base = Path("public/enigmas")
    if not base.exists():
        raise SystemExit("Error: public/enigmas/ does not exist")

    # find all public/enigmas/*/text.tex
    tex_files = list(base.glob("*/text.tex"))
    if not tex_files:
        raise SystemExit("No text.tex files found under public/enigmas/*/")

    for tex_path in tex_files:
        md = MD(tex_path)
        md.build()
        if md.done:
            md.export(str(tex_path).replace(tex_path.suffix,'.md'))
        else:
            md.export()
            print(tex_path)
            exit()