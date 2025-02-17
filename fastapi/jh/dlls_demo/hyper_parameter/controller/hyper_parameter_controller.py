import os
import sys

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from hyper_parameter.service.hyper_parameter_service_impl import HyperParameterServiceImpl

hyperParameterRouter = APIRouter()

async def injectHyperParameterService() -> HyperParameterServiceImpl:
    return HyperParameterServiceImpl()

@hyperParameterRouter.post("/hyper-parameter-test")
async def requestGradientDescent(hyperParameterService: HyperParameterServiceImpl =
                                 Depends(injectHyperParameterService)):

    hyperParameterResponse = await hyperParameterService.requestProcess()

    return hyperParameterResponse
