from app.api.recommendations import router as recommendations_router

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.tenants import router as tenant_router
from app.api.companies import router as company_router
from app.api.company_signals import router as company_signal_router
from app.api.icp_profiles import router as icp_profiles_router


app = FastAPI(
    title="Decision Maker AI",
    version="0.3.0",
    description="AI decision intelligence platform for B2B revenue teams.",
)


@app.get("/")
def root():
    return {
        "service": "Decision Maker AI",
        "version": "0.3.0",
        "status": "running",
    }


app.include_router(auth_router)
app.include_router(tenant_router)
app.include_router(icp_profiles_router)
app.include_router(company_router)
app.include_router(company_signal_router)


app.include_router(recommendations_router)
