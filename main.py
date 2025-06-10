from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI
from langserve import add_routes

load_dotenv()

model = Ollama(model="llama3.1:8b", temperature=0.1)

system_prompt = "Translate the following into {language}."
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt), ("user", "{text}")
    ]
)

parser = StrOutputParser()

chain = prompt_template | model | parser # prompt -> model -> parser
# This chain takes a language and text, translates the text into the specified language using the Ollama model, and returns the translated text.

app = FastAPI(
    title="Ollama Translation API",
    description="An API for translating text using the Ollama model.",
    version="1.0.0"
)

add_routes(app, chain, path="/chain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)