import os

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
