import os
import sys
from pathlib import Path

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

@openAiBasicRouter.post("/openai/text-to-sound")
async def text_to_sound(openAITalkRequestForm: OpenAITalkRequestForm,
                        openAIBasicService: OpenAIBasicServiceImpl =
                        Depends(injectOpenAIBasicService)):

    print(f"OpenAI Basic Controller -> text_to_sound(): openAITalkRequestForm: {openAITalkRequestForm}")

    # 텍스트를 음성 파일로 변환
    speech_file_path = Path("speech.mp3")
    try:
        await openAIBasicService.text_to_speech(openAITalkRequestForm.userSendMessage, speech_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"음성 변환 중 오류 발생: {str(e)}")

    # 생성된 음성 파일 반환
    return FileResponse(speech_file_path, media_type="audio/mpeg", filename="speech.mp3")