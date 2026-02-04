import streamlit as st
from PIL import Image
import io

# Título e Estilo da Página (Igual à imagem que você amou)
st.set_page_config(page_title="Scanner Colorido Pro", page_icon="📄")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    div.stButton > button { width: 100%; border-radius: 15px; height: 3.5em; font-weight: bold; }
    .stTextInput input { background-color: #2D2D2D; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 Scanner Pessoal")

# Memória para guardar as páginas
if 'lista_paginas' not in st.session_state:
    st.session_state.lista_paginas = []

# Campo para dar nome ao arquivo
nome_arquivo = st.text_input("Nome do documento:", "Meu_Documento_01")

# Câmera (Abre automaticamente no celular)
foto = st.camera_input("Tire a foto da folha")

if foto:
    img = Image.open(foto).convert('RGB')
    st.session_state.lista_paginas.append(img)
    st.success(f"Página {len(st.session_state.lista_paginas)} capturada!")

# Mostrar opções se já tiver páginas
if st.session_state.lista_paginas:
    st.info(f"O documento atual tem {len(st.session_state.lista_paginas)} página(s).")
    
    if st.button("🗑️ Limpar tudo e recomeçar"):
        st.session_state.lista_paginas = []
        st.rerun()

    # Botão de Finalizar
    if st.button("✅ Gerar PDF Colorido"):
        pdf_buffer = io.BytesIO()
        primeira = st.session_state.lista_paginas[0]
        outras = st.session_state.lista_paginas[1:]
        
        # Lógica para manter abaixo de 1MB (Reduz qualidade se tiver muitas páginas)
        q = max(15, 85 // len(st.session_state.lista_paginas))
        
        primeira.save(pdf_buffer, format="PDF", save_all=True, append_images=outras, quality=q, optimize=True)
        
        st.download_button(
            label="📥 Baixar PDF Final (Colorido)",
            data=pdf_buffer.getvalue(),
            file_name=f"{nome_arquivo}.pdf",
            mime="application/pdf"
        )
