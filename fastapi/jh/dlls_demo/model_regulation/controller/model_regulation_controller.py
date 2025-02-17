import os
import sys

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from model_regulation.service.model_regulation_service_impl import ModelRegulationServiceImpl

modelRegulationRouter = APIRouter()

async def injectModelRegulationService() -> ModelRegulationServiceImpl:
    return ModelRegulationServiceImpl()

@modelRegulationRouter.post("/model-regulation-test")
async def requestModelRegulation(modelRegulationService: ModelRegulationServiceImpl =
                                 Depends(injectModelRegulationService)):

    modelRegulationResponse = await modelRegulationService.requestProcess()

    return modelRegulationResponse
