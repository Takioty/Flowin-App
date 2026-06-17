import streamlit as st
from dataclasses import dataclass, field
import uuid
from google import genai 

# Configuração da página
st.set_page_config(page_title="Flowin", page_icon="📋", layout="wide")
state = st.session_state

# Inicialização de dados
if "tarefas" not in state: state.tarefas = []
if "gastos" not in state: state.gastos = []
if "notas" not in state: state.notas = []
if "historico_ia" not in state: state.historico_ia = []

# Funções de renderização
def render_verity_ia(api_key):
    st.header("🙂 Assistente Virtual — Verity")
    for msg in state.historico_ia:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if prompt := st.chat_input("Pergunte algo..."):
        if not api_key:
            st.error("Insira sua API Key no menu lateral.")
            return
        
        state.historico_ia.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        with st.chat_message("assistant"):
            client = genai.Client(api_key=api_key)
            resposta = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            st.write(resposta.text)
            state.historico_ia.append({"role": "assistant", "content": resposta.text})

def render_tarefas():
    st.header("✅ Gerenciador de Tarefas")
    nova_tarefa = st.text_input("Nova tarefa")
    if st.button("Adicionar"):
        state.tarefas.append({"id": uuid.uuid4(), "texto": nova_tarefa})
    
    for t in state.tarefas:
        col1, col2 = st.columns([0.8, 0.2])
        col1.write(t["texto"])
        if col2.button("Remover", key=t["id"]):
            state.tarefas.remove(t)
            st.rerun()

def render_financas():
    st.header("💰 Controle de Gastos")
    valor = st.number_input("Valor", min_value=0.0)
    descricao = st.text_input("Descrição")
    if st.button("Registrar Gasto"):
        state.gastos.append({"valor": valor, "desc": descricao})
    st.write(f"Total gasto: R$ {sum(g['valor'] for g in state.gastos):.2f}")

def render_notas():
    st.header("📓 Bloco de Notas")
    titulo = st.text_input("Título")
    conteudo = st.text_area("Conteúdo")
    if st.button("Salvar Nota"):
        state.notas.append({"titulo": titulo, "conteudo": conteudo})
    for n in state.notas:
        with st.expander(n["titulo"]):
            st.write(n["conteudo"])

# Barra Lateral
with st.sidebar:
    st.title("Flowin")
    api_key = st.text_input("API Key do Gemini", type="password")
    st.markdown("[Obter chave aqui](https://aistudio.google.com/app/apikey)")
    pagina = st.radio("Navegação", ["🙂 Verity IA", "✅ Tarefas", "💰 Finanças", "📓 Notas"])

# Roteamento
if pagina == "🙂 Verity IA": render_verity_ia(api_key)
elif pagina == "✅ Tarefas": render_tarefas()
elif pagina == "💰 Finanças": render_financas()
elif pagina == "📓 Notas": render_notas()
