import streamlit as st
from streamlit_audiorec import st_audiorec
from jarvis_logic import transcrever_audio, responder_jarvis, gerar_audio

st.title("🤖 Jarvis - Assistente de Vendas")

# Captura de áudio
audio_bytes = st_audiorec()

if audio_bytes is not None:
    st.audio(audio_bytes, format="audio/wav")
    
    with st.spinner("Processando..."):
        try:
            # 1. Transcreve
            texto_comando = transcrever_audio(audio_bytes)
            st.write(f"Você disse: {texto_comando}")
            
            # 2. Lógica de ativação
            if "jarvis" in texto_comando.lower():
                resposta = responder_jarvis(texto_comando)
                st.success(f"Jarvis: {resposta}")
                
                # 3. Gera voz
                caminho_audio = gerar_audio(resposta)
                st.audio(caminho_audio)
            else:
                st.warning("Jarvis não foi ativado. Diga 'Jarvis' no início.")
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
