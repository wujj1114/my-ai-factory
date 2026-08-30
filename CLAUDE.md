# CLAUDE.md - AI 軟體開發工廠與 LLM Wiki 執行準則

本專案是一個遵循 **LLM Wiki 規範** 與 **多智能體流水線 (Multi-Agent Pipeline)** 的軟體開發專案。當你在本專案中進行任何開發、文檔編寫或代碼重構時，請嚴格遵守以下規則：

---

## 🎯 核心原則

1. **嚴禁空白筆記 (No Sparse Notes)**：
   - 知識庫位於 `docs/wiki/`。
   - 所有筆記均必須包含標準 YAML Frontmatter，具備完整的欄位定義、型別、範例值、狀態碼及 Mermaid 流程圖，嚴禁殘缺頁面。

2. **全拓樸雙向連結 (Bi-directional Links)**：
   - 廣泛使用 Obsidian 雙向連結語法 `[[檔案路徑或名稱|自訂文字]]`（例如 `[[docs/wiki/04_資料庫設計與Schema/users表|users 表]]` 或 `[[docs/wiki/05_API規格與介接/POST_api_v1_auth_login|POST /api/v1/auth/login]]`）。
   - 確保每個實體（表、API、模組、ADR、PRD）在圖譜中皆有上下游連結。

3. **規格 ◄► DDL ◄► 代碼 三方對齊 (Doc-Code-DDL Sync)**：
   - 修改程式碼或資料庫模型時，必須同步更新 `04_資料庫設計與Schema/` 與 `05_API規格與介接/`。
   - 任何變更均須同步記錄於 `日誌.md` 與 `目錄.md`。

4. **二進制檔案處理 (Binary Parsers)**：
   - 解析 `raw_specs/` 下之 Word/Excel/PDF/DB 時，一律透過 Python 腳本（`python -X utf8 scripts/...`）提取文字，杜絕 Big5/CP950 亂碼。

5. **MCP 工具安全**：
   - GitHub Token 請置於 `.antigravity/mcp_servers.json`（已受 `.gitignore` 保護），嚴禁將 Token 寫入任何公開文件或範本。

---

## 🧭 常用指令

```bash
# 執行 Wiki 一致性與雙向連結稽核
python -X utf8 scripts/audit_wiki_consistency.py

# 執行測試套件
pytest tests/
# 或 npm test
```
