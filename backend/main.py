import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Uvozimo routerje (ekvivalent Flask Blueprintom)
from routers import ai_router, health_router

app = FastAPI(
    title="AI Okrogla Miza API",
    description="Samodejno generirana dokumentacija za hibridni backend.",
    version="1.0.0",
    docs_url="/apidocs"  # Swagger bo na isti poti, kot si imel v Flasku
)

# << dodaj ta del za konfiguracijo CORS

# CORS omogoči Streamlitu dostop do API-ja - bbrskalniki po defaultu prepovedujejo strani na portu 8000, da komunicira s portom 8001 recimo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registracija poti (ekvivalent blueprintom)
app.include_router(health_router, prefix="/api")
app.include_router(ai_router, prefix="/api")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)