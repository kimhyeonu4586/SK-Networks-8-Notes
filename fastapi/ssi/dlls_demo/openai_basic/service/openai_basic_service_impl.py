from pathlib import Path

from openai_basic.repository.openai_basic_repository_impl import OpenAIBasicRepositoryImpl
from openai_basic.service.openai_basic_service import OpenAIBasicService


class OpenAIBasicServiceImpl(OpenAIBasicService):

    def __init__(self):
        self.__openAiBasicRepository = OpenAIBasicRepositoryImpl()

    async def letsTalk(self, userSendMessage):
        return await self.__openAiBasicRepository.generateText(userSendMessage)

    async def audioAnalysis(self, file):
        return await self.__openAiBasicRepository.audioAnalysis(file)

    async def text_to_speech(self, text: str, file_path: Path):
        await self.__openAiBasicRepository.convert_text_to_speech(text, file_path)