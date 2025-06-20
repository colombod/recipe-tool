# This file was generated by Codebase-Generator, do not edit directly
import os
import time
import logging
from typing import Optional, List, Type, Union, Dict, Any

from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.models.openai import OpenAIModel, OpenAIResponsesModel, OpenAIResponsesModelSettings
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.mcp import MCPServer

from openai.types.responses import WebSearchToolParam, FileSearchToolParam

from recipe_executor.llm_utils.azure_openai import get_azure_openai_model
from recipe_executor.llm_utils.responses import get_openai_responses_model
from recipe_executor.llm_utils.azure_responses import get_azure_responses_model
from recipe_executor.protocols import ContextProtocol


def get_model(
    logger: logging.Logger, model_id: str, context: ContextProtocol
) -> Union[OpenAIModel, AnthropicModel, OpenAIResponsesModel]:
    """
    Initialize an LLM model based on a standardized model_id string.
    Expected formats:
      - 'provider/model_name'
      - 'provider/model_name/deployment_name'

    Supported providers:
      - openai
      - azure
      - anthropic
      - ollama
      - openai_responses
      - azure_responses

    Raises:
        ValueError: If model_id format is invalid or provider unsupported.
    """
    parts = model_id.split("/")
    if len(parts) < 2:
        raise ValueError(f"Invalid model_id format: '{model_id}'")
    provider = parts[0].lower()
    config = context.get_config()

    # OpenAI
    if provider == "openai":
        if len(parts) != 2:
            raise ValueError(f"Invalid OpenAI model_id: '{model_id}'")
        model_name = parts[1]
        api_key = config.get("openai_api_key")
        provider_obj = OpenAIProvider(api_key=api_key)
        return OpenAIModel(model_name=model_name, provider=provider_obj)

    # Azure OpenAI
    if provider == "azure":
        # azure/model_name or azure/model_name/deployment_name
        if len(parts) == 2:
            model_name, deployment = parts[1], None
        elif len(parts) == 3:
            model_name, deployment = parts[1], parts[2]
        else:
            raise ValueError(f"Invalid Azure model_id: '{model_id}'")
        return get_azure_openai_model(
            logger=logger,
            model_name=model_name,
            deployment_name=deployment,
            context=context,
        )

    # Anthropic
    if provider == "anthropic":
        if len(parts) != 2:
            raise ValueError(f"Invalid Anthropic model_id: '{model_id}'")
        model_name = parts[1]
        api_key = config.get("anthropic_api_key")
        provider_obj = AnthropicProvider(api_key=api_key)
        return AnthropicModel(model_name=model_name, provider=provider_obj)

    # Ollama
    if provider == "ollama":
        if len(parts) != 2:
            raise ValueError(f"Invalid Ollama model_id: '{model_id}'")
        model_name = parts[1]
        base_url = config.get("ollama_base_url") or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        provider_obj = OpenAIProvider(base_url=f"{base_url}/v1")
        return OpenAIModel(model_name=model_name, provider=provider_obj)

    # OpenAI Responses API
    if provider == "openai_responses":
        if len(parts) != 2:
            raise ValueError(f"Invalid OpenAI Responses model_id: '{model_id}'")
        model_name = parts[1]
        return get_openai_responses_model(logger, model_name)

    # Azure Responses API
    if provider == "azure_responses":
        # azure_responses/model_name or azure_responses/model_name/deployment_name
        if len(parts) == 2:
            model_name, deployment = parts[1], None
        elif len(parts) == 3:
            model_name, deployment = parts[1], parts[2]
        else:
            raise ValueError(f"Invalid Azure Responses model_id: '{model_id}'")
        return get_azure_responses_model(logger, model_name, deployment)

    raise ValueError(f"Unsupported LLM provider: '{provider}' in model_id '{model_id}'")


class LLM:
    """
    Unified interface for interacting with various LLM providers
    and optional MCP servers.
    """

    def __init__(
        self,
        logger: logging.Logger,
        context: ContextProtocol,
        model: str = "openai/gpt-4o",
        max_tokens: Optional[int] = None,
        mcp_servers: Optional[List[MCPServer]] = None,
    ):
        self.logger: logging.Logger = logger
        self.context: ContextProtocol = context
        self.default_model_id: str = model
        self.default_max_tokens: Optional[int] = max_tokens
        self.default_mcp_servers: List[MCPServer] = mcp_servers or []

    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        output_type: Type[Union[str, BaseModel]] = str,
        mcp_servers: Optional[List[MCPServer]] = None,
        openai_builtin_tools: Optional[List[Dict[str, Any]]] = None,
    ) -> Union[str, BaseModel]:
        """
        Generate an output from the LLM based on the provided prompt.
        """
        model_id = model or self.default_model_id
        tokens = max_tokens if max_tokens is not None else self.default_max_tokens
        servers = mcp_servers if mcp_servers is not None else self.default_mcp_servers

        provider_name = model_id.split("/", 1)[0]
        self.logger.info(
            "LLM generate using provider=%s model_id=%s",
            provider_name,
            model_id,
        )

        output_name = getattr(output_type, "__name__", str(output_type))
        self.logger.debug(
            "LLM request prompt=%r model_id=%s max_tokens=%s output_type=%s mcp_servers=%s",
            prompt,
            model_id,
            tokens,
            output_name,
            [type(s).__name__ for s in servers],
        )

        try:
            model_instance = get_model(self.logger, model_id, self.context)
        except ValueError as err:
            self.logger.error("Invalid model_id '%s': %s", model_id, err)
            raise

        agent_kwargs: Dict[str, Any] = {
            "model": model_instance,
            "output_type": output_type,
            "mcp_servers": servers,
        }
        # Responses API with built-in tools
        if provider_name in ("openai_responses", "azure_responses") and openai_builtin_tools:
            typed_tools: List[Union[WebSearchToolParam, FileSearchToolParam]] = []
            for tool in openai_builtin_tools:
                try:
                    typed_tools.append(WebSearchToolParam(**tool))
                except TypeError:
                    typed_tools.append(FileSearchToolParam(**tool))
            settings = OpenAIResponsesModelSettings(openai_builtin_tools=typed_tools)
            agent_kwargs["model_settings"] = settings
        # max_tokens for other models
        elif tokens is not None:
            agent_kwargs["model_settings"] = ModelSettings(max_tokens=tokens)

        agent: Agent = Agent(**agent_kwargs)  # type: ignore

        start = time.time()
        try:
            async with agent.run_mcp_servers():
                result = await agent.run(prompt)
        except Exception as err:
            self.logger.error(
                "LLM call failed model_id=%s error=%s",
                model_id,
                err,
            )
            raise
        end = time.time()

        duration = end - start
        try:
            usage = result.usage()
        except Exception:
            usage = None

        if usage:
            self.logger.info(
                "LLM result time=%.3f sec requests=%d tokens_total=%d (req=%d res=%d)",
                duration,
                usage.requests,
                usage.total_tokens,
                usage.request_tokens,
                usage.response_tokens,
            )
        else:
            self.logger.info(
                "LLM result time=%.3f sec (usage unavailable)",
                duration,
            )

        self.logger.debug("LLM raw result data=%r", result.data)

        return result.output
