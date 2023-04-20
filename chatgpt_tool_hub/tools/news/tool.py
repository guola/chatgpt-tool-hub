from typing import Any

from chatgpt_tool_hub.bots import initialize_bot
from chatgpt_tool_hub.engine import ToolEngine
from chatgpt_tool_hub.models import build_model_params
from chatgpt_tool_hub.models.model_factory import ModelFactory
from chatgpt_tool_hub.tools.all_tool_list import main_tool_register
from chatgpt_tool_hub.tools.base_tool import BaseTool
from chatgpt_tool_hub.tools.load_tools import load_tools
from chatgpt_tool_hub.tools.news import news_tool_register

default_tool_name = "news"


class NewsTool(BaseTool):
    name: str = default_tool_name
    description: str = (
        "Useful when you want to get information about current news stories, "
        "such as financial news, daily morning reports and any other news. "
        "The input should be a description of your needs in natural language."
    )
    bot: ToolEngine = Any

    def __init__(self, **tool_kwargs: Any):
        # 这个工具直接返回内容
        super().__init__(return_direct=True)

        tools = load_tools(news_tool_register.get_registered_tool_names(), news_tool_register, **tool_kwargs)
        llm = ModelFactory().create_llm_model(**build_model_params(tool_kwargs))

        self.bot = initialize_bot(tools, llm, bot="qa-bot", verbose=True,
                                  max_iterations=2, early_stopping_method="force")

    def _run(self, query: str) -> str:
        """Use the tool."""
        if not query:
            return "the input of tool is empty"
        if not self.bot:
            return "the tool was not initialized"

        # todo should connect to parent bot
        return self.bot.run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("NewsTool does not support async")


main_tool_register.register_tool(default_tool_name, lambda kwargs: NewsTool(**kwargs), [])
