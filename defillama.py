from typing import Any
import httpx
import json
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio

# Initialize FastMCP server
mcp = FastMCP("defillama-mcp")
app = FastAPI()

# Constants
DEFI_API_BASE = "https://api.llama.fi"
COIN_API_BASE = "https://coins.llama.fi"
USER_AGENT = "DEFI-APP/1.0"

@mcp.tool()
async def get_protocols() -> dict[Any, Any]:
    """Get all protocols from defillama.

    Args:
    """
    url = f"{DEFI_API_BASE}/protocols"
    data = await make_request(url)

    return data[:20]

@mcp.tool()
async def get_protocol_tvl(protocol: str) -> dict[Any, Any]:
    """ Get a defi protocol tvl from defillama
    Args:
        protocol: protocol name
    """
    url = f"{DEFI_API_BASE}/protocol/{protocol}"
    data = await make_request(url)
    return data["currentChainTvls"]

@mcp.tool()
async def get_chain_tvl(chain: str) -> dict[Any, Any]:
    """ Get a chain's tvl

    Args:
        chain: chain name
    """
    url = f"{DEFI_API_BASE}/v2/historicalChainTvl/{chain}"
    data = await make_request(url)
    return data[:30]

@mcp.tool()
async def get_token_prices(token: str) -> dict[Any, Any]:
    """ Get a token's price
    Args:
        token: token name
    """
    url = f"{COIN_API_BASE}/prices/current/{token}"
    data = await make_request(url)
    return data


async def make_request(url: str) -> dict[str, Any] | None:
    """Make a request to the API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def sse_stream(request: Request):
    try:
        while True:
            if await request.is_disconnected():
                break      
            protocols = await get_protocols()
            if protocols:  # Make sure we have data to send
                yield f"data: {json.dumps(protocols)}\n\n"
            else:
                yield f"data: {json.dumps({'status': 'no data available'})}\n\n"
            
            await asyncio.sleep(1)  # 每秒发送一次数据
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


@app.get("/sse")
async def sse_endpoint(request: Request):
    return StreamingResponse(
        sse_stream(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
            "Access-Control-Allow-Origin": "*",  # Allow CORS for SSE
        },
    )



@app.get("/api/protocols")
async def api_protocols():
    return await get_protocols()

@app.get("/api/protocol/{protocol}")
async def api_protocol_tvl(protocol: str):
    return await get_protocol_tvl(protocol)

@app.get("/api/chain/{chain}")
async def api_chain_tvl(chain: str):
    return await get_chain_tvl(chain)

@app.get("/api/token/{token}")
async def api_token_prices(token: str):
    return await get_token_prices(token)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8080,
        log_level="info",
        timeout_keep_alive=65,  
    )
    #mcp.run(transport='stdio')