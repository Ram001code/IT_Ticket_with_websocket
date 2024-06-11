import asyncio
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from langchain.llms import OpenAI  # Use your preferred LLM provider
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from prompt import get_llm_chain, memory    # get_llm_chain: is llm chain model
from proc import get_final_output    #returning after parsing


# Global memory for all WebSocket connections
# memory = ConversationBufferMemory(max_length=10)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    """Request model for both API and WebSocket requests."""
    message: str

# WebSocket endpoint
@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    username = await websocket.receive_text()  # Get username
    await websocket.send_text(f"Welcome, {username}!")

    # llm = OpenAI()  # Create LLM for each connection
    # chain = LLMChain({"llm": llm, "prompt": "Respond to the following:"})

    try:
        while True:
            message = await websocket.receive_text()
            data = ChatRequest(message=message)  # Validate incoming message
            response = await get_llm_chain.call({"input": data.message})
            # memory.update(response)  # Update global memory
            final_output = get_final_output(response)
            await websocket.send_text(final_output)
    except websockets.ConnectionClosed:
        pass

# API endpoint for non-WebSocket requests
# @app.post("/chat")
# async def chat(data: ChatRequest):  # Use ChatRequest model for validation
#     llm = OpenAI()  # Create LLM for each API request
#     chain = LLMChain({"llm": llm, "prompt": "Respond to the following:"})
#     response = await chain.call({"input": data.message, "memory": memory})
#     memory.update(response)  # Update global memory
#     return response  # Return the response as an API response

if __name__ =="__main__":
    uvicorn.run(app)
