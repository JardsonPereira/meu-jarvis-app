import streamlit as st
from st_audiorec import st_audiorec
import openai
from jarvis_logic import processar_venda_inteligente, criar_audio_resposta

st.title("🤖 Jarvis - Assistente de Vendas")

# Botão de Ativação
if st.button("Ativar Jarvis"):
    st.write("Jarvis: O que posso fazer por você, senhor?")
    # Toca o áudio de saudação (opcional: gere um mp3 fixo para isso)
    
    # Captura de Áudio
    audio_data = st_audiorec()
    
    if audio_data is not None:
        st.audio(audio_data, format='audio/wav')
        
        # Aqui você enviaria o arquivo para o Whisper Transcribe
        # (Omitindo transcrição complexa para manter simples, 
        # mas você usaria openai.Audio.transcribe(audio_file))
        
        # Simulação da entrada de texto do Jarvis
        texto_comando = "Venda de notebook" # Substitua pela transcrição real
        
        with st.spinner("Jarvis está pensando..."):
            resposta_texto = processar_venda_inteligente(texto_comando)
            st.success(resposta_texto)
            
            # Gera áudio da resposta
            arquivo_audio = criar_audio_resposta(resposta_texto)
            st.audio(arquivo_audio)
