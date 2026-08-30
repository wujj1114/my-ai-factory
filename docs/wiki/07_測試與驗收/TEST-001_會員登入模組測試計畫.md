---
title: TEST-001 會員登入模組測試計畫與驗收查核
type: TestPlan
module: 會員認證模組
status: Active
created: 2026-08-30
updated: 2026-08-30
tags:
  - test-plan
  - integration-test
  - qa-checklist
---

# TEST-001: 會員登入模組測試計畫與驗收標準

## 🎯 測試範疇 (Test Scope)
針對 [[docs/wiki/01_使用者需求與PRD/REQ-001_會員登入與身份驗證|REQ-001]] 所定義之登入驗收條件進行全覆蓋自動化與整合測試，包含正確性、邊界異常、安全防護與鎖定機制。

---

## 🧪 整合測試案例矩陣 (Test Matrix)

| 案例 ID | 測試案例描述 | 輸入資料 (Input) | 預期結果 (Expected Result) | 關聯 AC | 執行狀態 |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **TC-AUTH-01** | 正確帳號密碼登入 | `user@example.com` / 正確密碼 | HTTP 200，取得 JWT Token，`last_login_at` 更新 | AC-1 | 🟢 Pass |
| **TC-AUTH-02** | 錯誤密碼登入 | `user@example.com` / 錯誤密碼 | HTTP 401 `AUTH_INVALID_CREDENTIALS`，失敗次數+1 | AC-2 | 🟢 Pass |
| **TC-AUTH-03** | 不存在之 Email 登入 | `non_exist@test.com` / 任意密碼 | HTTP 401 `AUTH_INVALID_CREDENTIALS`（防帳號枚舉） | AC-2 | 🟢 Pass |
| **TC-AUTH-04** | 連續 5 次密碼錯誤鎖定 | 相同帳號連續 5 次錯誤登入 | 第 5 次回傳 HTTP 403，帳號狀態變為 `LOCKED` | AC-3 | 🟢 Pass |
| **TC-AUTH-05** | 鎖定期間嘗試登入 | 已鎖定帳號 + 正確密碼 | HTTP 403 `AUTH_ACCOUNT_LOCKED`，拒絕核發 Token | AC-4 | 🟢 Pass |
| **TC-AUTH-06** | 格式不正確之 Email | `invalid-email-format` | HTTP 400 `VALIDATION_FAILED` | - | 🟢 Pass |

---

## 🔍 自動化執行指令
```bash
# 於 Docker 沙盒中執行會員認證整合測試套件
pytest tests/auth/test_login_integration.py -v
```

---

## 🔗 雙向關聯拓樸 (Bi-directional Links)
* 驗證之需求規格：[[docs/wiki/01_使用者需求與PRD/REQ-001_會員登入與身份驗證|REQ-001 會員登入與身份驗證]]
* 驗證之業務流程：[[docs/wiki/02_系統分析SA/SA-001_會員登入業務流程與狀態機|SA-001 會員登入業務流程與狀態機]]
* 驗證之系統設計：[[docs/wiki/03_系統設計SD/SD-001_JWT認證與Token刷新機制|SD-001 JWT 認證與 Token 刷新機制]]
* 驗證之 API 端點：[[docs/wiki/05_API規格與介接/POST_api_v1_auth_login|POST /api/v1/auth/login]]
* 存取之資料表：[[docs/wiki/04_資料庫設計與Schema/users表|users 表]]
