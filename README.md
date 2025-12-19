    Docker!

    Podpora za lokalne GGUF modele (preko llama-cpp) in direktne HuggingFace modele (preko transformers).


⚡ Program najbolje izvedemo na lightning ai cloud VM, za študente zastonj. Imajo močne GPU-je, prilagojeni za webappe in AI. Ob registraciji uporabite šolski mail. V novem studiu v terminal kopirajte projekt.
Postopek zagona:

    Odprite nov Studio na Lightning AI.

    V terminal kopirajte projekt (Git clone).

    Zaženite ukaz:
    Bash

    docker compose up --build

    Čas nalaganja: Zagon aplikacije vzame približno 5 minut. Vsi agenti se morajo zaporedno naložiti v VRAM. Spremljaj loge v terminalu; ko vidiš Uvicorn running, je sistem pripravljen.

    Dostop: Lightning AI ne odpre avtomatsko portov v brskalniku. Uporabiti moraš Port Viewer plugin na desni strani ekrana studia in izbrati port 5501.

📂 Nalaganje in dodajanje modelov
1. Prenos GGUF modelov (kompresiran format)

Modele shranjujemo v mapo models/. Za prenos uporabi wget neposredno v terminalu studia:
Bash

cd AI-OkroglaMiza/models && wget https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-uncensored-GGUF/resolve/main/Llama-3.2-3B-Instruct-uncensored-Q4_K_M.gguf

2. Dodajanje agentov v kodo

Nove agente registrirate v datoteki backend/config.py.

Primer za Transformers model (Qwen3):
Python

{
    "id": "qwen3",
    "name": "🤖 Qwen3-0.6B",
    "type": "transformers",
    "model_path": "Qwen/Qwen3-0.6B",
}

Primer za specializiranega programerja (EssentialAI):
Python

{
    "id": "Fast code",
    "name": "Fast code",
    "model_id": "EssentialAI/rnj-1-instruct",
    "default_system": ("Ti si vrhunski programer in arhitekt programske opreme z 20 leti izkušenj. "
                       "Tvoj cilj je pisati čisto, učinkovito in varno kodo, ki je pripravljena za produkcijo. "
                       "Tvoja pravila: Piši kodo, ki je modularna; vključi jedrnate komentarje; "
                       "uporabljaj najnovejše knjižnice; odgovori neposredno s kodo."),
    "is_gguf": False
},

🛠 Tehnične podrobnosti

    Porti: Backend teče na 5000, Frontend na 5501.

    Docker Volumes: Mapa ./models prenešeni modeli ostanejo shranjeni tudi po ponovnem zagonu studia.














# AI-OkroglaMiza

# QuickStart guide!

## 1. Kloniraj repo v lokalno mašino:
```bash
git clone https://github.com/Altr0y/AI-OkroglaMiza
cd AI-OkroglaMiza
```

## 2. Preklopi na razvojno vejo
```bash
git checkout dev
git pull
```

## 3. Ustvari novi "feature" vejo kjer boš implementiral svoje
```bash
git checkout -b feature/ID-opis
git push -u origin feature/ID-opis
```

## 4. Delaj svoje funkcionalnosti
```bash
git add .
git commit -m "Opis spremembe"
git push
```

### 4.1 Zagon celega projekta

Iz roota projekta:
```bash
docker compose up # opcijsko -d (v ozadju)
# na nekaterih sistemih docker-compose
```

Backend ima podporo za avtomatski reload z:
```bash
docker compose watch
```

### 4.2 Swagger dokumentacija za backend
```bash
http://localhost:5000/apidocs/
```

## 5. odpri PR (Pull request)
```bash
Na GitHubu izberi:
base: dev
compare: tvoj feature branch
Ustvari PR
```

# Pravila:
-> Za merge v dev ni potreben approval.
-> Za merge v main je obvezen 1 approval.

## Posodobi lokalni repozitorij na zadnjo verzijo

Če že imaš repozitorij na računalniku, ga lahko posodobiš na zadnje stanje z GitHub-a:

```bash
git checkout dev     # preklopi na glavno razvojno vejo
git pull             # potegni zadnje spremembe iz GitHub-a
```

Hvala lepa in želim uspešno programiranje!
