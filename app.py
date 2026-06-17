# ==========================================
# 1. IMPORTAÇÕES
# ==========================================

import streamlit as st
from dataclasses import dataclass, field
import uuid
import pandas as pd
import plotly.express as px
import time
from google import genai  # Nova biblioteca oficial para o Assistente IA

# ==========================================
# 2. CONFIGURAÇÕES GLOBAIS
# ==========================================

st.set_page_config(
    page_title="Flowin",
    page_icon="📋",
    layout="wide"
)

state = st.session_state

# ==========================================
# 3. ESTRUTURAS DE DADOS (DATACLASSES)
# ==========================================

@dataclass
class Todo:
    text: str
    is_done: bool = False
    uid: uuid.UUID = field(default_factory=uuid.uuid4)

# ==========================================
# 4. INICIALIZAÇÃO DO SESSION STATE
# ==========================================

if "gastos" not in state:
    state.gastos = []

if "tarefas" not in state:
    state.tarefas = []

if "notas" not in state:
    state.notas = [
        {
            "id": str(uuid.uuid4()),
            "titulo": "🚀 Log de Bug #07 - Segurança",
            "conteudo": "Migração para autenticação via API Key do usuário para garantir segurança dos dados e escalabilidade, evitando exposição de chaves no GitHub."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "⏳ Log de Bug #03 - Infinite Loop no Cronômetro",
            "conteudo": "Dificuldade encontrada: O comando st.rerun() dentro do laço do Pomodoro estava sendo disparado rápido demais, ignorando o tempo real do processador e travando a aba do navegador por uso de 100% da CPU."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "⏱️ Resolução do Bug #03 - Sincronia de Tempo",
            "conteudo": "Solução aplicada: Introduzimos a biblioteca 'time' e adicionamos o método 'time.sleep(1)' imediatamente antes do decremento de segundos. Isso forçou o script a esperar exatamente 1 segundo antes de atualizar a tela."
        }
    ]

if "todos" not in state:
    state.todos = [
        Todo(text="Comprar leite"),
        Todo(text="Lavar louça"),
        Todo(text="Estudar Python")
    ]

if "tempo_estudado" not in state:
    state.tempo_estudado = 0  

if "pomodoro_segundos_restantes" not in state:
    state.pomodoro_segundos_restantes = 25 * 60

if "pomodoro_rodando" not in state:
    state.pomodoro_rodando = False

if "modo_atual" not in state:
    state.modo_atual = "🎯 Foco (25 min)"

if "historico_ia" not in state:
    state.historico_ia = [
        {"role": "assistant", "content": "Olá! Eu sou a Verity, sua assistente virtual no Flowin. Por favor, insira sua chave API do Gemini na barra lateral para começarmos a conversar hoje!"}
    ]

# Garantia de retrocompatibilidade de IDs
for gasto in state.gastos:
    if "id" not in gasto:
        gasto["id"] = str(uuid.uuid4())

for tarefa in state.tarefas:
    if "id" not in tarefa:
        tarefa["id"] = str(uuid.uuid4())

# ==========================================
# 5. FUNÇÕES DE LÓGICA E BACKEND (CALLBACKS)
# ==========================================

def remover_tarefa(id_tarefa):
    state.tarefas = [t for t in state.tarefas if t["id"] != id_tarefa]
    st.toast("Tarefa removida! 🗑️")

def remover_gasto(id_gasto):
    state.gastos = [g for g in state.gastos if g["id"] != id_gasto]
    st.toast("Gasto removido! 🗑️")

def limpar_todos_gastos():
    state.gastos = []
    st.toast("Histórico de finanças limpo! 🧹")

def remover_nota(id_nota):
    state.notas = [n for n in state.notas if n["id"] != id_nota]
    st.toast("Nota excluída! 🗑️")

def remove_todo(i):
    state.todos.pop(i)

def add_todo():
    if state.new_item_text != "":
        state.todos.append(Todo(text=state.new_item_text))
        state.new_item_text = ""

def check_todo(i, novo_valor):
    state.todos[i].is_done = novo_valor

def delete_all_checked():
    state.todos = [t for t in state.todos if not t.is_done]

