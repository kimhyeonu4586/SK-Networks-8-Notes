import os
import sys

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from mnist.service.mnist_service_impl import MnistServiceImpl

mnistRouter = APIRouter()

async def injectMnistService() -> MnistServiceImpl:
    return MnistServiceImpl()

@mnistRouter.post("/mnist-test")
async def requestMnist(mnistService: MnistServiceImpl =
                       Depends(injectMnistService)):

    mnistResponse = await mnistService.requestProcess()

    return mnistResponse
