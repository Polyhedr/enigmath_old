import re
from pathlib import Path
bp=breakpoint

def extract_tags(tex):
    before_section, after_section = tex.split(r'\section*{')[:2]
    title = after_section.split(r'}')[0]
    tags = [title]
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
        
        out_lines = []
        out_lines.append(format_number(hotpep))
        out_lines.append(format_number(laptop))
        out_lines.extend(tags)

        out_path.write_text("\n".join(out_lines) + "\n", encoding='utf-8')

        print(f"Wrote {out_path} hotpep={hotpep}, laptop={laptop})")

if __name__ == '__main__':
    main()