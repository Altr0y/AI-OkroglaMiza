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

# Frontend - Next.js vzpostavitev projekta

## Ukazi za namestitev in zagon v razvojnem načinu:
```bash
npm i
npm run dev
```

Spletno mesto dostopno na: http://localhost:3000


## Build projekta in zagon:
```bash
npm run build
npm start
```
