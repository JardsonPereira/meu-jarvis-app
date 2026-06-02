import streamlit as st
from supabase import create_client
from openai import OpenAI
from gtts import gTTS
import io

# Inicializa o cliente OpenAI de forma segura
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Inicializa o Supabase de forma segura
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def transcrever_audio(audio_bytes):
    """Envia o áudio para a API do Whisper (OpenAI)."""
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.wav"
    
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcript.text

def responder_jarvis(comando_texto):
    """Lógica da IA consultando o banco."""
    # Busca simplificada (exemplo)
    response = supabase.table("produtos").select("nome, descricao").limit(5).execute()
    contexto = str(response.data)
    
    prompt = f"Você é o Jarvis. Use estes dados de estoque: {contexto}. Responda à pergunta: {comando_texto}"
    
    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Você é Jarvis, especialista em logística."},
                  {"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content

def gerar_audio(texto):
    """Cria o arquivo de áudio."""
    tts = gTTS(text=texto, lang='pt', slow=False)
    arquivo = "resposta.mp3"
    tts.save(arquivo)
    return arquivo
