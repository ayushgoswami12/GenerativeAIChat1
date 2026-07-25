from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq 
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

model = ChatGroq(model='openai/gpt-oss-120b')
parser = StrOutputParser()


short_message = PromptTemplate.from_template(
    "Give {answer} in 1 words"
)
detailed_message = PromptTemplate.from_template(
    "Give {answer} in 100 words"
)
answer = "machine learning "
runnables = RunnableParallel({
   "short": short_message | model | parser , 
    "Long Answer" :detailed_message | model | parser
})

response = runnables.invoke({"answer" : "machine learning "})
print(response)