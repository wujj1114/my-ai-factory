---
title: users 資料表設計與 Schema 規範
type: Schema
table_name: users
database: PostgreSQL
module: 會員認證模組
status: Active
created: 2026-08-30
updated: 2026-08-30
tags:
  - database-schema
  - postgresql
  - data-dictionary
---

# `users` 資料表設計 (Data Dictionary)

## 📌 實體用途概述
儲存系統所有註冊用戶之身分憑證、權限角色、安全狀態（鎖定/停用）與審計時間戳記。

* **所屬模組**：[[會員認證模組]]
* **底層資料庫**：PostgreSQL 16+（參見決策 [[docs/wiki/06_架構決策ADR/ADR-001_關聯式資料庫選用PostgreSQL|ADR-001]]）

---

## 📋 欄位字典定義 (Field Definitions)

| 欄位名稱 (Column) | 資料型別 (Type) | 允許 NULL | 預設值 (Default) | 主鍵/外鍵 | 欄位說明與商業邏輯 | 範例值 (Sample) |
| :--- | :--- | :---: | :--- | :---: | :--- | :--- |
| `id` | `UUID` | 否 | `gen_random_uuid()` | **PK** | 用戶唯一識別碼 (v4) | `9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d` |
| `email` | `VARCHAR(255)` | 否 | - | **UK** | 用戶登入電子郵件 (大小寫不敏感) | `dev.lead@example.com` |
| `password_hash` | `VARCHAR(255)` | 否 | - | - | Argon2id 加密後密碼雜湊字串 | `$argon2id$v=19$m=65536,t=3,p=4$...` |
| `display_name` | `VARCHAR(100)` | 否 | - | - | 介面顯示名稱 | `王大明` |
| `role` | `VARCHAR(32)` | 否 | `'USER'` | - | 角色權限：`ADMIN`, `DEVELOPER`, `USER` | `DEVELOPER` |
| `status` | `VARCHAR(32)` | 否 | `'PENDING'` | - | 狀態：`PENDING`, `ACTIVE`, `LOCKED`, `DISABLED` | `ACTIVE` |
| `failed_login_attempts` | `INT` | 否 | `0` | - | 連續登入失敗計數器 (>=5 觸發鎖定) | `0` |
| `locked_until` | `TIMESTAMPTZ` | 是 | `NULL` | - | 帳號鎖定截止時間戳記 | `2026-08-30T13:30:00Z` |
| `token_version` | `INT` | 否 | `1` | - | Token 輪轉版本號 (手動登出全裝置時遞增) | `1` |
| `last_login_at` | `TIMESTAMPTZ` | 是 | `NULL` | - | 最後一次成功登入時間 | `2026-08-30T12:50:00Z` |
| `created_at` | `TIMESTAMPTZ` | 否 | `CURRENT_TIMESTAMP` | - | 帳號建立時間 | `2026-08-30T10:00:00Z` |
| `updated_at` | `TIMESTAMPTZ` | 否 | `CURRENT_TIMESTAMP` | - | 最後資料更新時間 | `2026-08-30T12:50:00Z` |

---

## 🛠️ 實體 DDL 腳本 (PostgreSQL)

```sql
-- 啟用 pgcrypto 擴充套件以產生 UUID
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    role VARCHAR(32) NOT NULL DEFAULT 'USER',
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    failed_login_attempts INT NOT NULL DEFAULT 0,
    locked_until TIMESTAMPTZ NULL,
    token_version INT NOT NULL DEFAULT 1,
    last_login_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_users_email UNIQUE (email)
);

-- 建立索引加速查詢
CREATE INDEX idx_users_email_lower ON users (LOWER(email));
CREATE INDEX idx_users_status ON users (status);
```

---

## 🔗 雙向關聯拓樸 (Bi-directional Links)

### 讀寫此資料表之 API 端點
* 讀取並更新登入狀態：[[docs/wiki/05_API規格與介接/POST_api_v1_auth_login|POST /api/v1/auth/login]]

### 關聯規格與設計
* 需求來源：[[docs/wiki/01_使用者需求與PRD/REQ-001_會員登入與身份驗證|REQ-001 會員登入與身份驗證]]
* 業務流程：[[docs/wiki/02_系統分析SA/SA-001_會員登入業務流程與狀態機|SA-001 會員登入業務流程與狀態機]]
* 系統設計：[[docs/wiki/03_系統設計SD/SD-001_JWT認證與Token刷新機制|SD-001 JWT 認證與 Token 刷新機制]]
* 技術決策：[[docs/wiki/06_架構決策ADR/ADR-001_關聯式資料庫選用PostgreSQL|ADR-001 關聯式資料庫選用 PostgreSQL]]
