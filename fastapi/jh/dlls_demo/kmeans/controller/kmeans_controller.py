import os
import sys

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from kmeans.service.kmeans_service_impl import KMeansServiceImpl

kMeansRouter = APIRouter()

async def injectKMeansService() -> KMeansServiceImpl:
    return KMeansServiceImpl()

@kMeansRouter.post("/kmeans-game")
async def requestKMeans(kMeansService: KMeansServiceImpl =
                       Depends(injectKMeansService)):

    kMeansResponse = await kMeansService.requestProcess()

    return kMeansResponse
