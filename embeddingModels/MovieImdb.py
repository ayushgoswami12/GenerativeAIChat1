from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

# Schema
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str
    

parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Extract Movie Information From the paragraph.
            
            If the input contains only a movie title (and optionally a year),
            identify the movie and fill as many fields as possible. 

            {format_instructions}
            """,
        ),
        ("human", "{paragraph}"),
    ]
)

para = input("Give me paragraph: ")

final_prompt = prompt.invoke(
    {
        "paragraph": para,
        "format_instructions": parser.get_format_instructions(),
    }
)

model = ChatGroq(model="groq/compound-mini")
#new coding
response = model.invoke(final_prompt)

print(response.content)