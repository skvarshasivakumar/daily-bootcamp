"""Parse the DSA sheet .docx into content/dsa.json.
Usage: python build_dsa.py dsa_sheet.docx"""
import json, re, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def main(path: str) -> None:
    z = zipfile.ZipFile(path)
    rels = {r.get("Id"): r.get("Target")
            for r in ET.fromstring(z.read("word/_rels/document.xml.rels"))}
    body = ET.fromstring(z.read("word/document.xml")).find(W + "body")

    items, section, sub = [], "", ""
    for p in body.iter(W + "p"):
        plain, links = [], []
        for ch in p:
            if ch.tag == W + "hyperlink":
                label = "".join(t.text or "" for t in ch.iter(W + "t")).strip("[] ")
                url = rels.get(ch.get(R + "id"))
                if url:
                    links.append({"label": label or "Link", "url": url})
            elif ch.tag == W + "r":
                plain.append("".join(t.text or "" for t in ch.iter(W + "t")))
        text = re.sub(r"\s+", " ", "".join(plain)).strip()
        if not text:
            continue

        m = re.match(r"^(\d+)\.\s*(.*)$", text)
        if m:  # a problem line
            title = re.sub(r"\[Conceptual[^\]]*\]", "", m.group(2))
            title = re.sub(r"\[\s*\]", "", title)
            title = re.sub(r"\s+", " ", title).strip()
            items.append({"no": int(m.group(1)), "title": title,
                          "section": section, "sub": sub, "links": links})
            continue

        h = re.match(r"^(.*?)\s*\((\d+)(\s+questions)?\)$", text)
        if h:  # "Basics (30 questions)" = section, "Things to know... (9)" = subsection
            if h.group(3):
                section, sub = h.group(1), ""
            else:
                sub = h.group(1)

    out = Path(__file__).parent / "content" / "dsa.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")

    nums = [i["no"] for i in items]
    missing = sorted(set(range(1, max(nums) + 1)) - set(nums)) if nums else []
    print(f"Problems: {len(items)} | with links: {sum(1 for i in items if i['links'])} "
          f"| conceptual: {sum(1 for i in items if not i['links'])}")
    print("Missing numbers:", missing or "none")
    if len(items) != 456:
        print("WARNING: expected 456 problems, check the doc or tell me what looks off.")


if __name__ == "__main__":
    main(sys.argv[1])