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

#### GPU Konfiguracija

Projekt podpira NVIDIA, AMD in CPU-only konfiguracije. Nastavi spremenljivke v `.env` datoteki ali jih eksportiraj:

**Za NVIDIA GPU:**
```bash
export GPU_DRIVER=nvidia
export GPU_COUNT=1  # ali število GPU-jev ki jih želiš uporabiti
```
V `docker-compose.yml` komentiraj sekcijo `devices` (vrstice z `/dev/kfd` in `/dev/dri`).

**Za AMD GPU:**
```bash
export GPU_DRIVER=  # prazno ali sploh ne nastavi
export GPU_COUNT=0  # ali sploh ne nastavi
```
V `docker-compose.yml` pusti sekcijo `devices` odkomentirano.

**Za CPU-only (brez GPU):**
```bash
export GPU_DRIVER=none
export GPU_COUNT=0
```
V `docker-compose.yml` komentiraj sekcijo `devices`.

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
