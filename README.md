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


Happy searching! 🙏
