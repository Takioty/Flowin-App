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

# Funções de Lógica (Callbacks)
def remover_tarefa(id_tarefa): state.tarefas = [t for t in state.tarefas if t["id"] != id_tarefa]
def remover_gasto(id_gasto): state.gastos = [g for g in state.gastos if g["id"] != id_gasto]
def remover_nota(id_nota): state.notas = [n for n in state.notas if n["id"] != id_nota]

# Renderização da IA (Com autenticação corrigida)
def render_verity_ia(api_key):
    st.header("🙂 Assistente Virtual — Verity")
    for msg in state.historico_ia:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if prompt := st.chat_input("Pergunte algo à Verity..."):
        if not api_key:
            st.error("Por favor, insira sua chave API no menu lateral.")
            return
        
        state.historico_ia.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        with st.chat_message("assistant"):
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
                st.write(response.text)
                state.historico_ia.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro na conexão com a IA: {e}")

# Renderização das outras abas
def render_tarefas():
    st.header("✅ Gerenciador de Tarefas")
    nova_tarefa = st.text_input("Nova tarefa")
    if st.button("Adicionar"):
        state.tarefas.append({"id": uuid.uuid4(), "texto": nova_tarefa})
    for t in state.tarefas:
        c1, c2 = st.columns([0.8, 0.2])
        c1.write(t["texto"])
        if c2.button("🗑️", key=str(t["id"])):
            remover_tarefa(t["id"])
            st.rerun()

def render_financas():
    st.header("💰 Controle de Gastos")
    col1, col2 = st.columns(2)
    valor = col1.number_input("Valor", min_value=0.0)
    descricao = col2.text_input("Descrição")
    if st.button("Registrar Gasto"):
        state.gastos.append({"id": uuid.uuid4(), "valor": valor, "desc": descricao})
    st.write(f"### Total gasto: R$ {sum(g['valor'] for g in state.gastos):.2f}")
    for g in state.gastos:
        st.write(f"{g['desc']}: R$ {g['valor']:.2f}")

def render_notas():
    st.header("📓 Bloco de Notas")
    titulo = st.text_input("Título da nota")
    conteudo = st.text_area("Conteúdo")
    if st.button("Salvar Nota"):
        state.notas.append({"id": uuid.uuid4(), "titulo": titulo, "conteudo": conteudo})
    for n in state.notas:
        with st.expander(n["titulo"]):
            st.write(n["conteudo"])
            if st.button("Excluir", key=f"del_{n['id']}"):
                remover_nota(n["id"])
                st.rerun()

# Barra Lateral e Roteamento
with st.sidebar:
    st.title("Flowin")
    api_key = st.text_input("API Key do Gemini", type="password")
    st.markdown("[Obter sua chave aqui](https://aistudio.google.com/app/apikey)")
    st.markdown("---")
    pagina = st.radio("Navegação", ["🙂 Verity IA", "✅ Tarefas", "💰 Finanças", "📓 Notas"])

if pagina == "🙂 Verity IA": render_verity_ia(api_key)
elif pagina == "✅ Tarefas": render_tarefas()
elif pagina == "💰 Finanças": render_financas()
elif pagina == "📓 Notas": render_notas()
