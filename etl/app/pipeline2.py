import os
import sys
import subprocess
from pathlib import Path

print("cwd =", os.getcwd())

sys.path.append(os.path.join(os.getcwd(), 'etl', 'app'))

from clean_text import clean_text_all_files
from chunk_split import run_pipeline

def main():
    print(f"cwd = {os.getcwd()}")

    # [1/4] Cleaning raw data files
    print("[1/5] Cleaning raw data files...")
    input_folder = "data/raw"
    cleaned_output_folder = os.path.join("data", "outputs", "cleaned_text")
    os.makedirs(cleaned_output_folder, exist_ok=True)

    clean_text_all_files(
        input_folder=input_folder,
        output_folder=cleaned_output_folder,
        suffix="_cleaned.txt"
    )

    # [2/4] Splitting cleaned files into chunks/subchunks/sentences/windows
    print("[2/5] Splitting cleaned files into chunks/subchunks/sentences/windows...")
    for fname in os.listdir(cleaned_output_folder):
        if not fname.endswith('_cleaned.txt'):
            continue

        input_cleaned_file = os.path.join(cleaned_output_folder, fname)
        file_stem = os.path.splitext(fname)[0]           # e.g., "mn5chunk_cleaned"
        base_name = file_stem.replace('_cleaned', '')    # e.g., "mn5chunk"
        outdir_for_this_file = os.path.join("data", "outputs", f"{base_name}_chunk_split")
        os.makedirs(outdir_for_this_file, exist_ok=True)

        print(f"⏳ Splitting chunks for {fname}")
        run_pipeline(
            input_txt=input_cleaned_file,
            out_chunks=os.path.join(outdir_for_this_file, 'chunks.csv'),
            out_subchunks=os.path.join(outdir_for_this_file, 'subchunks_200.csv'),
            out_sentences=os.path.join(outdir_for_this_file, 'sentences_from_200.csv'),
            out_windows=os.path.join(outdir_for_this_file, 'windows_2_3.csv'),
            prefix="MAIN",
            id_width=3,
            chunk_size=8000,
            sub_size=200,
            tokenizer="whitespace"
        )

    # [3/4] Check for .md files and run Markdown heading parser
    print("[3/5] Checking for .md file and running Markdown parser if available...")
    md_files = list(Path("data/raw").glob("*.md"))
    if not md_files:
        print("⏭️ No .md file found in data/raw. Skipping heading parse and join.")
        return  # ✅ inside main()

    for md_file in md_files:
        base_filename = md_file.stem  # e.g., "MN5chunk-heading" or "tipitaka1"
        out_folder_hd_parse = f"data/outputs/{base_filename}_hd_parse"

        print(f"⏳ Parsing headings from: {md_file}")
        subprocess.run([
            sys.executable, "etl/app/md_headings_parse.py",
            "--input", str(md_file),
            "--outdir", out_folder_hd_parse
        ], check=True)
        print(f"✅ Parsed headings saved to: {out_folder_hd_parse}")

        # [4/4] Join layers
        print("[4/5] Joining all layers with Markdown heading tokens...")

        heading_units_csv = os.path.join(out_folder_hd_parse, "units_sentences_with_tokens.csv")
        if not os.path.exists(heading_units_csv):
            print("[!] No headings parse units found. Skipping join.")
            continue  # ✅ inside the loop

        chunk_split_name = base_filename.replace("-heading", "")
        chunk_split_dir = os.path.join("data/outputs", f"{chunk_split_name}_chunk_split")

        out_folder_join = f"{base_filename}_join_headings_by_tokens"
        os.makedirs(os.path.join("data/outputs", out_folder_join), exist_ok=True)

        join_args = [
            sys.executable, "etl/app/join_headings_by_tokens.py",
            "--units", heading_units_csv,
            "--sentences", os.path.join(chunk_split_dir, "sentences_from_200.csv"),
            "--windows", os.path.join(chunk_split_dir, "windows_2_3.csv"),
            "--subchunks", os.path.join(chunk_split_dir, "subchunks_200.csv"),
            "--chunks", os.path.join(chunk_split_dir, "chunks.csv"),
            "--outdir", os.path.join("data/outputs", out_folder_join)
        ]

        subprocess.run(join_args, check=True)
        print(f"✅ Joined headings → data/outputs/{out_folder_join}")

        # [5/5] Create LaBSE vectors from _with_headings CSVs
        print("[5/5] Creating LaBSE vectors from _with_headings CSVs...")

        # base name ကို md_file.stem ကနေ ယူ
        base_name = base_filename.replace("-heading", "")
        out_embed_dir = os.path.join("data", "outputs", f"{base_name}_labse_embeddings")
        os.makedirs(out_embed_dir, exist_ok=True)

        vectorize_args = [
            sys.executable, "etl/app/make_labse_embeddings.py",
            "--sentences", os.path.join("data/outputs", f"{base_filename}_join_headings_by_tokens", "sentences_with_headings.csv"),
            "--windows", os.path.join("data/outputs", f"{base_filename}_join_headings_by_tokens", "windows_with_headings.csv"),
            "--subchunks", os.path.join("data/outputs", f"{base_filename}_join_headings_by_tokens", "subchunks_with_headings.csv"),
            "--chunks", os.path.join("data/outputs", f"{base_filename}_join_headings_by_tokens", "chunks_with_headings.csv"),
            "--outdir", out_embed_dir   # 👈 အသစ် ထည့်မယ်
        ]

        subprocess.run(vectorize_args, check=True)
        print(f"[✓] LaBSE vectors saved to {out_embed_dir}")


if __name__ == "__main__":
    main()
