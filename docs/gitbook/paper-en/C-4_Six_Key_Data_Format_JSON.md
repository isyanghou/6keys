---
title: "C-4_Six-Key Data Format JSON"
date: 2025-06-22
language: en-US
encoding: UTF-8
---
# Appendix C-4　Six-Key Data Format JSON

>  This appendix demonstrates how to encapsulate six-key indicators  
> ($\zeta_{1\ldots6}$), weighted distance $D_w$, critical flags $C_i$  
> and necessary experimental metadata in a **single JSON file**.  
> **Fork, modify, refute, or establish alternative formats are all welcome.**

---
## Draft Purpose

1. **Re-analysis/Refutation**: Any researcher can directly read *.sixkeys.json*,  
   recalculate ROC/AUC or provide counterexamples.  
2. **Cross-experimental Comparison**: Unified fields and units facilitate multi-center aggregation/meta-analysis.  
3. **Competition/Benchmark**: Serves as submission interface for future "SixKeys-Challenge".

---
## Structure Definition (Schema)

### 1　File Naming Convention

```text
sub-<ID>[_ses-<label>][_task-<label>]_sixkeys.json
# Recommended to place in same layer as BIDS side-car (derivatives/SixKeys/)
````

_Example_: `sub-03_ses-postpropofol_task-rest_sixkeys.json`

<!-- Manual page break -->
<div class="pagebreak"></div>

### 2　JSON Top-Level Fields

| Field             | Type / Unit           | Description                                      |
| ----------------- | --------------------- | ------------------------------------------------ |
| `schema_version`  | `string`              | **Required**; currently fixed at `"0.1"`         |
| `weights_version` | `string`              | Weight vector version (e.g., `"2025-v1.0"`)      |
| `subject_id`      | `string`              | Corresponds to _participants.tsv_                |
| `session`         | `string`              | Multiple scans/sessions (e.g., `ses-02`)         |
| `condition`       | `string`              | Awake / N2 / Dex-light / Propofol-deep …        |
| `sampling_rate`   | `number` or `object`  | Hz; can use object for multi-signal: `{"EEG":1000,"MEG":2000}` |
| `time_window`     | `number` \| `array` s | Sliding window for ζ calculation; can store array if different for each key |
| `zetas`           | `object`              | Six-key standardized coordinates, see **3**      |
| `Dw`              | `number`              | $\displaystyle D_w=\sqrt{\sum_i w_i\zeta_i^2}$  |
| `C_flags`         | `object`              | Binary critical criteria `0/1` (FELC … TEB)      |
| `raw_refs`        | `object`              | Raw file paths/DOI/SHA-256                       |
| `in_manifold`*    | `boolean`             | _Optional_; whether $D_w<\theta_c$ (threshold noted in `notes`) |
| `notes`           | `string` (GFM)        | Supplements: device, drug dosage, weight vectors… |

### 3　`zetas` Sub-fields

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

- For missing values, please fill with `null` and explain the reason in `notes`.
    
- To add custom indicators, please open another namespace `extra_*` (validator will ignore).
    
---

## Implementation Example

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
    notes          = "Propofol Ce≈4 µg/ml; BIS≈35"
)

save_record(rec, "sub-03_ses-postpropofol_sixkeys.json")
```

### Command Line Validator

```bash
sixkeys-validate  sub-03_ses-postpropofol_sixkeys.json
```

Output example:

```
✓ schema OK       ✓ zetas length = 6
✓ Dw recomputed   ✓ C_flags ∈ {0,1}
```

---

<!-- Manual page break -->
<div class="pagebreak"></div>

## O　Example Data (Observation)

|Filename|State|$D_w$|in_manifold|
|---|---|--:|---|
|`sub-01_task-rest_sixkeys.json`|Awake|0.143|true|
|`sub-02_task-sevo_sixkeys.json`|Sevo-mid|0.788|false|
|`sub-03_ses-postpropofol_task-rest_sixkeys.json`|Propofol-deep|1.274|false|

> _Figure H-1_: Differences of three samples in six-dimensional radar chart (schematic, omitted).

---

## R　Limitations and Future Work (Reflection)

1. **v0.1 only stores "single-segment average"** —— For millisecond-level ζ sequences, recommend separate _.h5_/_.zarr_ storage.
    
2. **Weight vector `w_i`** not locked; please specify version in `notes` or separate _weights.json_.
    
3. **BIDS Integration** —— Welcome proposals for _BIDS-SixKeys_ side-car specification.
    
4. **PR Collection** —— For field additions/deletions, unit disputes, JSON→Parquet migration, please go to GitHub issue `#dataset_schema`.
    

---
## C　Community Invitation (Call for Collaboration)

> Have Awake/Sleep/Anesthesia EEG, MEG, Neuropixels, two-photon or fMRI data?  
> Welcome to try this format to output _.sixkeys.json_ and submit PR/dataset link.  
---

<!-- Manual page break -->
<div class="pagebreak"></div>

## Appendix: Minimal YAML-Schema (v0.1)

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