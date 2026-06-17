# ==========================================
# 1. IMPORTAÇÕES
# ==========================================

import streamlit as st
from dataclasses import dataclass, field
import uuid
import pandas as pd
import plotly.express as px
import time
from google import genai 

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
            "titulo": "🐛 Log de Bug #01 - Conflito no st.form",
            "conteudo": "Dificuldade encontrada: Ao alternar entre as abas do menu lateral, o Streamlit destruía as variáveis de formulário ativas. Isso causava uma quebra na aplicação sempre que tentávamos salvar uma Tarefa ou Finança usando callbacks de botão comum (on_click)."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "🩹 Resolução do Bug #01 - Refatoração",
            "conteudo": "Solução aplicada: Removemos a lógica de monitoramento externa e passamos a usar 'if st.form_submit_button():' para capturar os dados do formulário instantaneamente e de forma síncrona diretamente da tela, eliminando o erro de tela vermelha."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "⚠️ Log de Bug #02 - KeyError: 'id'",
            "conteudo": "Dificuldade encontrada: Após atualizar a estrutura da lixeira para usar UUIDs únicos, os dados antigos salvos no cache do navegador que não possuíam o campo 'id' geravam uma exceção fatal. Corrigido adicionando um laço de verificação preventiva e limpeza na inicialização do app."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "⏳ Log de Bug #03 - Infinite Loop no Cronômetro",
            "conteudo": "Dificuldade encontrada: O comando st.rerun() dentro do laço do Pomodoro estava sendo disparado rápido demais, ignorando o tempo real do processador e travando a aba do navegador por uso de 100% da CPU."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "⏱️ Resolução do Bug #03 - Sincronia de Tempo",
            "conteudo": "Solução aplicada: Introduzimos a biblioteca 'time' e adicionamos o método 'time.sleep(1)' imediatamente antes do decremento de segundos. Isso forçou o script a esperar exatamente 1 segundo antes de atualizar a tela, normalizando o consumo de hardware."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "🤖 Log de Bug #04 - Vazamento de Contexto (Prompt)",
            "conteudo": "Dificuldade encontrada: A inteligência artificial começou a inventar dados fictícios sobre despesas que o usuário nunca cadastrou, misturando o histórico de conversas antigas com a sessão atual do app."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "🧠 Resolução do Bug #04 - Engenharia de Prompt",
            "conteudo": "Solução aplicada: Blindamos o 'system_instruction' da Verity, adicionando uma ordem explícita: 'Baseie-se estritamente e unicamente nos dados JSON fornecidos abaixo. Se a lista estiver vazia, diga explicitamente que não há registros'."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "📊 Log de Bug #05 - Gráfico Plotly Invisível",
            "conteudo": "Dificuldade encontrada: O gráfico de pizza da aba de Finanças quebrava e ficava completamente invisível quando o usuário limpapa o histórico de compras, pois o Pandas tentava agrupar um DataFrame vazio por 'Categoria'."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "🎨 Resolução do Bug #05 - Renderização Condicional",
            "conteudo": "Solução aplicada: Envolvemos toda a plotagem do gráfico dentro do bloco condicional 'if state.gastos:'. Dessa forma, o gráfico só é construído se houver pelo menos um item registrado, evitando falhas matemáticas no Plotly."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "🔑 Log de Bug #06 - API Key Exposta",
            "conteudo": "Dificuldade encontrada: Risco de segurança ao deixar o token do Gemini hardcoded no topo do arquivo principal, o que gerava alertas de segurança automáticos ao tentar realizar commits para o repositório público do GitHub."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "🔐 Resolução do Bug #06 - Variáveis de Ambiente",
            "conteudo": "Solução aplicada: Planejado para a próxima sprint a migração da chave para o sistema nativo 'st.secrets' do Streamlit ou leitura via arquivo .env invisível, garantindo que as credenciais fiquem salvas apenas no servidor local."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "🚀 Log de Bug #07 - Autenticação Dinâmica",
            "conteudo": "Solução aplicada: Migração completa para autenticação via API Key do próprio usuário direto na interface da barra lateral, resolvendo os problemas de push do GitHub e garantindo isolamento de quotas."
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "🛑 Log de Bug #08 - Rate Limit (Erro 429)",
            "conteudo": "Dificuldade encontrada: Ao realizar testes seguidos na Verity IA no plano gratuito, o Google bloqueou temporariamente as requisições por esgotamento de quota de requisições por minuto (RESOURCE_EXHAUSTED)."
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
        {"role": "assistant", "content": "Olá! Eu sou a Verity, sua assistente virtual no Flowin. Por favor, insira sua chave API na barra lateral para que eu possa analisar seus dados e te ajudar hoje!"}
    ]

