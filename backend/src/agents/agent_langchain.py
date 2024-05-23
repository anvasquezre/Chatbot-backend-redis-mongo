from typing import Any, List

from core.dtos.messages_dto import BaseMessageDto
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.chains.base import Chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from pydantic import ConfigDict
from src.agents.agent_base import AgentBase
from src.agents.prompts import HISTORY_TEMPLATE, SYSTEM_TEMPLATE
from src.agents.tools import (
    CurrentWeatherSearchToolByLatLong,
    ForecastWeatherSearchTool,
    GetCoordinatesByLocationName,
)
from utils.settings import settings


class LangchainAgent(AgentBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    langchain_agent_executor: Any  # AgentExecutor , Pydantic throws error when using AgentExecutor in the type hint

    def format_text_to_input(self, text: str) -> dict:
        return {"input": text}

    def execute(self, text: str, message_history: List[BaseMessageDto]) -> str:
        message_history_str = self.format_message_history(message_history)
        text = f"{message_history_str}\n{text}"
        inputs = self.format_text_to_input(text)
        executor: AgentExecutor = self.langchain_agent_executor
        response = executor.invoke(inputs)
        response = response["output"]
        return response

    def format_message_history(self, message_history: List[BaseMessageDto]) -> str:
        if not message_history:
            return ""
        message_string = ""
        for message in message_history:
            role = message.role
            content = message.content
            individual_message = f"Role: {role}, Content: {content}\n\n"
            message_string += individual_message
        final_message = HISTORY_TEMPLATE.format(**{"message_history": message_string})
        return final_message

    async def aexecute(self, text: str, message_history: List[BaseMessageDto]) -> str:
        message_history_str = self.format_message_history(message_history)
        text = f"{message_history_str}\n{text}"
        inputs = self.format_text_to_input(text)
        executor: AgentExecutor = self.langchain_agent_executor
        response = await executor.ainvoke(inputs)
        response = response["output"]
        return response

    @classmethod
    def create(cls) -> "LangchainAgent":
        tools = [
            CurrentWeatherSearchToolByLatLong(),
            ForecastWeatherSearchTool(),
            GetCoordinatesByLocationName(),
        ]

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_TEMPLATE),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        llm = ChatOpenAI(
            api_key=settings.OPENAI.OPENAI_API_KEY.get_secret_value(),
            # model="gpt-4o-2024-05-13",
            model="gpt-3.5-turbo-0125",
            temperature=0,
        )

        llm_with_tools = llm.bind_tools(tools=tools)

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | OpenAIToolsAgentOutputParser()
        )
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        return cls(langchain_agent_executor=agent_executor)
