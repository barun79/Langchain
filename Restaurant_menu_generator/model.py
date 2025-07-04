from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain , SequentialChain
import streamlit as st
import os


# Set OpenRouter endpoint
try:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
except Exception:
    from secret_key import API_KEY 
    os.environ["OPENAI_API_KEY"] = API_KEY

os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

def generate_restaurant_data(cusine: str, tone: str):
    # Use a model that's available as free on OpenRouter
    llm = ChatOpenAI(
        model="mistralai/mistral-7b-instruct:free",
        temperature=0.7
    )

    # Name chain
    name_prompt = PromptTemplate(
        input_variables=["cusine"],
        template = "Suggest a creative name for {cusine} resturant. Only return the name, nothing else."
    )
    name_chain = LLMChain(llm = llm, prompt = name_prompt, output_key = "restaurant_name")

    # Description chain

    des_prompt = PromptTemplate(
        input_variables=["restaurant_name", "tone"],
        template = "Write a short, {tone} description for a restaurant named '{restaurant_name}'."
    )
    des_chain = LLMChain(llm = llm, prompt= des_prompt, output_key = "description")

    # Menu chain

    menu_prompt = PromptTemplate(
        input_variables=["restaurant_name", "cusine"],
        template = "Suggest 5 popular {cusine} dishes for a restaurant called '{restaurant_name}'. Format as a list."
    )
    menu_chain = LLMChain(llm = llm, prompt = menu_prompt, output_key= "menu")

    # Slogan

    slogan_prompt = PromptTemplate(
        input_variables = ["restaurant_name", "tone"],
        template = "Create a short and {tone} slogan for a restaurant called '{restaurant_name}'."
    )
    slogan_chain = LLMChain(llm=llm, prompt=slogan_prompt, output_key="slogan")

    # Combine chain

    full_chain = SequentialChain(
        chains = [name_chain, des_chain, menu_chain, slogan_chain],
        input_variables = ["cusine", "tone"],
        output_variables = ["restaurant_name", "description", "menu", "slogan"],
        verbose = True
    )

    return full_chain.invoke({"cusine": cusine, "tone": tone})