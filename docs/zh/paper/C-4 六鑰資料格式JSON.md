# C-4　六鑰臨界資料格式JSON

>  本附錄示範如何以**單一 JSON 檔**封裝六鑰指標  
> （$\zeta_{1\ldots6}$）、加權距離 $D_w$、臨界旗標 $C_i$  
> 以及必要的實驗中繼資料。  
> **Fork、修改、推翻、另立格式皆歡迎。**

---
## 草案目的（Purpose）

1. **重分析／駁斥**：任何研究者可直接讀取 *.sixkeys.json*，  
   重算 ROC / AUC 或提出反例。  
2. **跨實驗比較**：統一欄位與單位，便於多中心匯整／形上 meta-analysis。  
3. **競賽／基準**：作為未來 “SixKeys-Challenge” 的提交介面。

---
## 結構定義（Schema）

### 1　檔名規則

```text
sub-<ID>[_ses-<label>][_task-<label>]_sixkeys.json
# 建議與 BIDS side-car 放在同層（derivatives/SixKeys/）
````

_範例_：`sub-03_ses-postpropofol_task-rest_sixkeys.json`

<!-- 手動換頁 -->
<div class="pagebreak"></div>

### 2　JSON 頂層欄位

| 欄位                | 型別 / 單位               | 說明                                             |
| ----------------- | --------------------- | ---------------------------------------------- |
| `schema_version`  | `string`              | **必填**；目前固定 `"0.1"`                            |
| `weights_version` | `string`              | 權重向量版本（例：`"2025-v1.0"`）                        |
| `subject_id`      | `string`              | 對應 _participants.tsv_                          |
| `session`         | `string`              | 多次掃描 / 場次（例：`ses-02`）                          |
| `condition`       | `string`              | Awake / N2 / Dex-light / Propofol-deep …       |
| `sampling_rate`   | `number` or `object`  | Hz；可用物件包多訊號：`{"EEG":1000,"MEG":2000}`          |
| `time_window`     | `number` \| `array` s | 計算 ζ 的滑窗；若各鑰不同可存陣列                             |
| `zetas`           | `object`              | 六鑰標準化座標，見 **3**                                |
| `Dw`              | `number`              | $\displaystyle D_w=\sqrt{\sum_i w_i\zeta_i^2}$ |
| `C_flags`         | `object`              | 二元臨界判準 `0/1`（FELC … TEB）                       |
| `raw_refs`        | `object`              | 原始檔路徑／DOI／SHA-256                              |
| `in_manifold`*    | `boolean`             | _選填_；是否 $D_w<\theta_c$（門檻請在 `notes` 標註）        |
| `notes`           | `string` (GFM)        | 補充：裝置、藥物劑量、權重向量…                               |
### 3　`zetas` 子欄位

```json
"zetas": {
  "zeta1":  0.12,   // FELC
  "zeta2": -1.83,   // TEB (η)
  "zeta3":  0.47,   // RFI
  "zeta4": -0.28,   // ECGP
  "zeta5":  0.05,   // PWC
  "zeta6": -0.11    // ACI
}
```

- 缺值請以 `null` 填寫並於 `notes` 說明原因。
    
- 欲加入自訂指標，請另開命名空間 `extra_*`（驗證器將忽略）。
    
---

## 實作範例（Implementation）

### Python API

```python
from sixkeys.io import SixKeyRecord, save_record

rec = SixKeyRecord(
    schema_version = "0.1",
    weights_version= "2025-v1.0",
    subject_id     = "S03",
    session        = "ses-postpropofol",
    condition      = "propofol-deep",
    sampling_rate  = {"EEG": 1000},
    time_window    = 0.1,
    zetas          = [0.12, -1.83, 0.47, -0.28, 0.05, -0.11],
    Dw             = 1.274,
    C_flags        = {"FELC":0,"RFI":0,"ECGP":0,"PWC":0,"ACI":1,"TEB":0},
    raw_refs       = {"EEG":"sub-03_task-rest_eeg.fif"},
    in_manifold    = False,
    notes          = "Propofol Ce≈4 µg/ml；BIS≈35"
)

save_record(rec, "sub-03_ses-postpropofol_sixkeys.json")
```

### 命令列驗證器

```bash
sixkeys-validate  sub-03_ses-postpropofol_sixkeys.json
```

輸出範例：

```
✓ schema OK       ✓ zetas length = 6
✓ Dw recomputed   ✓ C_flags ∈ {0,1}
```

---

<!-- 手動換頁 -->
<div class="pagebreak"></div>

## O　示例資料（Observation）

|檔名|狀態|$D_w$|in_manifold|
|---|---|--:|---|
|`sub-01_task-rest_sixkeys.json`|Awake|0.143|true|
|`sub-02_task-sevo_sixkeys.json`|Sevo-mid|0.788|false|
|`sub-03_ses-postpropofol_task-rest_sixkeys.json`|Propofol-deep|1.274|false|

> _圖 H-1_：三筆樣本於六維雷達圖的差異（示意，略）。

---

## R　侷限與後續工作（Reflection）

1. **v0.1 僅存「單段平均」** —— 若需毫秒級 ζ 序列，建議另存 _.h5_／_.zarr_。
    
2. **權重向量 `w_i`** 未鎖定；請在 `notes` 或獨立 _weights.json_ 指明版本。
    
3. **BIDS 整合** —— 歡迎提案 _BIDS-SixKeys_ side-car 規格。
    
4. **PR 徵集** —— 欄位增刪、單位爭議、JSON→Parquet 遷移請至 GitHub issue `#dataset_schema`。
    

---
## C　社群邀請（Call for Collaboration）

> 手上有 Awake / Sleep / Anesthesia EEG、MEG、Neuropixels、雙光子或 fMRI？  
> 歡迎試用本格式輸出 _.sixkeys.json_，並提交 PR / dataset link。  
---

<!-- 手動換頁 -->
<div class="pagebreak"></div>

## 附：最小 YAML-Schema （v0.1）

```yaml
# sixkey_schema.yaml · v0.1
$schema: "https://json-schema.org/draft/2020-12/schema"
title: "SixKeys Single-Record Schema"
type: object
required: [schema_version, subject_id, zetas, Dw]
additionalProperties: false

properties:
  schema_version: {type: string, const: "0.1"}
  weights_version:{type: string}

  subject_id:     {type: string}
  session:        {type: string}
  condition:      {type: string}
  sampling_rate:  {oneOf: [{type: number},{type: object}]}
  time_window:    {oneOf: [{type: number},{type: array}]}

  zetas:
    type: object
    required: [zeta1,zeta2,zeta3,zeta4,zeta5,zeta6]
    patternProperties:
      "^zeta[1-6]$": {type: ["number","null"]}

  Dw:    {type: number}

  C_flags:
    type: object
    patternProperties: {"^[A-Z]{3,4}$": {type: integer, enum: [0,1]}}

  raw_refs: {type: object, additionalProperties: {type: string}}
  in_manifold: {type: boolean}
  notes: {type: string}
```