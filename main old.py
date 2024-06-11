import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket,WebSocketDisconnect
from prompt import get_llm_chain
from proc import get_final_output
# from websockets import serve, WebSocketServerProtocol
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from typing import Dict

import time
import json

RESET_MEMORY = False


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


# @app.post("/chat")
# async def chat(data: ChatRequest):
#     global RESET_MEMORY
#     message = data.message
#     if not message:
#         RESET_MEMORY = True
#     try:
#         llm_chain = get_llm_chain(RESET_MEMORY)
#         output = llm_chain.predict(description=message)
#         #final_output = {"output": output}
#         final_output = get_final_output(output)
        
#         # ticket_number = final_output["ticket_number"]
#         # ticket_number = final_output.get("ticket_number", 0)  # Default to 0 if "is_order" is not present

#         def checkword(myout, word):
#             for key, value in myout.items():
#                 if isinstance(value, str):
#                     for match in word:
#                         if match.lower() in value.lower():
#                             return True
#             return False
#         myout= final_output
#         word= ['Ticket Number']
#         result= checkword(myout, word)
       
#         if result== True:
#            time.sleep(30)
#            RESET_MEMORY = True
#         else:
#            RESET_MEMORY = False

#         return final_output
    
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail=str(e))

# templates= Jinja2Templates(directory="templates")

# @app.get("/", response_class= HTMLResponse)
# async def get(request: Request):
#     return templates.TemplateResponse("chat.html", {"request": request})


connections: Dict[str, WebSocket] = {}

# client_id
@app.websocket("/ws/{Email_id}/{First_nam}/{Last_name}")
async def websocket_endpoint(websocket: WebSocket, Email_id: str, First_nam:str, Last_name: str ):
    await websocket.accept()
    # Emply_id= '1245'

    connections[Email_id] = websocket
    try:
        while True:
            message = await websocket.receive_text()
            # data = json.loads(message)
            # data = ChatRequest(data)  # Validate incoming message
            # llm_chain = get_llm_chain(RESET_MEMORY)
            # query = data['message']
            llm_chain = get_llm_chain()
            output = llm_chain.predict(description=message)
            # print(type(output))
            # final_output = {"output": output}
            final_output = get_final_output(output)
            # s_data = {'message':output}
            await websocket.send_json(final_output)
            # await websocket.send_json(client_id)

    except WebSocketDisconnect:
        del connections[Email_id]
        

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, ws_ping_timeout=None)    