import os
from pathlib import Path

import httpx
import openai

from fastapi import HTTPException
from config.openai_config import OpenAIConfig
from openai_basic.repository.openai_basic_repository import OpenAIBasicRepository


class OpenAIBasicRepositoryImpl(OpenAIBasicRepository):
    SIMILARITY_TOP_RANK = 3

    OpenAIConfig.loadConfig()
    api_key = OpenAIConfig.get_api_key()

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    templateQuery = """You are a helpful assistant.
        {question}
        Provide a detailed answer to the above question."""

    OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
    OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"

    async def generateText(self, userSendMessage):
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": userSendMessage}
            ]
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.OPENAI_CHAT_COMPLETIONS_URL, headers=self.headers, json=data)
                response.raise_for_status()

                return response.json()['choices'][0]['message']['content'].strip()

            except httpx.HTTPStatusError as e:
                print(f"HTTP Error: {str(e)}")
                print(f"Status Code: {e.response.status_code}")
                print(f"Response Text: {e.response.text}")
                raise HTTPException(status_code=e.response.status_code, detail=f"HTTP Error: {e}")

            except (httpx.RequestError, ValueError) as e:
                print(f"Request Error: {e}")
                raise HTTPException(status_code=500, detail=f"Request Error: {e}")

    async def audioAnalysis(self, audioFile):
        try:
            file_location = f"tmp_{audioFile.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(audioFile.file.read())

            with open(file_location, "rb") as file:
                transcript = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=file
                )

            os.remove(file_location)
            print(f"transcript: {transcript}")

            return transcript.text

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"에러 발생: {str(e)}")

    async def convert_text_to_speech(self, text: str, file_path: Path):
        """
        OpenAI TTS API를 호출하여 텍스트를 음성으로 변환하고 파일로 저장
        """
        try:
            print("Starting text-to-speech conversion...")
            response = openai.audio.speech.create(
                model="tts-1",  # 최신 TTS 모델
                voice="alloy",  # 원하는 음성 선택 (다양한 음성 옵션 있음)
                input=text
            )
            print(f"Response received from OpenAI: {response}")

            # 응답의 'content' 속성에서 음성 파일 데이터 추출
            audio_data = response.content
            print(f"Audio data length: {len(audio_data)} bytes")

            # 음성 파일을 지정된 경로에 저장
            with open(file_path, "wb") as audio_file:
                print(f"Saving audio to {file_path}")
                audio_file.write(audio_data)
            print(f"Audio saved successfully at {file_path}")

        except Exception as e:
            print(f"Error in TTS conversion: {e}")
            raise Exception(f"음성 변환 중 오류 발생: {str(e)}")

