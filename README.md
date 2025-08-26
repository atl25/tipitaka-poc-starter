# Tipitaka POC Starter – One‑Click ETL + Search

## 🗂 Project Structure

```
tipitaka-poc-starter/
├── docker-compose.yml              # your compose (example provided below)
├── bootstrap.sh                    # one-touch orchestrator
├── data/
│   └── download_folder.py          # downloads 'outputs/' from your Drive (optional)
└── etl/
    ├── Dockerfile.etl              # container for ETL steps
    ├── requirements.txt            # Python deps for ETL image
    └── app/
        ├── pipeline.py             # ETL entrypoint (schema + CSV + vectors + sanity search)
        ├── insert_vectors_generic.py
        ├── weaviate_multitier_setup_and_search_patched.py
        └── search_weaviate_labse_hybridfix.py
```

Your **model/data** artifacts are expected under **`data/outputs/`** (either pre-mounted or downloaded at runtime):

```
data/outputs/
├── windows_with_headings.csv
├── sentences_with_headings.csv
├── windows_2_3.csv
├── sentences_from_200.csv
├── subchunks_200.csv
├── chunks.csv
├── windows_ids.txt           ┐
├── windows_labse.npy         │
├── sentences_ids.txt         │  LaBSE vectors + ids (must align)
├── sentences_labse.npy       │
├── subchunks_ids.txt         │
├── subchunks_labse.npy       │
├── chunks_ids.txt            │
└── chunks_labse.npy          ┘
```


## ✅ Prerequisites

Docker (Docker Desktop on Windows/macOS, Docker Engine on Linux)

Windows မှာ Git Bash (သို့) PowerShell/CMD ကို အသုံးပြုနိုင်ပါတယ်


🚀 One-Click Setup

Git Bash (recommended):

cd tipitaka-poc-starter
./bootstrap.sh setup


setup သည် အလိုအလျောက် အောက်ပါ အဆင့်များကို လုပ်ဆောင်ပါတယ်—

up — Weaviate container run

build — ETL image build

load — pipeline.py ကို chạy (wait → schema → CSV → vectors → sanity search)


🧠 What the pipeline does

etl/app/pipeline.py (simple runner):

Wait for Weaviate readiness (/v1/.well-known/ready or OK)

Schema setup — 4 collections: Window, Sentence, Subchunk, Chunk

CSV Insert (BM25) — class တိုင်းအတွက် CSV တစ်ခုချင်းစီ တင်

windows_with_headings.csv မရှိရင် windows_2_3.csv fallback

sentences_with_headings.csv မရှိရင် sentences_from_200.csv fallback

Vector Insert (ရှိနေလျှင်သာ) — insert_vectors_generic.py နဲ့ ids/npy တင်

Sanity Search — Window collection ပေါ် mettā ကို စမ်းရှာ


# Search Quick Reference

# ---------- Bash / Git Bash / WSL ----------
# Window
python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Window --mode bm25   --query "mettā" --k 5
python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Window --mode vector --query "mettā" --k 5
python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Window --mode hybrid --alpha 0.5 --query "mettā" --k 5

# Sentence
python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Sentence --mode bm25   --query "Admonish (garahati)" --k 5
python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Sentence --mode vector --query "Admonish (garahati)" --k 5
python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Sentence --mode hybrid --alpha 0.5 --query "Admonish (garahati)" --k 5

# Subchunk
python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Subchunk --mode bm25   --query "အနိစ္စ" --k 5
python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Subchunk --mode vector --query "အနိစ္စ" --k 5
python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Subchunk --mode hybrid --alpha 0.5 --query "အနိစ္စ" --k 5

# Chunk
python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Chunk --mode bm25   --query "Four Noble Truths" --k 5
python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Chunk --mode vector --query "Four Noble Truths" --k 5
python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Chunk --mode hybrid --alpha 0.5 --query "Four Noble Truths" --k 5

