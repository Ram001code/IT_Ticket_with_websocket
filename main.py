import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from prompt import get_llm_chain
from proc import get_final_output
import time

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



@app.post("/chat")
async def chat(data: ChatRequest):
    global RESET_MEMORY
    message = data.message
    if not message:
        RESET_MEMORY = True
    try:
        llm_chain = get_llm_chain(RESET_MEMORY)
        output = llm_chain.predict(description=message)
        #final_output = {"output": output}
        final_output = get_final_output(output)
        
        # ticket_number = final_output["ticket_number"]
        # ticket_number = final_output.get("ticket_number", 0)  # Default to 0 if "is_order" is not present

        def checkword(myout, word):
            for key, value in myout.items():
                if isinstance(value, str):
                    for match in word:
                        if match.lower() in value.lower():
                            return True
            return False
        myout= final_output
        word= ['Ticket Number']
        result= checkword(myout, word)
       
        if result== True:
           time.sleep(30)
           RESET_MEMORY = True
        else:
           RESET_MEMORY = False

        return final_output
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    uvicorn.run(app)    