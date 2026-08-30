# 🤖 AI Agent 軟體開發工廠與 LLM Wiki 知識庫管理規範

本文件為全專案所有 AI Agent（包括 Coordinator、PM、Architect、Developer、Reviewer、Tester 及知識庫管理員）與人類工程師共同遵守之最高執行準則。

---

## 🏛️ 一、LLM Wiki 核心原則 (Core Principles)

### 1. 嚴禁空白或殘缺頁面 (No Sparse Notes)
* 知識庫（`docs/wiki/`）中所有 Markdown 筆記必須維持 **100% 完整度**。
* 每篇筆記必須具備標準 **YAML Frontmatter**（包含 `title`、`type`、`status`、`tags`、`created`、`updated`、`module` 等欄位）。
* 具備完整規格細節：具體資料型態、邊界條件、狀態轉換代碼、Request/Response JSON 範例與錯誤代碼，**嚴禁骨架空頁（Stub/Placeholder）或「待補充/TBD」字眼**。

### 2. 全拓樸雙向連結 (Bi-directional Links)
* 本知識庫專為 **Obsidian** 與 **AI 圖譜檢索** 設計，所有實體必須透過 `[[WikiLink]]` 進行雙向網狀連結。
* **強連結規則**：
  * 需求（PRD）必須連結至 ➔ 系統分析 `[[SA-xxx]]`、架構決策 `[[ADR-xxx]]`。
  * 系統分析（SA）必須連結至 ➔ 系統設計 `[[SD-xxx]]`、資料表 `[[xxx表]]`、`[[API端點]]`。
  * 資料庫 Schema 必須連結至 ➔ 關聯資料表 `[[xxx表]]`、存取此表的 `[[API端點]]`、所屬 `[[功能模組]]`。
  * API 規格必須連結至 ➔ 呼叫的 `[[資料表]]`、對應的 `[[系統設計SD]]`、驗證的 `[[測試案例]]`。
  * 架構決策（ADR）必須連結至 ➔ 影響的 `[[模組]]` 與 `[[系統設計SD]]`。
* **點開任一筆記，必須能回溯其上游需求來源與下游實作細節。**

### 3. 規格書 ◄► DDL ◄► 程式碼 三方對齊審計 (Doc-Code-DDL Sync)
* **單一真相來源 (Single Source of Truth, SSOT)**：
  * 當程式碼（`src/`）或資料庫 Migration 發生變更時，AI 必須主動或在 Pre-PR 階段同步更新 `docs/wiki/04_資料庫設計與Schema/` 與 `docs/wiki/05_API規格與介接/`。
  * 嚴禁出現「程式碼有欄位，但 SA/SD/Schema 文件沒有」或「規格書已廢棄，但程式碼仍在引用」的脫節現象。
  * 每次重大變更須透過 `scripts/audit_wiki_consistency.py` 執行三方交叉稽核。

### 4. 二進制與結構化資料讀取規範 (Binary & Spec Parser)
* 面對 `raw_specs/` 目錄下的二進制或結構化檔案（Word `.docx`、Excel `.xlsx`、PDF `.pdf`、舊系統 `.sql/.db`）：
  * **嚴禁直接盲讀二進制串流**。
  * **強制撰寫並執行專案 Python 腳本**（使用 `python-docx`, `pandas`, `openpyxl`, `pypdf`, `sqlite3`）。
  * 執行指令時必須強制加上 `-X utf8`（如 `python -X utf8 scripts/parse_raw_specs.py`），徹底杜絕 Windows 繁體中文 Big5/CP950 亂碼。

### 5. 目錄 (MOC) 與日誌 (Changelog) 即時同步
* 根目錄維護 `目錄.md`：作為知識庫的 Map of Content (MOC)，分類導覽所有子維度筆記。
* 根目錄維護 `日誌.md`：記錄每次架構演進、需求變更、Schema 異動與審計結果。
* 任何新增、重構、廢棄之規格，均須在 `目錄.md` 建立索引並於 `日誌.md` 留下記錄。

---

## 📂 二、知識庫標準目錄結構規範

```text
my-ai-factory/
├── raw_specs/                       # 原始客戶文件 (Word, Excel, PDF, DDL, 會議紀錄)
├── docs/wiki/                       # LLM Wiki 結構化知識庫 (Obsidian Vault 根目錄)
│   ├── 01_使用者需求與PRD/           # User Stories, AC, Feature Requirements
│   ├── 02_系統分析SA/               # 業務流程圖, 狀態機, 商業邏輯規則
│   ├── 03_系統設計SD/               # 模組架構, 循序圖, 元件設計
│   ├── 04_資料庫設計與Schema/       # 資料表字典, 實體 DDL, 索引與關聯
│   ├── 05_API規格與介接/             # RESTful/GraphQL 端點, Request/Response, Error Codes
│   ├── 06_架構決策ADR/              # Architecture Decision Records (ADR-001 ~)
│   └── 07_測試與驗收/               # 測試計畫, 整合測試案例, QA 查核點
├── scripts/                         # 自動化維護、轉換、三方一致性稽核 Python 腳本
├── 目錄.md                          # 知識庫總目錄 (Map of Content, MOC)
├── 日誌.md                          # 規格與開發變更日誌 (Dev Changelog)
├── AGENTS.md                        # 全域多 Agent 與 Wiki 運作規範 (本檔案)
└── CLAUDE.md                        # Claude / AI 助理快速參照指引
```

---

## 🔄 三、多 Agent 協同作業與 Wiki 讀寫矩陣

| Subagent 角色 | 主要讀取知識庫分區 | 主要產出/更新知識庫分區 | 審計與驗證責任 |
| :--- | :--- | :--- | :--- |
| **Coordinator** | `目錄.md`, `01_PRD`, `06_ADR` | `日誌.md`, GitHub Issues | 監督生命週期流轉與整體交付進度 |
| **PM Agent** | `raw_specs/`, `01_PRD` | `01_使用者需求與PRD/`, `目錄.md` | 確保原始需求轉化為無歧義之 User Story 與 AC |
| **Architect Agent** | `01_PRD`, `02_SA`, `06_ADR` | `02_SA/`, `03_SD/`, `04_Schema/`, `05_API/`, `06_ADR/` | 產出架構圖、DDL 與 API 規範，並全數建立雙向連結 |
| **Developer Agent** | `03_SD/`, `04_Schema/`, `05_API/` | `src/`, `tests/`, 更新 API/Schema 差異 | 嚴格依據 Wiki 規範編寫程式碼與單元測試 |
| **Reviewer Agent** | `03_SD/`, `04_Schema/`, `05_API/`, `src/` | PR Review Comments, `日誌.md` | 檢查 PR 實作與 Wiki 規格是否 100% 一致 |
| **Tester Agent** | `01_PRD`, `05_API/`, `07_測試與驗收/` | `07_測試與驗收/`, Bug Issues | 執行沙盒 E2E 測試，回填測試結果與覆蓋率報告 |
| **Wiki 管理員** | 全分區 Markdown 與程式碼 | `目錄.md`, `日誌.md`, 修正三方脫節 | 定期執行 `scripts/audit_wiki_consistency.py` 確保雙向連結無死鏈 |
