# DeFiLlama MCP

<p align="center">
  <img src="https://raw.githubusercontent.com/llama-community/defillama-assets/main/defillama-logo.png" alt="DeFiLlama MCP Logo" width="200" height="auto"/>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)

## Overview

DeFiLlama MCP is a powerful and flexible tool that provides a microservice-based API wrapper around the DeFi Llama ecosystem. It leverages the FastMCP framework to transform DeFi Llama's comprehensive DeFi data into easily accessible tool endpoints that can be integrated with various AI applications, including LLM agents and autonomous systems.

This project serves as a bridge between the rich data sources provided by DeFi Llama and the emerging needs of AI-driven applications in the Web3 space. By wrapping DeFi Llama's APIs in a standardized MCP (Microservice Communication Protocol) format, developers can quickly integrate real-time DeFi data into their AI systems without dealing with the complexities of direct API integration.

## Features

- **Protocol Data Access**: Retrieve comprehensive information about DeFi protocols including TVL (Total Value Locked) metrics.
- **Blockchain Analytics**: Access historical TVL data for specific blockchains to analyze trends and growth patterns.
- **Token Price Tracking**: Fetch current price information for various tokens across multiple chains.
- **Liquidity Pool Data**: Get detailed insights into liquidity pools, including TVL and other critical metrics.
- **Standardized Interface**: All data is accessible through a consistent API pattern, making it easy to integrate with AI systems.
- **Docker Support**: Ready-to-deploy containerization for easy implementation in any environment.
- **Server-Sent Events**: Real-time data updates using SSE transport mechanism.

## Architecture

DeFiLlama MCP is built using a modular architecture that separates the data-fetching logic from the API interface. The core components include:

1. **API Clients**: Specialized HTTP clients for each of DeFi Llama's API endpoints (Main, Coins, Yields).
2. **MCP Tools**: Function-based tools that transform raw API responses into structured data for consumption by AI agents.
3. **FastMCP Server**: A lightweight server that exposes the tools via HTTP and SSE (Server-Sent Events).
4. **Error Handling**: Robust error management to ensure reliability even when upstream services experience issues.

## Installation

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) (Python package installer and environment manager)

### Option 1: Local Installation

```bash
# Clone the repository
git clone https://github.com/demcp/defillama-mcp.git
cd defillama-mcp

# Create a virtual environment and install dependencies
uv venv
uv pip install -e .

# Run the server
uv run defillama.py
```

### Option 2: Docker Installation

```bash
# Clone the repository
git clone https://github.com/demcp/defillama-mcp.git
cd defillama-mcp

# Build the Docker image
docker build -t defillama-mcp .

# Run the container
docker run -p 8080:8080 defillama-mcp
```

## Usage

Once the server is running, it exposes several endpoints that can be used to interact with DeFi Llama data:

### Available Tools

- `get_protocols`: Retrieve information about top DeFi protocols.
- `get_protocol_tvl`: Get TVL data for a specific protocol.
- `get_chain_tvl`: Access historical TVL data for a specific blockchain.
- `get_token_prices`: Obtain current price information for specific tokens.
- `get_pools`: List available liquidity pools.
- `get_pool_tvl`: Get detailed information about a specific liquidity pool.

### Example: Using with Python

```python
import httpx

# Query the MCP server for protocol data
async def get_protocol_data(protocol_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8080/tools/get_protocol_tvl",
            json={"protocol": protocol_name}
        )
        return response.json()

# Usage
import asyncio
result = asyncio.run(get_protocol_data("aave"))
print(result)
```

### Example: Using with LangChain

```python
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

# Load DeFiLlama MCP tools
tools = load_tools(["defillama-mcp"], base_url="http://localhost:8080")

# Initialize an agent with the tools
llm = OpenAI(temperature=0)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Run the agent
agent.run("What is the current TVL of Uniswap?")
```

### Example: Using with Autonomous Agents

```python
from autogen import Agent, ConversableAgent

financial_analyst = ConversableAgent(
    name="FinancialAnalyst",
    llm_config={
        "tools": [
            {
                "name": "defillama_protocol_tvl",
                "url": "http://localhost:8080/tools/get_protocol_tvl"
            }
        ]
    }
)

# The agent can now access DeFi data during its reasoning process
financial_analyst.initiate_chat("Analyze the TVL trends for Aave protocol")
```

## API Reference

### GET /protocols

Returns a list of DeFi protocols tracked by DeFi Llama.

**Response:**
```json
[
  {
    "id": "ethereum:0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9",
    "name": "Aave",
    "symbol": "AAVE",
    "chain": "Ethereum",
    "tvl": 6240000000
  },
  ...
]
```

### POST /tools/get_protocol_tvl

Get TVL information for a specific protocol.

**Request:**
```json
{
  "protocol": "aave"
}
```

**Response:**
```json
{
  "ethereum": 3240000000,
  "polygon": 980000000,
  "avalanche": 570000000,
  "optimism": 450000000,
  "arbitrum": 1000000000,
  "total": 6240000000
}
```

### POST /tools/get_chain_tvl

Get historical TVL data for a blockchain.

**Request:**
```json
{
  "chain": "ethereum"
}
```

**Response:**
```json
[
  {
    "date": "2023-01-01",
    "tvl": 28500000000
  },
  {
    "date": "2023-01-02",
    "tvl": 28700000000
  },
  ...
]
```

## Contributing

Contributions are welcome! Here's how you can help improve DeFiLlama MCP:

1. **Fork the Repository**: Create your own fork of the project.
2. **Create a Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Your Changes**: `git commit -m 'Add some amazing feature'`
4. **Push to the Branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**: Submit your changes for review.

### Development Guidelines

- Follow PEP 8 style guidelines for Python code.
- Write tests for new features.
- Update documentation to reflect changes.
- Ensure backward compatibility when possible.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [DeFi Llama](https://defillama.com/) for providing the comprehensive DeFi data APIs.
- The [FastMCP](https://github.com/mcpai/fastmcp) team for creating the microservice framework.
- All contributors who have helped shape this project.

## Roadmap

- [ ] Add support for more DeFi Llama endpoints
- [ ] Implement caching layer for improved performance
- [ ] Develop authentication and rate limiting
- [ ] Create detailed documentation site
- [ ] Build example integrations with popular AI frameworks
- [ ] Add metric collection and monitoring

## Contact

For questions, suggestions, or discussions about this project, please open an issue on GitHub or contact the maintainers:

- GitHub Issues: [https://github.com/demcp/defillama-mcp/issues](https://github.com/demcp/defillama-mcp/issues)

---

<p align="center">Built with ❤️ for the Web3 and AI communities</p>

```shell
uv run defillama.py
```
