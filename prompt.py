import os
import openai
#import chromadb
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessagePromptTemplate,MessagesPlaceholder


os.environ["OPENAI_API_TYPE"] = openai.api_type = "azure"
os.environ["OPENAI_API_VERSION"] = openai.api_version = "2023-03-15-preview" #"2022-12-01" 
os.environ["OPENAI_API_BASE"] = openai.api_base =  ""
os.environ["OPENAI_API_KEY"] = openai.api_key = ""#os.getenv("AZUREOPENAI_API_KEY")

embeddings = AzureOpenAIEmbeddings(deployment="")


from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import FewShotChatMessagePromptTemplate
from langchain import PromptTemplate, LLMChain


model = AzureChatOpenAI(
        openai_api_base="",
        openai_api_version="2023-03-15-preview",
        deployment_name='',
        openai_api_key="",
        openai_api_type="azure",
        temperature=0
        )


from langchain.memory import ConversationBufferMemory


memory = ConversationBufferMemory()

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI


from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI



Template = """You are an AI assistant for IT support team. 
Your primary job is to infer title, description and category from user input and create the ticket.
Do the following steps:

1. Don't send any greet message if user is talking about issue.
2. Ask for the issue details.
3. Infer title,description and category.
4. title,description and category should be clear to you. In case if you won't able to infer title,description and category then you should ask for more details regarding issue.
5. Get the confirmation from user by saying "Thanks for the details. Below is your details." Mention the issue details in the structured format and ask the user "Please confirm if I can go ahead and create a ticket with the mentioned details.
6.Once user confirms then return the message "Thanks for confirming! I'll cretae a ticket with following issue details." and issue details in JSON format. 
7. Your output should be specific to user input. Think wisely before providing any output.
8. Don't create ticket for the same issue again and again.




User input: {description}


LLM Output: Thanks for the details, I'll create a ticket for you !!


"""


prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=Template
        ),  # The persistent system prompt
        MessagesPlaceholder(
            variable_name="chat_history"
        ),  # Where the memory will be stored.
        HumanMessagePromptTemplate.from_template(
            "{description}"
        ),  # Where the human input will injected
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)



def get_llm_chain(reset_memory):
    if reset_memory:
        memory.clear()
    chat_llm_chain = LLMChain(
    llm=model,
    prompt=prompt,
    verbose=True,
    memory=memory,
    )

    return chat_llm_chain
    


