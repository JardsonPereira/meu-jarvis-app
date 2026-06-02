import os
import openai
from supabase import create_client
from gtts import gTTS
import streamlit as st

# Configuração dos clientes
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
openai.api_key = st.secrets["OPENAI_API_KEY"]

def buscar_contexto_no_supabase(query):
    # Exemplo: busca simples em uma tabela de produtos
    response = supabase.table("produtos").select("nome, descricao, preco").ilike("nome", f"%{query}%").execute()
    return str(response.data)

def processar_venda_inteligente(comando_usuario):
    # 1. Busca contexto no banco
    contexto = buscar_contexto_no_supabase(comando_usuario)
    
    # 2. IA gera a resposta
    prompt = f"""Você é o Jarvis, um consultor de logística. 
    Responda o cliente de forma profissional e persuasiva. 
    Use estes dados de estoque: {contexto}.
    Pergunta do cliente: {comando_usuario}"""
    
    resposta = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Você é o Jarvis, especialista em vendas."},
                  {"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content

def criar_audio_resposta(texto):
    tts = gTTS(text=texto, lang='pt', slow=False)
    arquivo_audio = "resposta.mp3"
    tts.save(arquivo_audio)
    return arquivo_audio
