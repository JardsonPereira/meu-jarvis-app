import streamlit as st
from supabase import create_client
from openai import OpenAI
from gtts import gTTS
import io

# Inicialização segura
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
openai_key = st.secrets["OPENAI_API_KEY"]

supabase = create_client(url, key)
client = OpenAI(api_key=openai_key)

def transcrever_audio(audio_bytes):
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.wav"
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcript.text

def responder_jarvis(comando_texto):
    # Busca dados no Supabase
    response = supabase.table("produtos").select("nome, descricao").limit(5).execute()
    contexto = str(response.data)
    
    prompt = f"Você é o Jarvis. Use estes dados de estoque: {contexto}. Responda ao cliente: {comando_texto}"
    
    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Você é Jarvis, especialista em logística."},
                  {"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content

def gerar_audio(texto):
    tts = gTTS(text=texto, lang='pt', slow=False)
    arquivo = "resposta.mp3"
    tts.save(arquivo)
    return arquivo