# ==========================================
# 6. ESTILIZAÇÃO CSS CUSTOMIZADA
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #0b0c10;
}
[data-testid="stSidebar"] {
    background-color: #111217;
    border-right: 1px solid #1a1b23;
}
.user-profile-container {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    margin-top: -10px;
}
.user-avatar-circle {
    width: 32px;
    height: 32px;
    background-color: #3100b9;
    border-radius: 50%;
    flex-shrink: 0;
}
.user-profile-name {
    font-size: 15px !important;
    font-weight: 600;
    color: #ffffff;
}
.sidebar-title-top {
    font-size: 34px !important;
    font-weight: 700;
    color: #8b5cf6;
    text-align: center;
    width: 100%;
}
.sidebar-description {
    font-size: 13px !important;
    color: #797c8e;
    text-align: center;
    width: 100%;
}
.custom-hr {
    border: 0;
    height: 1px;
    background-color: #1c1d27;
    margin-bottom: 20px;
}
.feature-card {
    background-color: #111217;
    border: 1px solid #1a1b23;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    height: 100%;
}
.feature-card h3 {
    color: #a855f7 !important;
    margin-top: 0 !important;
}
.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #9333ea);
    color: white;
    border: none;
    border-radius: 10px;
}
.item-custom {
    text-align: center;
    background-color: #16171f;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 6px;
    border: 1px solid #232533;
    color: #e5e7eb;
    min-height: 46px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.nota-container {
    background-color: #111217;
    border: 1px solid #1a1b23;
    border-radius: 12px;
    padding: 20px;
}
.pomodoro-display {
    font-size: 80px !important;
    font-weight: 700;
    color: #a855f7;
    text-align: center;
    background-color: #111217;
    border: 1px solid #232533;
    border-radius: 16px;
    padding: 24px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 7. FUNÇÕES DE RENDERIZAÇÃO DAS PÁGINAS
# ==========================================

def render_inicio():
    st.title("🚀 Bem-vindo ao Flowin")
    st.subheader("Seu espaço integrado para foco, organização e controle")
    st.divider()
    
    st.markdown("### 🛠️ Explore as Funcionalidades")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='feature-card'><h3>🙂 Verity IA</h3><ul><li>Inteligência artificial nativa integrada ao ecossistema.<li>Insights baseados nas suas anotações e tarefas diárias.</ul></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div class='feature-card'><h3>✅ Gerenciamento de Tarefas</h3><ul><li>Criação de compromissos com definição clara de prazos.<li>Atribuição de níveis de prioridade visuais.</ul></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div class='feature-card'><h3>💰 Controle Financeiro</h3><ul><li>Registro instantâneo de despesas por contextos.<li>Gráficos dinâmicos gerados via Plotly.</ul></div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='feature-card'><h3>⏱️ Cronômetro Pomodoro</h3><ul><li>Ciclos tradicionais de 25 minutos de foco absoluto.<li>Descansos curtos de 5 minutos automáticos.</ul></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div class='feature-card'><h3>📝 To-do List</h3><ul><li>Painel dinâmico de marcação rápida de checklists.<li>Mecanismo de descarte em massa.</ul></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div class='feature-card'><h3>📓 Bloco de Notas</h3><ul><li>Espaço livre para rascunhos e registros textuais.<li>Exclusão isolada e dinâmica das notas.</ul></div>", unsafe_allow_html=True)


def render_verity_ia(api_key):
    st.header("🙂 Assistente Virtual — Verity")
    st.caption("Sua inteligência artificial conectada às suas tarefas, finanças e notas.")
    st.divider()

    for msg in state.historico_ia:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Pergunte à Verity sobre a sua rotina..."):
        if not api_key:
            st.error("Por favor, insira sua chave API no menu lateral para falar com a Verity.")
            return

        with st.chat_message("user"):
            st.write(prompt)
        state.historico_ia.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            try:
                with st.spinner("Verity está pensando..."):
                    contexto_sistema = (
                        "Você é a Verity, a Assistente Virtual nativa do aplicativo 'Flowin'. "
                        "Apresente-se e responda de forma direta e estruturada usando Markdown.\n\n"
                        "--- DADOS DO APP ---\n"
                    )
                    contexto_sistema += f"- Tarefas salvas: {len(state.tarefas)}\n"
                    contexto_sistema += f"- Gastos cadastrados: {len(state.gastos)}\n"
                    contexto_sistema += f"- Notas escritas: {len(state.notas)}\n"
                    contexto_sistema += f"- Minutos focados hoje: {state.tempo_estudado}\n"

                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=f"{contexto_sistema}\nPergunta do usuário: {prompt}"
                    )
                    
                    st.write(response.text)
                    state.historico_ia.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro na conexão (Verifique sua chave): {e}")


def render_tarefas():
    st.header("✅ Área de Tarefas")

    with st.form("form_tarefa", border=False):
        nome_tar = st.text_input("Nome da tarefa")
        prio_tar = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
        data_tar = st.date_input("Data")
        
        if st.form_submit_button("Adicionar tarefa"):
            if nome_tar != "":
                state.tarefas.append({
                    "id": str(uuid.uuid4()),
                    "Nome": nome_tar,
                    "Prioridade": prio_tar,
                    "Data": data_tar.strftime("%d/%m/%Y")
                })
                st.toast("Tarefa adicionada! 🚀")

    if state.tarefas:
        st.divider()
        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        c1.markdown("<b>Tarefa</b>", unsafe_allow_html=True)
        c2.markdown("<b>Prioridade</b>", unsafe_allow_html=True)
        c3.markdown("<b>Data Limite</b>", unsafe_allow_html=True)
        c4.write("")

        for t in state.tarefas:
            col_nome, col_prio, col_data, col_btn = st.columns([4, 2, 2, 1])
            col_nome.markdown(f"<div class='item-custom'>{t['Nome']}</div>", unsafe_allow_html=True)
            cor_prio = "#ef4444" if t['Prioridade'] == "Alta" else "#f59e0b" if t['Prioridade'] == "Média" else "#94a3b8"
            col_prio.markdown(f"<div class='item-custom' style='color:{cor_prio}; font-weight:bold;'>{t['Prioridade']}</div>", unsafe_allow_html=True)
            col_data.markdown(f"<div class='item-custom'>{t['Data']}</div>", unsafe_allow_html=True)
            col_btn.button("🗑️", key=f"del_tar_{t['id']}", on_click=remover_tarefa, args=[t['id']])
    else:
        st.info("Nenhuma tarefa agendada no momento.")


def render_financas():
    st.header("💰 Controle Financeiro")

    with st.form("form_gasto", border=False):
        desc_gasto = st.text_input("Descrição")
        cat_gasto = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Estudos", "Outros"])
        val_gasto = st.number_input("Valor", min_value=0.0)
        
        if st.form_submit_button("Registrar gasto"):
            if desc_gasto != "":
                state.gastos.append({
                    "id": str(uuid.uuid4()),
                    "Descrição": desc_gasto,
                    "Categoria": cat_gasto,
                    "Valor": val_gasto
                })
                st.toast("Gasto registrado! 👍")

    if state.gastos:
        df = pd.DataFrame(state.gastos)
        st.divider()
        col_tabela, col_grafico = st.columns([1.2, 1])

        with col_tabela:
            st.subheader("🛒 Histórico de Compras")
            for gasto in state.gastos:
                col_desc, col_cat, col_val, col_btn = st.columns([3, 3, 2, 1])
                col_desc.markdown(f"<div class='item-custom'>{gasto['Descrição']}</div>", unsafe_allow_html=True)
                col_cat.markdown(f"<div class='item-custom'>{gasto['Categoria']}</div>", unsafe_allow_html=True)
                col_val.markdown(f"<div class='item-custom'>R$ {gasto['Valor']:.2f}</div>", unsafe_allow_html=True)
                col_btn.button("🗑️", key=f"del_fin_{gasto['id']}", on_click=remover_gasto, args=[gasto['id']])
            
            st.button("🧹 Limpar Histórico Completo", on_click=limpar_todos_gastos)

        with col_grafico:
            st.subheader("📊 Distribuição de Gastos")
            df_categoria = df.groupby("Categoria")["Valor"].sum().reset_index()
            fig = px.pie(df_categoria, values="Valor", names="Categoria", hole=0.4, color_discrete_sequence=px.colors.sequential.Purples_r)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)


