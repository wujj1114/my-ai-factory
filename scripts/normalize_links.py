import re
from pathlib import Path

wiki_dir = Path("docs/wiki")
moc_file = Path("目錄.md")
log_file = Path("日誌.md")

files = list(wiki_dir.rglob("*.md"))
if moc_file.exists():
    files.append(moc_file)
if log_file.exists():
    files.append(log_file)

for f in files:
    content = f.read_text(encoding="utf-8")
    # 將 `[[...]]` 轉換為 [[...]]
    new_content = re.sub(r"`(\[\[[^`\]]+\]\])`", r"\1", content)
    if new_content != content:
        f.write_text(new_content, encoding="utf-8")
        print(f"✅ Converted native Obsidian links in: {f}")

print("All Wiki files converted to native Obsidian wikilinks.")
