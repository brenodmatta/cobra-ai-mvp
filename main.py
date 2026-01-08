import streamlit as st
import google.generativeai as genai
import os

# 1. Configuração Visual da Página
st.set_page_config(page_title="COBRA.AI - Recuperação Estratégica", layout="wide")
st.title("🐍 COBRA.AI - Sistema de Recuperação de Crédito")

# 2. Conexão com o Cérebro (Gemini)
# A API KEY será configurada no servidor por segurança
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

# 3. Interface de Dados (O que o usuário preenche)
with st.sidebar:
    st.header("Dados do Caso")
    nome = st.text_input("Nome do Cliente")
    valor = st.number_input("Valor Devido (R$)", min_value=0.0, format="%.2f")
    atraso = st.number_input("Dias em Atraso", min_value=0)
    canal = st.selectbox("Canal de Saída", ["WhatsApp", "Telefone", "E-mail"])
    estagio = st.selectbox("Estágio", ["Lembrete", "1ª Cobrança", "Reescalonamento", "Aviso Final"])

situacao = st.text_area("O que o devedor disse agora? (Relato da Situação)")

if st.button("DISPARAR ESTRATÉGIA"):
    if not api_key:
        st.error("Erro: API Key não configurada.")
    else:
        # Busca seu prompt salvo no arquivo txt
        with open("prompt_mestre.txt", "r", encoding="utf-8") as f:
            prompt_base = f.read()
        
        # Monta a consulta final
        input_data = f"\nCLIENTE: {nome}\nVALOR: {valor}\nATRASO: {atraso}\nCANAL: {canal}\nESTÁGIO: {estagio}\nSITUAÇÃO: {situacao}"
        
        with st.spinner("Analisando comportamento e gerando scripts..."):
            response = model.generate_content(prompt_base + input_data)
            st.markdown("### 🎯 Diagnóstico e Scripts Gerados")
            st.write(response.text)
