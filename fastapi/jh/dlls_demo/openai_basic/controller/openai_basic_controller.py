import os
import sys

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from typing import Any

from openai_basic.controller.request_form.openai_talk_request_form import OpenAITalkRequestForm
from openai_basic.service.openai_basic_service_impl import OpenAIBasicServiceImpl

openAiBasicRouter = APIRouter()

async def injectOpenAIBasicService() -> OpenAIBasicServiceImpl:
    return OpenAIBasicServiceImpl()

@openAiBasicRouter.post("/openai/lets-talk")
async def talkWithOpenAI(openAITalkRequestForm: OpenAITalkRequestForm,
                         openAIBasicService: OpenAIBasicServiceImpl =
                         Depends(injectOpenAIBasicService)):

    print(f"OpenAI Basic Controller -> talkWithOpenAI(): openAITalkRequestForm: {openAITalkRequestForm}")

    openAiGeneratedText = await openAIBasicService.letsTalk(openAITalkRequestForm.userSendMessage)

    return JSONResponse(content=openAiGeneratedText, status_code=status.HTTP_200_OK)

@openAiBasicRouter.post("/openai/audio-analysis")
async def audioAnalysisWithOpenAI(file: UploadFile = File(...),
                                  openAIBasicService: OpenAIBasicServiceImpl =
                                  Depends(injectOpenAIBasicService)):

    analyzedAudio = await openAIBasicService.audioAnalysis(file)

    return JSONResponse(content=analyzedAudio, status_code=status.HTTP_200_OK)
