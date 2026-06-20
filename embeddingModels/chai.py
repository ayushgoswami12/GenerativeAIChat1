from dotenv import load_dotenv
from pydantic import BaseModel 
from typing import List , Optional 

#This is schema 
class Movie(BaseModel) :
    title : str 
    release_year : Optional[int]
    genre : List[str]
    director : Optional[str]
    cast : List[str]
    rating : Optional[float]
    summary :  str 
     
    


load_dotenv()

# from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq

model = ChatGroq(model="groq/compound-mini")
#added to git 
# temperature 0 to 1 , 0 => facts  , 1 => creativity 

response = model.invoke("Analyse good stocks for today and give me 3 stock names ? ") 
print(response.content)
#made some chagnes  