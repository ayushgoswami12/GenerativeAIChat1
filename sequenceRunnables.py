from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq 
from langchain_core.prompts import  ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

#1 prompt 
prompt = ChatPromptTemplate.from_messages([
    (     
    "system" ,
    """
    You are helpful assistant , you keep your answer short by default (around 30 - 70 words)
    
    Only give long answer if the user wants detailed, long format , or long answers and in long you can go upto 200 words but dont extend it to 500 or more 
    """
    ),
    ('human',"{input}")
    ]
    #you can also do chatpromptTemplate.from_template 
    
    
 )
# prompt = ChatPromptTemplate.from_template(
#     "Explain {topic} in simple words  in 50 words , only extend if user wants long answer "
# )

#2 model 
model = ChatGroq(model='openai/gpt-oss-120b')


#Output Parser      
parser = StrOutputParser()

runnables  = prompt | model | parser

response = runnables.invoke(" Machine learning  in long format ? ")

print(response)