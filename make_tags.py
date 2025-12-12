import argparse
import re, sys
from pathlib import Path

def format_number(x):
    # If x is (close to) integer, print as integer without decimal point
    if abs(x - round(x)) < 1e-12:
        return str(int(round(x)))
    # otherwise round to 2 decimals, strip trailing zeros
    s = f"{x:.1f}"
    s = s.rstrip('0').rstrip('.') if '.' in s else s
    return s

def extract_first_enumerate(tex):
    m = re.search(r'\\begin\{enumerate\}', tex)
    if not m:
        return None
    start = m.end()
    # find matching \end{enumerate} from start
    m2 = re.search(r'\\end\{enumerate\}', tex[start:])
    if not m2:
        return tex[start:]
    end = start + m2.start()
    return tex[start:end]

def split_items(enumerate_block):
    parts = re.split(r'(?m)^\s*\\item\b', enumerate_block)
    parts = [re.split(r'\\item\b', p)[0] for p in parts]
    return [p for p in parts if p.strip() != '']

def count_emoji_in_item(item, emoji_type):
    m = re.search(r'\\indicators\{([0-9.]+)\}\{([0-9.]+)\}', item)
    if not m:
        return 0.0
    difficulty, coding = m.groups()
    if emoji_type == 'hot-pepper':
        return float(difficulty)
    elif emoji_type == 'laptop':
        return float(coding)
    else:
        return 0.0

def extract_tags(tex):
    """
    Extract tags from lines beginning with '%' before the first \section.
    """
    tags = []
    before_section = tex.split(r'\section')[0]

    for line in before_section.splitlines():
        line = line.strip()
        if line.startswith("%"):
            tag = line[1:].strip()
            if tag:
                tags.append(tag)

    return tags

def main():
    base = Path("public/enigmas")
    if not base.exists():
        raise SystemExit("Error: public/enigmas/ does not exist")

    # find all public/enigmas/*/text.tex
    tex_files = list(base.glob("*/text.tex"))
    if not tex_files:
        raise SystemExit("No text.tex files found under public/enigmas/*/")

    for tex_path in tex_files:
        tex = tex_path.read_text(encoding='utf-8')

        enum_block = extract_first_enumerate(tex)
        if enum_block is None:
            question_items = []
        else:
            question_items = split_items(enum_block)

        n_questions = len(question_items)

        if n_questions == 0:
            print(f"Warning: no questions found in {tex_path}")
            continue

        # emoji counts
        hotpep_counts = [count_emoji_in_item(it, 'hot-pepper') for it in question_items]
        laptop_counts = [count_emoji_in_item(it, 'laptop') for it in question_items]

        total_hotpep = sum(hotpep_counts)
        total_laptop = sum(laptop_counts)

        mean_hotpep = total_hotpep / n_questions
        mean_laptop = total_laptop / n_questions

        mean_hotpep_str = format_number(mean_hotpep)
        mean_laptop_str = format_number(mean_laptop)

        # tags
        tags = extract_tags(tex)

        # output file
        out_path = tex_path.parent / "tags.txt"

        out_lines = []
        out_lines.append(mean_hotpep_str)
        out_lines.append(mean_laptop_str)
        out_lines.extend(tags)

        out_path.write_text("\n".join(out_lines) + "\n", encoding='utf-8')

        print(f"Wrote {out_path}  (questions={n_questions}, "
              f"laptop={total_laptop}, hotpep={total_hotpep})")


if __name__ == '__main__':
    main()
