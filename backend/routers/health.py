from fastapi import APIRouter
import torch
import psutil
import os
from typing import Dict, Any

router = APIRouter(tags=["Zdravje"])

@router.get("/health", response_model=Dict[str, Any])
async def health_check():
    """
    Preprost health check za preverjanje pripravljenosti in diagnostiko.
    
    Vrne:
        - status: "ok" (kot v starem blueprintu)
        - gpu: Informacije o dostopnosti CUDA
        - system: Poraba CPU in RAM
    """
    gpu_available = torch.cuda.is_available()
    
    # Pridobivanje podatkov o sistemu
    memory = psutil.virtual_memory()
    
    return {
        "status": "ok",  # Ohranjen ključ iz tvojega starega Flask blueprinta
        "diagnostics": {
            "gpu": {
                "available": gpu_available,
                "name": torch.cuda.get_device_name(0) if gpu_available else "N/A",
                "vram_allocated_gb": f"{torch.cuda.memory_allocated(0) / 1024**3:.2f}" if gpu_available else "0"
            },
            "system": {
                "cpu_usage_percent": psutil.cpu_percent(),
                "ram_usage_percent": memory.percent,
                "pid": os.getpid()
            }
        }
    }