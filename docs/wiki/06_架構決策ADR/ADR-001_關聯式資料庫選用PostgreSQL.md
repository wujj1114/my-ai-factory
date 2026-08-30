---
title: ADR-001 關聯式資料庫選用 PostgreSQL
type: ADR
status: Accepted
date: 2026-08-30
deciders: 首席架構師, 專案團隊
module: 基礎架構
tags:
  - architecture-decision
  - database
  - postgresql
---

# ADR-001: 關聯式資料庫選用 PostgreSQL

## 📌 脈絡與問題陳述 (Context and Problem Statement)
本專案為多智能體自動化軟體工廠及對應的業務應用系統，需要持久化存儲使用者身分、角色權限、專案元數據與稽核日誌。我們需要一個支援強 ACID 特性、高可靠性、優秀 JSON/JSONB 支援且與多數 ORM (Prisma / SQLAlchemy / TypeORM) 深度相容的關聯式資料庫。

## 🎯 決策驅動因素 (Decision Drivers)
1. **資料完整性與關聯強約束**：多租戶與使用者權限體系需要強嚴謹的外鍵與交易隔離機制。
2. **非結構化擴充性**：後續各 Agent 產出之中繼 JSON 結構需以高效 JSONB 格式保存。
3. **生態系與開源支援度**：在 Docker 沙盒及雲端託管服務中具備極高成熟度。

## 💡 考量方案 (Considered Options)
* **方案 A**: PostgreSQL (v16+)
* **方案 B**: MySQL (v8.0+)
* **方案 C**: MongoDB (v7.0+)

## 🏆 決策結果 (Decision Outcome)
**選定方案 A (PostgreSQL)**，因為它在進階查詢功能（CTE, Window Function）、複雜索引（GIN, GiST）及 JSONB 原生查詢上具備絕對優勢，能最佳化支援後續知識庫中繼資料與業務系統需求。

### 正面影響 (Positive Consequences)
* 提供完美的 ACID 與資料一致性保證。
* 原生 JSONB 支援讓未來的 Schema 擴展更加彈性。
* 完備的開源生態與 Docker 鏡像支援。

### 負面影響 / 緩解措施 (Negative Consequences & Mitigations)
* **連線管理負擔**：高並發時需配置 PgBouncer 或連線池機制。

## 🔗 雙向關聯實體 (Related Entities)
* 影響的資料庫 Schema：[[docs/wiki/04_資料庫設計與Schema/users表|users 表]]
* 關聯系統設計：[[docs/wiki/03_系統設計SD/SD-001_JWT認證與Token刷新機制|SD-001 JWT 認證與 Token 刷新機制]]
* 關聯需求：[[docs/wiki/01_使用者需求與PRD/REQ-001_會員登入與身份驗證|REQ-001 會員登入與身份驗證]]
