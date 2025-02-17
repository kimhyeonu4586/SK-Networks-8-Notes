import os
import sys

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from ensemble_method.service.ensemble_method_service_impl import EnsembleMethodServiceImpl

ensembleMethodRouter = APIRouter()

async def injectEnsembleMethodService() -> EnsembleMethodServiceImpl:
    return EnsembleMethodServiceImpl()

@ensembleMethodRouter.post("/ensemble-method")
async def requestEnsembleMethod(ensembleMethodService: EnsembleMethodServiceImpl =
                                Depends(injectEnsembleMethodService)):

    ensembleMethodResponse = await ensembleMethodService.ensembleMethod()

    return ensembleMethodResponse
