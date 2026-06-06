from dotenv import load_dotenv 

load_dotenv()

from langchain_groq import ChatGroq 
from langchain_core.messages import AIMessage , SystemMessage, HumanMessage
messages_hisrtory = [
    
    SystemMessage(content= "you are stock market analyst ")
] 
model = ChatGroq(model= "openai/gpt-oss-120b")
while True : 
    prompt1 = input("You : ")
    messages_hisrtory.append(HumanMessage(content=prompt1))
    response = model.invoke( messages_hisrtory)
    
    if prompt1 =="exit" :
        break 
    
    print( "Bot : " ,response.content)
    messages_hisrtory.append(AIMessage(content=response.content))
    
print(messages_hisrtory)