# ---------- Windows PowerShell ----------
# (PowerShell prefers using python .\script.py)
python .\etl\app\search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Sentence --mode bm25   --query "Admonish (garahati)" --k 5
python .\etl\app\search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Sentence --mode vector --query "Admonish (garahati)" --k 5
python .\etl\app\search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Sentence --mode hybrid --alpha 0.5 --query "Admonish (garahati)" --k 5

# ---------- Windows CMD ----------
cd /d D:\tipitaka-poc-starter
python etl\app\search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Window --mode hybrid --alpha 0.5 --query "mettā" --k 5

# ---------- Run inside Docker (no local Python needed) ----------
# (Container-to-container URL သုံးထားပြီး --url http://weaviate:8080)
docker compose run --rm etl python etl/app/search_weaviate_labse_hybridfix.py --url http://weaviate:8080 --grpc-port 50051 --collection Window --mode hybrid --alpha 0.5 --query "mettā" --k 5









## 🚀 Quick Start (recommended)

1) **Clone** this repo and place your `outputs/` under `data/outputs/`  
   – *OR* set the envs below so the container downloads it automatically.

2) **Start everything** in one command:
   ```bash
   ./bootstrap.sh setup
   ```
   This will:
   - Bring up Weaviate
   - Build the ETL image
   - Run the ETL pipeline:
     - wait for Weaviate health
     - create/refresh schema
     - insert CSV for BM25
     - insert vectors for Window/Sentence/Subchunk/Chunk (if files exist)
     - run a tiny sanity search

3) **Search**
   - **GraphQL**: open http://localhost:8080/v1/graphql
   - **CLI** (examples below)


## ⚙️ Environment (defaults & overrides)

`etl/app/pipeline.py` honors the following environment variables (you can set them in `docker-compose.yml` or your shell):

```
WEAVIATE_URL=http://weaviate:8080
WEAVIATE_GRPC_PORT=50051
DATA_DIR=/workspace/data
OUTPUTS_DIR=/workspace/data/outputs
DOWNLOAD_OUTPUTS=0            # set 1 to force download via data/download_folder.py
GOOGLE_DRIVE_FOLDER_ID=       # your Drive folder ID (optional)
```

### Two ways to provide `outputs/`

- **Bind mount (fastest)**: map your host `./data/outputs` into the ETL container at `/workspace/data/outputs`.
- **Download at runtime**: set `DOWNLOAD_OUTPUTS=1` and `GOOGLE_DRIVE_FOLDER_ID=XXXX` and ensure `data/download_folder.py` supports that ID/flags.


## 🐳 Example `docker-compose.yml` (minimal)

> If you already have one, keep it. Otherwise, here is a minimal reference.

```yaml
version: "3.9"
services:
  weaviate:
    image: semitechnologies/weaviate:1.24.10
    restart: unless-stopped
    ports:
      - "8080:8080"
      - "50051:50051"
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: "true"
      DEFAULT_VECTORIZER_MODULE: "none"        # we use offline LaBSE vectors
      CLUSTER_HOSTNAME: "node1"
    volumes:
      - ./weaviate_data:/var/lib/weaviate

  etl:
    build:
      context: .
      dockerfile: etl/Dockerfile.etl
    environment:
      WEAVIATE_URL: "http://weaviate:8080"
      WEAVIATE_GRPC_PORT: "50051"
      DATA_DIR: "/workspace/data"
      OUTPUTS_DIR: "/workspace/data/outputs"
      DOWNLOAD_OUTPUTS: "0"                    # set "1" to download via data/download_folder.py
      GOOGLE_DRIVE_FOLDER_ID: ""               # set if DOWNLOAD_OUTPUTS=1
    volumes:
      - ./data:/workspace/data                 # bind-mount so ETL sees ./data/outputs
    depends_on:
      - weaviate
```


## 🔎 How to search

### A) CLI (inside container via compose)

**Vector / BM25 / HYBRID** (HYBRID requires passing a query vector — this script does it for you):