def render_notas():
    st.header("📓 Bloco de Notas")

    with st.form("form_nota", border=False):
        tit_nota = st.text_input("Título da Nota", placeholder="Ex: Ideias de projeto")
        cont_nota = st.text_area("Conteúdo", placeholder="Escreva aqui...")
        
        if st.form_submit_button("Salvar Nota"):
            if cont_nota != "":
                state.notas.append({
                    "id": str(uuid.uuid4()),
                    "titulo": tit_nota if tit_nota.strip() != "" else "Sem título",
                    "conteudo": cont_nota
                })
                st.toast("Nota salva! 📝")

    if state.notas:
        st.divider()
        cols = st.columns(2)
        for idx, nota in enumerate(state.notas):
            col_atual = cols[idx % 2]
            with col_atual:
                st.markdown(f"<div class='nota-container'><h3>{nota['titulo']}</h3><p>{nota['conteudo']}</p></div>", unsafe_allow_html=True)
                st.button("Excluir Nota 🗑️", key=f"del_nota_{nota['id']}", on_click=remover_nota, args=[nota['id']])


def render_todo_list():
    st.title("📝 To-do List Checklist")
    with st.form(key="new_item_form", border=False):
        st.text_input("Adicionar à checklist diária", key="new_item_text")
        st.form_submit_button("Adicionar", on_click=add_todo)

    if state.todos:
        for i, todo in enumerate(state.todos):
            col1, col2 = st.columns([8, 1])
            with col1:
                st.checkbox(todo.text, value=todo.is_done, on_change=check_todo, args=[i, not todo.is_done], key=f"todo-{todo.uid}")
            with col2:
                st.button("🗑️", on_click=remove_todo, args=[i], key=f"delete_{i}")
        st.button("Apagar tarefas concluídas", on_click=delete_all_checked)


