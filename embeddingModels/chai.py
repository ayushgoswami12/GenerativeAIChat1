from dotenv import load_dotenv

load_dotenv()

# from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq

model = ChatGroq(model="groq/compound-mini")
# temperature 0 to 1 , 0 => facts  , 1 => creativity 

response = model.invoke("Analyse good stocks for today and give me 3 stock names ? ") 
print(response.content)