```bash
# Window (HYBRID) – BM25 + LaBSE vector
docker compose run --rm etl python etl/app/search_weaviate_labse_hybridfix.py \
  --collection Window --mode hybrid --query "four noble truths" --k 5 --alpha 0.5

# Subchunk (vector)
docker compose run --rm etl python etl/app/search_weaviate_labse_hybridfix.py \
  --collection Subchunk --mode vector --query "visuddhimagga" --k 5
```

### B) GraphQL (Browser)

Open **http://localhost:8080/v1/graphql** and paste a query.

**BM25 example**
```graphql
query Bm25Sentence($q: String!) {
  Get {
    Sentence(bm25: { query: $q, properties: ["sentence_text"] }, limit: 5) {
      sentence_id
      sentence_text
      path
      h1 h2 h3 h4
    }
  }
}
```
Variables:
```json
{ "q": "karuṇā" }
```

**Vector example**
```graphql
query VecWindow($vec: [Float!]!) {
  Get {
    Window(nearVector: { vector: $vec }, limit: 5) {
      window_id
      text
      path
      h1 h2 h3 h4
    }
  }
}
```

> To produce `$vec`, run in a terminal:
> ```bash
> python -c "from sentence_transformers import SentenceTransformer;import json; \
> m=SentenceTransformer('sentence-transformers/LaBSE'); \
> v=m.encode(['mettā'],convert_to_numpy=True)[0].astype('float32').tolist(); \
> print(json.dumps(v))"
> ```

**HYBRID example** (vectorizer=none ⇒ you MUST pass a vector)
```graphql
query HybridSub($q: String!, $vec: [Float!]!, $alpha: Float!) {
  Get {
    Subchunk(hybrid: { query: $q, vector: $vec, alpha: $alpha }, limit: 12) {
      subchunk_id
      subchunk_text
      path
    }
  }
}
```
Variables:
```json
{ "q": "patthayamāna", "vec": [/* vector here */], "alpha": 0.5 }
```


## 🧰 Commands (bootstrap)

```bash
./bootstrap.sh setup   # weaviate up → build etl → run pipeline (one shot)
./bootstrap.sh up      # start weaviate only
./bootstrap.sh load    # run ETL pipeline only
./bootstrap.sh logs    # tail weaviate logs
./bootstrap.sh down    # stop & remove containers
```


## 🔄 Updating data

- Replace files under `data/outputs/` and run:
  ```bash
  ./bootstrap.sh load
  ```
- If you changed schema drastically, consider recreating Weaviate state:
  ```bash
  ./bootstrap.sh down
  rm -rf weaviate_data
  ./bootstrap.sh setup
  ```


## ❗ Troubleshooting

- **Hybrid error** `VectorFromInput ... without vectorizer`  
  Your class uses `vectorizer=none`. Hybrid requires both **query text** and **query vector**.  
  Use `search_weaviate_labse_hybridfix.py` (it passes `vector=` for you) or provide a vector in GraphQL.

- **No results from a collection**  
  Likely not inserted. Ensure the corresponding CSV + `*_ids.txt` + `*_labse.npy` exist in `data/outputs/`.

- **Torch / model install issues**  
  The ETL image installs `sentence-transformers` (which pulls PyTorch). On first run it downloads LaBSE.  
  If your environment has no internet, pre-bake a wheel cache or build the image where internet is available.

- **Weaviate not ready / timeout**  
  Check `./bootstrap.sh logs`. Ensure ports `8080` and `50051` are free, and the service can write to `weaviate_data/`.

- **Different host paths**  
  Adjust the `volumes:` mapping in `docker-compose.yml` so the container sees your host `./data/outputs` at `/workspace/data/outputs`.


## 📎 Notes

- We keep **DEFAULT_VECTORIZER_MODULE: none** and **inject vectors offline** (LaBSE).  
- You can switch to built-in vectorizers later by enabling modules in Weaviate and adjusting the schema creation.  
- The ETL respects id consistency (stable UUIDs) if your inserter uses UUIDv5 over your row IDs.

---

Happy searching! 🙏
