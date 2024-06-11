import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import asyncio
from prompt import get_llm_chain
from proc import get_final_output

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
    """Request model for QA requests.
    Includes the question from the user.
    """
    message: str

# Store chat history separately from connections
chat_history: Dict[str, List[str]] = {}

# Store messages in connections
connections: Dict[str, str] = {}

@app.post("/send_message/{email_id}")
async def send_message(email_id: str, request: ChatRequest, background_tasks: BackgroundTasks):
    message = request.message
    # Store message in the connections dictionary
    connections[email_id] = message
    # Append the message to the chat history
    if email_id not in chat_history:
        chat_history[email_id] = [message]
        
    else:
        chat_history[email_id].append({"User": message})
        #chat_history[email_id].append({"LLM": final_output["answer"]})
    # Process the message in the background
    background_tasks.add_task(process_message, email_id, message)
    # Directly return the response from the LLM
    llm_chain = get_llm_chain()  # Assuming this function loads your LLM model
    output = llm_chain.predict(description=message)
    final_output = get_final_output(output)  # Assuming this function processes the output
    chat_history[email_id].append({"LLM": final_output})
    history = chat_history.get(email_id, [])
    #return {"email_id": email_id, "chat_history": history}
    return {"chat_history": history}

    #return final_output


async def process_message(email_id: str, message: str):
    # Simulate processing time
    await asyncio.sleep(2)
    print(f"Message from {email_id}: {message}")


#@app.get("/chat_history/{email_id}")
#async def get_chat_history(email_id: str):
 #   # Retrieve the chat history for the specified email ID
  #  history = chat_history.get(email_id, [])
   # return {"email_id": email_id, "chat_history": history}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
