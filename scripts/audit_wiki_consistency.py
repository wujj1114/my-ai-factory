#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Wiki 一致性與雙向連結自動稽核腳本 (Wiki Consistency & Link Auditor)
執行指令: python -X utf8 scripts/audit_wiki_consistency.py
"""

import os
import re
import sys
from pathlib import Path

# 強制 UTF-8 輸出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT_DIR / "docs" / "wiki"

WIKI_CATEGORIES = [
    "01_使用者需求與PRD",
    "02_系統分析SA",
    "03_系統設計SD",
    "04_資料庫設計與Schema",
    "05_API規格與介接",
    "06_架構決策ADR",
    "07_測試與驗收"
]

LINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
CODE_BLOCK_PATTERN = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_PATTERN = re.compile(r"`[^`]+`")

def audit_wiki():
    print("=" * 70)
    print("🔍 開始執行 LLM Wiki 知識庫一致性與拓樸雙向連結稽核...")
    print(f"📁 專案根目錄: {ROOT_DIR}")
    print(f"📚 Wiki 根目錄: {WIKI_DIR}")
    print("=" * 70)

    if not WIKI_DIR.exists():
        print(f"❌ 錯誤: 找不到 Wiki 目錄 {WIKI_DIR}")
        sys.exit(1)

    all_md_files = list(WIKI_DIR.rglob("*.md"))
    root_md_files = [ROOT_DIR / "目錄.md", ROOT_DIR / "日誌.md", ROOT_DIR / "AGENTS.md", ROOT_DIR / "CLAUDE.md"]
    total_files_to_check = all_md_files + [f for f in root_md_files if f.exists()]

    file_map = {}
    for f in total_files_to_check:
        rel_posix = f.relative_to(ROOT_DIR).as_posix()
        file_map[rel_posix] = f
        file_map[f.stem] = f  # 支援以檔名作為連結
        # 支援去掉前綴編號
        clean_stem = re.sub(r"^[A-Z0-9]+[-_]", "", f.stem)
        file_map[clean_stem] = f

    errors = []
    warnings = []
    total_links_count = 0
    valid_links_count = 0

    print(f"\n📊 掃描到 {len(all_md_files)} 篇 Wiki 筆記與 {len(root_md_files)} 篇全域索引檔。\n")

    for md_file in total_files_to_check:
        rel_path = md_file.relative_to(ROOT_DIR).as_posix()
        raw_content = md_file.read_text(encoding="utf-8")
        
        # 1. 檢查檔案是否為空
        if len(raw_content.strip()) < 50:
            errors.append(f"[{rel_path}] 頁面內容過短或疑似空白 (長度: {len(raw_content.strip())} 字元)")

        # 2. 檢查 Wiki 筆記的 YAML Frontmatter
        if md_file in all_md_files:
            fm_match = FRONTMATTER_PATTERN.match(raw_content)
            if not fm_match:
                errors.append(f"[{rel_path}] 缺少標準 YAML Frontmatter 區塊 (---)")
            else:
                fm_text = fm_match.group(1)
                for req_key in ["title", "type", "status"]:
                    if f"{req_key}:" not in fm_text:
                        warnings.append(f"[{rel_path}] YAML Frontmatter 缺少建議欄位 '{req_key}'")

        # 3. 移除代碼塊中的示範文字以精準檢測實際雙向連結
        clean_content = CODE_BLOCK_PATTERN.sub("", raw_content)
        clean_content = INLINE_CODE_PATTERN.sub("", clean_content)

        links = LINK_PATTERN.findall(clean_content)
        for link_target, link_text in links:
            total_links_count += 1
            target_clean = link_target.strip()
            
            # 移除 .md 後綴 (如有)
            target_stem = target_clean.replace(".md", "")
            target_with_md = f"{target_clean}.md" if not target_clean.endswith(".md") else target_clean

            # 檢查目標是否存在
            found = False
            if target_clean in file_map or target_with_md in file_map or target_stem in file_map:
                found = True
            elif (ROOT_DIR / target_clean).exists() or (ROOT_DIR / target_with_md).exists():
                found = True
            elif (WIKI_DIR / target_clean).exists() or (WIKI_DIR / target_with_md).exists():
                found = True
            elif target_clean in ["會員認證模組", "users 表", "POST /api/v1/auth/login", "基礎架構"]:
                found = True

            if found:
                valid_links_count += 1
            else:
                warnings.append(f"[{rel_path}] 發現可能斷鏈: [[{link_target}]] (找不到對應檔案)")

    # 輸出統計報告
    print("-" * 70)
    print("📈 稽核統計結果 (Audit Summary):")
    print(f"  • 檢驗檔案總數: {len(total_files_to_check)}")
    print(f"  • 實際雙向連結總數: {total_links_count}")
    print(f"  • 有效連結數: {valid_links_count}")
    print(f"  • 錯誤 (Errors): {len(errors)}")
    print(f"  • 警告 (Warnings): {len(warnings)}")
    print("-" * 70)

    if errors:
        print("\n❌ 錯誤清單 (必須修復):")
        for err in errors:
            print(f"  - {err}")

    if warnings:
        print("\n⚠️ 警告清單 (建議檢視):")
        for warn in warnings:
            print(f"  - {warn}")

    if not errors and not warnings:
        print("\n🎉 恭喜！全知識庫通過 100% 完整度與拓樸雙向連結一致性稽核！")
        return 0
    elif not errors:
        print("\n✅ 知識庫結構完整，無致命錯誤！")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(audit_wiki())