def render_pomodoro():
    st.header("⏱️ Cronômetro Pomodoro")
    
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("🎓 Tempo total de foco", f"{state.tempo_estudado} min")
    col_stat2.metric("🔄 Ciclos Feitos", f"{state.tempo_estudado // 25}")

    st.divider()
    modo_selecionado = st.radio("Modo:", ["🎯 Foco (25 min)", "☕ Pausa Curta (5 min)"], horizontal=True)
    
    if modo_selecionado != state.modo_atual:
        state.modo_atual = modo_selecionado
        state.pomodoro_segundos_restantes = 25 * 60 if "Foco" in modo_selecionado else 5 * 60
        state.pomodoro_rodando = False

    texto_cronometro = st.empty()
    c_btn1, c_btn2, _ = st.columns([1, 1, 4])

    if not state.pomodoro_rodando:
        if c_btn1.button("🚀 Iniciar"):
            state.pomodoro_rodando = True
            st.rerun()
    else:
        if c_btn1.button("Pausar ⏸️"):
            state.pomodoro_rodando = False
            st.rerun()

    if c_btn2.button("Reiniciar 🔄"):
        state.pomodoro_segundos_restantes = 25 * 60 if "Foco" in state.modo_atual else 5 * 60
        state.pomodoro_rodando = False
        st.rerun()

    if state.pomodoro_rodando and state.pomodoro_segundos_restantes > 0:
        mins, segs = divmod(state.pomodoro_segundos_restantes, 60)
        texto_cronometro.markdown(f"<div class='pomodoro-display'>{mins:02d}:{segs:02d}</div>", unsafe_allow_html=True)
        time.sleep(1)
        state.pomodoro_segundos_restantes -= 1
        st.rerun()
    elif state.pomodoro_segundos_restantes == 0 and state.pomodoro_rodando:
        state.pomodoro_rodando = False
        if "Foco" in state.modo_atual:
            state.tempo_estudado += 25  
            st.balloons()
        state.pomodoro_segundos_restantes = 5 * 60 if "Foco" in state.modo_atual else 25 * 60
        st.rerun()
    else:
        mins, segs = divmod(state.pomodoro_segundos_restantes, 60)
        texto_cronometro.markdown(f"<div class='pomodoro-display'>{mins:02d}:{segs:02d}</div>", unsafe_allow_html=True)

# ==========================================
# 8. CONSTRUÇÃO DA BARRA LATERAL (SIDEBAR)
# ==========================================

with st.sidebar:
    st.markdown("<div class='user-profile-container'><div class='user-avatar-circle'></div><span class='user-profile-name'>usuário_1</span></div>", unsafe_allow_html=True)
    st.markdown("<p class='sidebar-title-top'>📋 Flowin</p>", unsafe_allow_html=True)
    st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
    
    st.markdown("### 🔑 Token de Acesso")
    api_key_usuario = st.text_input("API Key do Gemini", type="password", placeholder="Cole sua chave aqui...")
    st.markdown("[Obter chave no AI Studio](https://aistudio.google.com/app/apikey)")
    st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)

    pagina = st.radio(
        "Navegação",
        ["🏠 Início", "🙂 Verity IA", "✅ Tarefas", "📝 To-do List", "💰 Finanças", "📓 Notas", "⏱️ Pomodoro"]
    )

# ==========================================
# 9. ROTEADOR DE NAVEGAÇÃO PRINCIPAL
# ==========================================

if pagina == "🏠 Início":
    render_inicio()
elif pagina == "🙂 Verity IA":
    render_verity_ia(api_key_usuario)
elif pagina == "✅ Tarefas":
    render_tarefas()
elif pagina == "💰 Finanças":
    render_financas()
elif pagina == "📓 Notas":
    render_notas()
elif pagina == "📝 To-do List":
    render_todo_list()
elif pagina == "⏱️ Pomodoro":
    render_pomodoro()
