import os
import sys

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from gradient_descent.service.gradient_descent_service_impl import GradientDescentServiceImpl

gradientDescentRouter = APIRouter()

async def injectGradientDescentService() -> GradientDescentServiceImpl:
    return GradientDescentServiceImpl()

@gradientDescentRouter.post("/gradient-descent-test")
async def requestGradientDescent(gradientDescentService: GradientDescentServiceImpl =
                                 Depends(injectGradientDescentService)):

    gradientDescentResponse = await gradientDescentService.requestProcess()

    return gradientDescentResponse
