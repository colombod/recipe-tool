# This file was generated by Codebase-Generator, do not edit directly
import os
import logging
from typing import Any, Dict, List, Optional

from pydantic_ai.mcp import MCPServer, MCPServerHTTP, MCPServerStdio

# Optional .env support
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # type: ignore

__all__ = ["get_mcp_server"]


def get_mcp_server(logger: logging.Logger, config: Dict[str, Any]) -> MCPServer:
    """
    Create an MCPServer client based on the provided configuration.

    Args:
        logger: Logger for logging messages.
        config: Configuration for the MCP server.

    Returns:
        A configured PydanticAI MCPServer instance.

    Raises:
        ValueError: If the configuration is invalid.
        RuntimeError: On errors creating the server instance.
    """
    if not isinstance(config, dict):
        raise ValueError("MCP server configuration must be a dict")

    # Mask sensitive info for logging
    sensitive = {"api_key", "apikey", "authorization", "auth", "token", "secret", "password"}
    masked: Dict[str, Any] = {}
    for key, value in config.items():
        low = key.lower()
        if low in sensitive:
            masked[key] = "***"
        elif key in ("headers", "env") and isinstance(value, dict):
            masked[key] = {k: "***" for k in value}
        else:
            masked[key] = value
    logger.debug("MCP server configuration: %s", masked)

    # HTTP(S) transport
    if "url" in config:
        url = config.get("url")
        if not isinstance(url, str) or not url.strip():
            raise ValueError("HTTP MCP server requires a non-empty 'url' string")

        headers = config.get("headers")
        if headers is not None and not isinstance(headers, dict):
            raise ValueError("HTTP MCP server 'headers' must be a dict if provided")

        tool_prefix = config.get("tool_prefix")
        if tool_prefix is not None and not isinstance(tool_prefix, str):
            raise ValueError("HTTP MCP server 'tool_prefix' must be a string if provided")

        logger.info("Creating HTTP MCP server for URL: %s", url)
        try:
            http_kwargs: Dict[str, Any] = {"url": url}
            if headers is not None:
                http_kwargs["headers"] = headers
            if tool_prefix is not None:
                http_kwargs["tool_prefix"] = tool_prefix
            return MCPServerHTTP(**http_kwargs)
        except Exception as exc:
            raise RuntimeError(f"Failed to create HTTP MCP server: {exc}") from exc

    # Stdio transport
    if "command" in config:
        command = config.get("command")
        if not isinstance(command, str) or not command.strip():
            raise ValueError("Stdio MCP server requires a non-empty 'command' string")

        args_cfg = config.get("args")
        if not isinstance(args_cfg, list) or not all(isinstance(a, str) for a in args_cfg):
            raise ValueError("Stdio MCP server 'args' must be a list of strings")
        args: List[str] = args_cfg  # type: ignore

        # Environment variables
        env_cfg = config.get("env")
        env: Optional[Dict[str, str]] = None
        if env_cfg is not None:
            if not isinstance(env_cfg, dict):
                raise ValueError("Stdio MCP server 'env' must be a dict if provided")
            # load .env if any value is empty and dotenv is available
            if load_dotenv and any(v == "" for v in env_cfg.values()):  # type: ignore
                load_dotenv()  # type: ignore
            env = {}
            for k, v in env_cfg.items():
                if not isinstance(v, str):
                    raise ValueError(f"Environment variable '{k}' must be a string")
                if v == "":
                    sys_val = os.getenv(k)
                    if sys_val is not None:
                        env[k] = sys_val
                else:
                    env[k] = v

        # Working directory (cwd or alias working_dir)
        cwd = config.get("cwd")
        if cwd is None:
            cwd = config.get("working_dir")
        if cwd is not None and not isinstance(cwd, str):
            raise ValueError("Stdio MCP server 'cwd' must be a string if provided")

        tool_prefix = config.get("tool_prefix")
        if tool_prefix is not None and not isinstance(tool_prefix, str):
            raise ValueError("Stdio MCP server 'tool_prefix' must be a string if provided")

        logger.info("Creating stdio MCP server with command: %s %s", command, args)
        try:
            stdio_kwargs: Dict[str, Any] = {"command": command, "args": args}
            if cwd is not None:
                stdio_kwargs["cwd"] = cwd
            if env is not None:
                stdio_kwargs["env"] = env
            if tool_prefix is not None:
                stdio_kwargs["tool_prefix"] = tool_prefix
            return MCPServerStdio(**stdio_kwargs)
        except Exception as exc:
            raise RuntimeError(f"Failed to create stdio MCP server: {exc}") from exc

    # No valid transport found
    raise ValueError("Invalid MCP server configuration: must contain 'url' for HTTP or 'command' for stdio transport")
