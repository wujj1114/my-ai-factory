---
title: POST /api/v1/auth/login 會員登入介面
type: API
method: POST
endpoint: /api/v1/auth/login
auth_required: false
module: 會員認證模組
status: Active
created: 2026-08-30
updated: 2026-08-30
tags:
  - api-spec
  - rest-api
  - authentication
---

# `POST /api/v1/auth/login` (會員登入)

## 📌 端點基本資訊
* **功能描述**：提供用戶以 Email 與密碼進行身分鑑別，成功後取得 JWT 存取憑證。
* **安全性要求**：公開端點 (Public)，配置 Rate Limiting (單一 IP 每分鐘最多 10 次)。
* **所屬模組**：[[會員認證模組]]

---

## 📥 請求參數規格 (Request)

### Headers
| Header 名稱 | 必填 | 範例值 | 說明 |
| :--- | :---: | :--- | :--- |
| `Content-Type` | 是 | `application/json` | 請求內容格式 |
| `User-Agent` | 是 | `Mozilla/5.0...` | 客戶端識別（用於審計日誌） |

### Body (JSON Schema)
```json
{
  "email": "user@example.com",
  "password": "Password123!"
}
```

| 欄位 (Field) | 型別 (Type) | 必填 | 驗證規則 (Validation) | 說明 |
| :--- | :--- | :---: | :--- | :--- |
| `email` | `string` | 是 | 符號 RFC 5322 Email 格式，最大 255 字元 | 登入電子郵件 |
| `password` | `string` | 是 | 長度 8-64 字元，不可全空白 | 明文密碼 |

---

## 📤 回應參數規格 (Response)

### 成功回應：HTTP 200 OK
```json
{
  "code": "SUCCESS",
  "message": "登入成功",
  "data": {
    "user": {
      "id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
      "email": "user@example.com",
      "displayName": "王大明",
      "role": "DEVELOPER"
    },
    "token": {
      "tokenType": "Bearer",
      "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expiresIn": 900,
      "refreshToken": "rf_7a8b9c0d1e2f3a4b5c6d..."
    }
  },
  "timestamp": "2026-08-30T13:20:00.123Z"
}
```

### 錯誤回應代碼表 (Error Codes)

| HTTP 狀態碼 | 錯誤代碼 (Error Code) | 觸發情境與原因 | 處理建議 |
| :---: | :--- | :--- | :--- |
| **400** | `VALIDATION_FAILED` | Email 格式不合法或密碼長度不足 | 請前端提示使用者檢查輸入內容 |
| **401** | `AUTH_INVALID_CREDENTIALS` | 帳號不存在或密碼錯誤 | 提示帳號密碼不符，計數失敗次數 |
| **403** | `AUTH_ACCOUNT_LOCKED` | 連續失敗達 5 次，帳號處於鎖定期間 | 提示鎖定截止時間，請稍後重試 |
| **429** | `RATE_LIMIT_EXCEEDED` | 該 IP 短時間內發送過多登入請求 | 觸發防禦，限制 1 分鐘後再試 |

---

## 🔗 雙向關聯拓樸 (Bi-directional Links)
* 存取與更新之資料表：[[docs/wiki/04_資料庫設計與Schema/users表|users 表]]
* 上游需求規格：[[docs/wiki/01_使用者需求與PRD/REQ-001_會員登入與身份驗證|REQ-001 會員登入與身份驗證]]
* 業務流程與狀態機：[[docs/wiki/02_系統分析SA/SA-001_會員登入業務流程與狀態機|SA-001 會員登入業務流程與狀態機]]
* 系統設計與循序圖：[[docs/wiki/03_系統設計SD/SD-001_JWT認證與Token刷新機制|SD-001 JWT 認證與 Token 刷新機制]]
* 測試驗證計畫：[[docs/wiki/07_測試與驗收/TEST-001_會員登入模組測試計畫|TEST-001 會員登入模組測試計畫]]
