import openai
from supabase import create_client
import streamlit as st
import io

# Configuração dos clientes
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
openai.api_key = st.secrets["OPENAI_API_KEY"]

def transcrever_audio(audio_bytes):
    """Envia o áudio para a API do Whisper (OpenAI) e recebe o texto."""
    # Transforma os bytes em um arquivo que a API entende
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.wav"
    
    transcript = openai.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcript.text

def buscar_venda(query):
    # Lógica de busca no Supabase (como vimos antes)
    response = supabase.table("produtos").select("*").ilike("nome", f"%{query}%").execute()
    return str(response.data)

def responder_jarvis(comando_texto):
    contexto = buscar_venda(comando_texto)
    prompt = f"Você é o Jarvis. Use estes dados: {contexto}. Responda: {comando_texto}"
    
    resposta = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Você é Jarvis."},
                  {"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content