# Garantia de IDs únicos
for gasto in state.gastos:
    if "id" not in gasto: gasto["id"] = str(uuid.uuid4())
for tarefa in state.tarefas:
    if "id" not in tarefa: tarefa["id"] = str(uuid.uuid4())

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
.stApp { background-color: #0b0c10; }
[data-testid="stSidebar"] { background-color: #111217; border-right: 1px solid #1a1b23; }
.user-profile-container { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; margin-top: -10px; }
.user-avatar-circle { width: 32px; height: 32px; background-color: #3100b9; border-radius: 50%; flex-shrink: 0; }
.user-profile-name { font-size: 15px !important; font-weight: 600; color: #ffffff; letter-spacing: -0.2px; }
.sidebar-title-top { font-size: 34px !important; font-weight: 700; color: #8b5cf6; margin-top: 10px; margin-bottom: 6px; letter-spacing: -0.8px; text-align: center; width: 100%; }
.sidebar-description { font-size: 13px !important; color: #797c8e; line-height: 1.4; margin-bottom: 25px; text-align: center; width: 100%; }
.custom-hr { border: 0; height: 1px; background-color: #1c1d27; margin-top: 0; margin-bottom: 20px; }
.menu-label { font-size: 11px !important; font-weight: 700; color: #434554; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; }
.feature-card { background-color: #111217; border: 1px solid #1a1b23; border-radius: 12px; padding: 24px; margin-bottom: 20px; height: 100%; }
.feature-card h3 { color: #a855f7 !important; margin-top: 0 !important; margin-bottom: 12px !important; font-size: 18px !important; }
.feature-card ul { margin: 0 !important; padding-left: 20px !important; color: #b3b6c6; }
.feature-card li { margin-bottom: 8px !important; font-size: 14px !important; line-height: 1.4; }
.stButton > button { background: linear-gradient(90deg, #7c3aed, #9333ea); color: white; border: none; border-radius: 10px; padding: 8px 20px; font-weight: 600; }
.stButton > button:hover { background: linear-gradient(90deg, #9333ea, #a855f7); }
.item-custom { text-align: center; background-color: #16171f; padding: 12px; border-radius: 8px; margin-bottom: 6px; border: 1px solid #232533; color: #e5e7eb; min-height: 46px; display: flex; align-items: center; justify-content: center; }
.nota-container { background-color: #111217; border: 1px solid #1a1b23; border-radius: 12px; padding: 20px; margin-bottom: 10px;}
.pomodoro-display { font-size: 80px !important; font-weight: 700; color: #a855f7; text-align: center; background-color: #111217; border: 1px solid #232533; border-radius: 16px; padding: 24px; font-family: monospace; }
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
        st.markdown("<div class='feature-card'><h3>🙂 Verity IA</h3><ul><li>Inteligência artificial nativa integrada ao ecossistema.<li>Leitura inteligente do seu contexto de dados do aplicativo.<li>Resumo de notas, insights financeiros e dicas personalizadas.</ul></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div class='feature-card'><h3>✅ Gerenciamento de Tarefas</h3><ul><li>Criação de compromissos com definição clara de prazos.<li>Atribuição de níveis de prioridade com marcadores visuais.<li>Remoção rápida e intuitiva através de lixeiras individuais.</ul></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div class='feature-card'><h3>💰 Controle Financeiro</h3><ul><li>Registro instantâneo de saídas financeiras por contextos.<li>Gráficos de pizza dinâmicos gerados via Plotly.<li>Acompanhamento total de despesas e limpeza de histórico.</ul></div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='feature-card'><h3>⏱️ Cronômetro Pomodoro</h3><ul><li>Ciclos tradicionais de 25 minutos de foco absoluto.<li>Descansos curtos de 5 minutos automáticos.<li>Métricas de tempo total e ciclos completados.</ul></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div class='feature-card'><h3>📝 To-do List</h3><ul><li>Painel dinâmico de marcação diária de checklists.<li>Mecanismo de descarte em massa para tarefas executadas.<li>Persistência simples de estado de checagem.</ul></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div class='feature-card'><h3>📓 Bloco de Notas</h3><ul><li>Espaço livre para rascunhos e registros textuais.<li>Distribuição automática das notas em formato de painel grid.<li>Exclusão isolada preservando dados paralelos.</ul></div>", unsafe_allow_html=True)


def render_verity_ia(api_key):
    st.header("🙂 Assistente Virtual — Verity")
    st.caption("Sua inteligência artificial conectada às suas tarefas, finanças e notas.")
    st.divider()

    for msg in state.historico_ia:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Pergunte à Verity sobre a sua rotina ou dados..."):
        if not api_key:
            st.error("Por favor, insira sua chave API no menu lateral para falar com a Verity.")
            return

        with st.chat_message("user"):
            st.write(prompt)
        state.historico_ia.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            try:
                with st.spinner("Verity está analisando seus dados e pensando..."):
                    contexto_sistema = (
                        "Você é a Verity, a Assistente Virtual nativa do aplicativo 'Flowin'. "
                        "Apresente-se e responda como Verity. Seja empática, direta, organizada e use markdown.\n\n"
                        "Aqui estão os dados resumidos do app para responder o usuário:\n"
                        f"- Tarefas agendadas: {len(state.tarefas)}\n"
                        f"- Quantidade de notas: {len(state.notas)}\n"
                        f"- Registros de gastos: {len(state.gastos)}\n"
                        f"- Tempo de Pomodoro focado: {state.tempo_estudado} minutos.\n\n"
                    )

                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=f"{contexto_sistema}\nPergunta do usuário: {prompt}"
                    )
                    
                    st.write(response.text)
                    state.historico_ia.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Ocorreu um erro ao falar com a IA: {e}")


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
                st.toast("Tarefa adicionada com sucesso! 🚀")

    if state.tarefas:
        st.divider()
        st.subheader("📋 Suas Tarefas Agendadas")
        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        c1.markdown("<b style='display:block; text-align:center;'>Tarefa</b>", unsafe_allow_html=True)
        c2.markdown("<b style='display:block; text-align:center;'>Prioridade</b>", unsafe_allow_html=True)
        c3.markdown("<b style='display:block; text-align:center;'>Data Limite</b>", unsafe_allow_html=True)
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
                st.toast("Gasto registrado com sucesso! 👍")

    if state.gastos:
        df = pd.DataFrame(state.gastos)
        st.divider()
        col_tabela, col_grafico = st.columns([1.2, 1])

        with col_tabela:
            st.subheader("🛒 Histórico de Compras")
            c1, c2, c3, c4 = st.columns([3, 3, 2, 1])
            c1.markdown("<b style='display:block; text-align:center;'>Descrição</b>", unsafe_allow_html=True)
            c2.markdown("<b style='display:block; text-align:center;'>Categoria</b>", unsafe_allow_html=True)
            c3.markdown("<b style='display:block; text-align:center;'>Valor</b>", unsafe_allow_html=True)
            c4.write("")
            
            for gasto in state.gastos:
                col_desc, col_cat, col_val, col_btn = st.columns([3, 3, 2, 1])
                col_desc.markdown(f"<div class='item-custom'>{gasto['Descrição']}</div>", unsafe_allow_html=True)
                col_cat.markdown(f"<div class='item-custom'>{gasto['Categoria']}</div>", unsafe_allow_html=True)
                col_val.markdown(f"<div class='item-custom'>R$ {gasto['Valor']:.2f}</div>", unsafe_allow_html=True)
                col_btn.button("🗑️", key=f"del_fin_{gasto['id']}", on_click=remover_gasto, args=[gasto['id']])
            
            st.write("")
            st.button("🧹 Limpar Histórico Completo", on_click=limpar_todos_gastos)

        with col_grafico:
            st.subheader("📊 Gastos por Categoria")
            df_categoria = df.groupby("Categoria")["Valor"].sum().reset_index()
            fig = px.pie(df_categoria, values="Valor", names="Categoria", hole=0.4, color_discrete_sequence=px.colors.sequential.Purples_r)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)


def render_notas():
    st.header("📓 Bloco de Notas")
    st.caption("Guarde suas ideias, rascunhos e logs de desenvolvimento")

    with st.form("form_nota", border=False):
        tit_nota = st.text_input("Título da Nota", placeholder="Ex: Ideias para o projeto")
        cont_nota = st.text_area("Conteúdo da Nota", placeholder="Digite sua anotação aqui...", height=150)
        
        if st.form_submit_button("Salvar Nota"):
            if cont_nota != "":
                state.notas.append({
                    "id": str(uuid.uuid4()),
                    "titulo": tit_nota.strip() if tit_nota.strip() != "" else "Nota sem título",
                    "conteudo": cont_nota
                })
                st.toast("Nota salva com sucesso! 📝")

    if state.notas:
        st.divider()
        st.subheader("📌 Suas Notas Salvas")
        cols = st.columns(2)
        for idx, nota in enumerate(state.notas):
            col_atual = cols[idx % 2]
            with col_atual:
                st.markdown(f"<div class='nota-container'><h3 style='color:#a855f7; margin-top:0; margin-bottom:10px;'>{nota['titulo']}</h3><p style='color:#e2e8f0; white-space: pre-wrap; font-size:15px;'>{nota['conteudo']}</p></div>", unsafe_allow_html=True)
                st.button("🗑️ Excluir Nota", key=f"del_nota_{nota['id']}", on_click=remover_nota, args=[nota['id']])
                st.write("") 


def render_todo_list():
    st.title("📝 To-do List")
    with st.form(key="new_item_form", border=False):
        st.text_input("Nova tarefa", key="new_item_text")
        st.form_submit_button("Adicionar", on_click=add_todo)

    if state.todos:
        for i, todo in enumerate(state.todos):
            col1, col2 = st.columns([8, 1])
            with col1:
                st.checkbox(todo.text, value=todo.is_done, on_change=check_todo, args=[i, not todo.is_done], key=f"todo-{todo.uid}")
            with col2:
                st.button("🗑️", on_click=remove_todo, args=[i], key=f"delete_{i}")
        st.button("Apagar concluídas", on_click=delete_all_checked)


def render_pomodoro():
    st.header("⏱️ Cronômetro Pomodoro")

    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("🎓 Total de Tempo Estudado", f"{state.tempo_estudado} min")
    col_stat2.metric("🔄 Ciclos Feitos", f"{state.tempo_estudado // 25}")

    st.divider()
    modo_selecionado = st.radio("Selecione o modo:", ["🎯 Foco (25 min)", "☕ Pausa Curta (5 min)"], horizontal=True)
    
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
        if c_btn1.button("⏸️ Pausar"):
            state.pomodoro_rodando = False
            st.rerun()

    if c_btn2.button("🔄 Reiniciar"):
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
    
    st.markdown("### 🔑 Token Gemini")
    api_key_usuario = st.text_input("API Key do Gemini", type="password", placeholder="Insira seu token...")
    st.markdown("[Pegar chave no AI Studio](https://aistudio.google.com/app/apikey)")
    st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)

    pagina = st.radio(
        "Navegação",
        ["🏠 Início", "🙂 Verity IA", "✅ Tarefas", "📝 To-do List", "💰 Finanças", "📓 Notas", "⏱️ Pomodoro"]
    )

    st.markdown("<div class='custom-hr' style='margin-top:30px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#4e5162; font-size:12px;'>Feito por <b>Pedro e Nicolas</b><br>Orientador: <b>Prof. Anderson</b></div>", unsafe_allow_html=True)

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
