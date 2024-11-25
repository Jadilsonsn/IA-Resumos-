
# Ferramentas utilizadas >>  LangChain, Pandas e OPENAI, Streamlit
from langchain.agents.agent_types import AgentType 
from langchain_experimental.agents import create_pandas_dataframe_agent 
from langchain_openai import ChatOpenAI 
import pandas as pd  
import openpyxl
import streamlit as st
from dotenv import load_dotenv
import os

#Variáveis de ambiente 
load_dotenv() 
api_key_chat = os.getenv("api_key") 
openai_organization_ap = os.getenv("openai_organization") 

# CARREGAR DATAFRAME 
st.set_page_config(page_title="assistente",page_icon="bird")  
df = None
with st.sidebar:
    st.subheader("Carregue seu arquivo")
    dados = st.file_uploader("Files",type=['xlsx'])
    
    if dados is not None:
        df = pd.read_excel(dados)
        

if df is not None:



# Dados da OPENAI 
 llm = ChatOpenAI(model ="gpt-3.5-turbo-0125",
                   temperature=0,
                   api_key = api_key_chat,
                   openai_organization = openai_organization_ap) 


# Template 
 agent_prompt_prefix = """
Você é o InsightSphere, 
um assistente virtual especializado em DataFrames Pandas.
Sua função é responder perguntas sobre o df com precisão, utilizando estratégias alternativas para lidar com dados desafiadores, como valores nulos, caracteres especiais e dados incompletos.
Responda apenas a perguntas relacionadas ao df, evitando informações falsas e priorizando a qualidade e a relevância.

 """

# Criação do agente
 agent = create_pandas_dataframe_agent(
    llm,
    df,
    prefix=agent_prompt_prefix,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS
 )



# STREAMLIT APP 

st.title("Analises de :blue[DataFrames]")  
pergunta = st.text_input("Experimente fazer uma pergunta: ",
           placeholder=" Digite uma pergunta ou comando ")
if pergunta: 
 resposta =  agent.invoke(pergunta)
 st.write(resposta.get("output")) 

