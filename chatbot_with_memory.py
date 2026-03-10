#%%
from langgraph.graph import  StateGraph,START,END,add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langchain_ollama.chat_models import  ChatOllama
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage,BaseMessage
from typing_extensions import Literal,List,TypedDict,Annotated

llm=ChatOllama(model='llama3.1:8b')

class ChatState(TypedDict):
    messages:Annotated[List[BaseMessage],add_messages]

def Chatbot(state:ChatState):
    messages=state['messages']
    response=llm.invoke(messages)
    return {'messages':[response]}

conn=sqlite3.connect('chat.db',check_same_thread=False)
checkpoint=SqliteSaver(conn=conn)

config={'configurable':{'thread_id':'1'}}

build=StateGraph(ChatState)
build.add_node('chatbot',Chatbot)
build.add_edge(START,'chatbot')
build.add_edge('chatbot',END)
graph=build.compile(checkpointer=checkpoint)

result=graph.invoke({'messages':HumanMessage(content='My name is Yash')},config=config)


#%%
print(result['messages'][0])
#%%

#%%
