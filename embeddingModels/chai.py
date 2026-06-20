from dotenv import load_dotenv
from pydantic import BaseModel 
from typing import List , Optional 
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
#This is schema 
class Movie(BaseModel) :
    title : str 
    release_year : Optional[int]
    genre : List[str]
    director : Optional[str]
    cast : List[str]
    rating : Optional[float]
    summary :  str 
     
    
parser = PydanticOutputParser(pydantic_object = Movie)
prompt = ChatPromptTemplate.messages(
    
)

load_dotenv()

# from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq

model = ChatGroq(model="groq/compound-mini")
#added to git 
# temperature 0 to 1 , 0 => facts  , 1 => creativity 

response = model.invoke("Analyse good stocks for today and give me 3 stock names ? ") 
print(response.content)
#made some chagnes  