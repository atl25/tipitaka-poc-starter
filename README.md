# Tipitaka POC Starter – One‑Click ETL + Search


1. project file အား download လုပ်ပါ။

- tipitaka-poc-starter ကို နှိပ်ပါ။ Code--> Open with GitHub Desktop -->မိမိသိမ်းလိုသည့် loacl file path ကို ရွေးချယ်ပြီး ဖိုင်ကိုသိမ်းပါ။

2. Docker Desktop ကို ဖွင့်ပါ

3. Docker မှာ အသုံးပြုနိုင်အောင် ပြင်ဆင်ခြင်း။
- ./bootstrap.sh setup ကို run ပါ။
- gitbash (or) power shall ကို ဖွင့်ပါ -cd tipitaka-poc-starter ./bootstrap.sh setup ကို run ပါ။
[gitbash (or) power shall တွင် မိမိ project file သိမ်းထားသော loacl file path ကို ရွေးပေးပါ. eg.cd "C:\Users\user\Desktop\tipitaka-poc-starter"]

4. စာရှာခြင်း
- gitbash, power shall, window teminal, doker terminal ကြိုက်နှစ်သက်ရာတွင် ရှာနိုင်သည်။
- project file ထည့်သွင်းထားသော် location ကိုပြောင်းပါ။

-python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Window --mode bm25 --query "mettā" --k 5

-python etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Window --mode vector --query "mettā" --k 5 python

-etl/app/search_weaviate_labse_hybridfix.py --url http://localhost:8080 --grpc-port 50051 --collection Window --mode hybrid --alpha 0.5 --query "mettā" --k 5

--collection တွင် Window, Sentence, Subchunk, Chunk ပြောင်းလဲ ရှာနိုင်သည်။

--mode တွင် bm25, vector, hybrid --alpha 0.5 ပြောင်းလဲရှာနိုင်သည်။

--query "metta" တွင် " "ဒီမှာ ရှာလိုသော စကားလုံးထည့်နိုင်သည်။

--k 5 တွင် 1 to 20 အထိ ရလဒ်အခုအရေအတွက် ပြောင်းလဲကြည့်နိုင်သည။


Happy searching! 🙏
