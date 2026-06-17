# ==========================================
# IMPORTAÇÕES
# ==========================================

import streamlit as st
from dataclasses import dataclass, field
import uuid
import pandas as pd
import plotly.express as px
import time
from google import genai 

# Nova biblioteca oficial para o Assistente IA

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Flowin",
    page_icon="📋",
    layout="wide"
)

state = st.session_state

# ==========================================
# INSPIRADO NAS REFERÊNCIAS COMO NOTION E GOOGLE NOTES
# ==========================================

st.markdown("""
<style>

/* Fundo principal do app */
.stApp {
    background-color: #0b0c10;
}

/* Painel de Fundo da Barra Lateral */
[data-testid="stSidebar"] {
    background-color: #111217;
    border-right: 1px solid #1a1b23;
}

/* Container do Perfil do Usuário Estilo image_eb34cd.png */
.user-profile-container {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    margin-top: -10px;
}

/* Círculo do Avatar Roxo */
.user-avatar-circle {
    width: 32px;
    height: 32px;
    background-color: #3100b9;
    border-radius: 50%;
    flex-shrink: 0;
}

/* Texto do Nome do Usuário ao Lado do Avatar */
.user-profile-name {
    font-size: 15px !important;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: -0.2px;
}

/* Nome Principal do App (Flowin) - Maior, Centralizado e em Roxo Premium */
.sidebar-title-top {
    font-size: 34px !important;
    font-weight: 700;
    color: #8b5cf6;
    margin-top: 10px;
    margin-bottom: 6px;
    letter-spacing: -0.8px;
    text-align: center;
    width: 100%;
}

/* Subtítulo / Descrição - Centralizado */
.sidebar-description {
    font-size: 13px !important;
    color: #797c8e;
    line-height: 1.4;
    margin-bottom: 25px;
    text-align: center;
    width: 100%;
}

/* Divisores Minimalistas e Finos */
.custom-hr {
    border: 0;
    height: 1px;
    background-color: #1c1d27;
    margin-top: 0;
    margin-bottom: 20px;
}

/* Rótulo de seção ("MENU") */
.menu-label {
    font-size: 11px !important;
    font-weight: 700;
    color: #434554;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}

/* ==========================================
   REMOÇÃO TOTAL DE COMPONENTES DO RADIO NATIVO
   ========================================== */

[data-testid="stSidebar"] div[role="radiogroup"] [data-testid="stWidgetRadioDot"],
[data-testid="stSidebar"] div[role="radiogroup"] [data-testid="stWidgetRadioDot"]::before,
[data-testid="stSidebar"] div[role="radiogroup"] [data-testid="stWidgetRadioDot"]::after,
[data-testid="stSidebar"] label > div:first-child {
    display: none !important;
    width: 0px !important;
    height: 0px !important;
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 6px !important;
    padding: 0 !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] > label {
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    padding: 11px 16px !important;
    background-color: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    transition: all 0.15s ease-in-out !important;
    margin: 0 !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
    color: #8a8d9f !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background-color: #181921 !important;
}
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover div[data-testid="stMarkdownContainer"] p {
    color: #ffffff !important;
}

/* ==========================================
   BLOCO SELECIONADO / ATIVO
   ========================================== */
[data-testid="stSidebar"] div[role="radiogroup"] [aria-checked="true"] {
    background: none !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] [aria-checked="true"] > label {
    background-color: #3b2863 !important;
    border-color: transparent !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] [aria-checked="true"] label div[data-testid="stMarkdownContainer"] p {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Rodapé Ajustado na Base - Centralizado */
.sidebar-footer-container {
    margin-top: 40px;
    text-align: center;
    width: 100%;
}

.sidebar-title-bottom {
    font-size: 16px !important;
    font-weight: 700;
    color: #8b5cf6;
    margin-bottom: 4px;
}

.sidebar-footer-credits {
    font-size: 12px !important;
    color: #4e5162;
    line-height: 1.5;
}

/* ==========================================
   CARDS E COMPONENTES DE CONTEÚDO
   ========================================== */

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
    margin-bottom: 12px !important;
    font-size: 18px !important;
}

.feature-card ul {
    margin: 0 !important;
    padding-left: 20px !important;
    color: #b3b6c6;
}

.feature-card li {
    margin-bottom: 8px !important;
    font-size: 14px !important;
    line-height: 1.4;
}

.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #9333ea);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #9333ea, #a855f7);
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
    font-family: monospace;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE (INICIALIZAÇÃO)
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
            "titulo": "🛑 Log de Bug #08 - Rate Limit (Erro 429)",
            "conteudo": "Dificuldade encontrada: Ao realizar testes seguidos na Verity IA no plano gratuito, o Google bloqueou as requisições por esgotamento de quota por minuto (RESOURCE_EXHAUSTED). Implementado painel dinâmico de chaves para evitar travamentos de quota compartilhada."
        }
    ]

if "tempo_estudado" not in state:
    state.tempo_estudado = 0  

if "pomodoro_segundos_restantes" not in state:
    state.pomodoro_segundos_restantes = 25 * 60

if "pomodoro_rodando" not in state:
    state.pomodoro_rodando = False

if "modo_atual" not in state:
    state.modo_atual = "🎯 Foco (25 min)"

# Inicialização do Histórico do Chat com o nome "Verity"
if "historico_ia" not in state:
    state.historico_ia = [
        {"role": "assistant", "content": "Olá! Eu sou a Verity, sua assistente virtual no Flowin. Como posso te ajudar a organizar seu dia, analisar suas finanças ou revisar suas anotações hoje?"}
    ]

for gasto in state.gastos:
    if "id" not in gasto:
        gasto["id"] = str(uuid.uuid4())

for tarefa in state.tarefas:
    if "id" not in tarefa:
        tarefa["id"] = str(uuid.uuid4())

# ==========================================
# BARRA LATERAL (MONTAGEM DO DESIGN)
# ==========================================

with st.sidebar:
    st.markdown("""
    <div class='user-profile-container'>
        <div class='user-avatar-circle'></div>
        <span class='user-profile-name'>Anderson.Vaz</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p class='sidebar-title-top'> Flowin</p>", unsafe_allow_html=True)
    st.markdown("<p class='sidebar-description'>Seu organizador pessoal feito somente para você.</p>", unsafe_allow_html=True)

    st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
    
    # Gerenciamento Dinâmico de API Keys para mitigar Erros 429
    st.markdown("### 🔑 Token Gemini")
    api_key_usuario = st.text_input("Insira sua Gemini API Key", type="password", placeholder="AI Studio Key...", value="")
    st.markdown("[Pegar chave no AI Studio](https://aistudio.google.com/app/apikey)", unsafe_allow_html=True)
    
    st.markdown("<div class='custom-hr' style='margin-top:15px;'></div>", unsafe_allow_html=True)
    st.markdown("<p class='menu-label'>Menu</p>", unsafe_allow_html=True)

    pagina = st.radio(
        "Navegação",
        ["🏠 Início", "🙂 Assistente IA", "✅ Tarefas", "📝 To-do List", "💰 Finanças", "📓 Notas", "⏱️ Pomodoro"],
        label_visibility="collapsed"
    )

    st.markdown("<div class='custom-hr' style='margin-top:30px;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='sidebar-footer-container'>
        <p class='sidebar-title-bottom'>💜 Flowin 💜</p>
        <div class='sidebar-footer-credits'>
            Feito por <b>Pedro Eduardo e Nicolas Palma</b><br>
            Orientador: <b>Prof. Anderson</b><br>
            <i>Desenvolvido em Streamlit</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGINA: INÍCIO
# ==========================================

if pagina == "🏠 Início":
    st.title("🚀 Bem-vindo ao Flowin")
    st.subheader("Seu espaço integrado para foco, organization e controle")
    st.divider()
    
    st.markdown("### 🛠️ Explore as Funcionalidades")
    st.write("")

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("""
        <div class='feature-card'>
            <h3>🙂 Assistente IA (Verity)</h3>
            <ul>
                <li>Inteligência artificial nativa integrada ao ecossistema.
                <li>Leitura inteligente do seu contexto de dados do aplicativo.
                <li>Resumo de notas, insights financeiros e dicas personalizadas.
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

        st.markdown("""
        <div class='feature-card'>
            <h3>✅ Gerenciamento de Tarefas</h3>
            <ul>
                <li>Criação de compromissos com definição clara de prazos.
                <li>Atribuição de níveis de prioridade com marcadores visuais.
                <li>Remoção rápida e intuitiva através de lixeiras individuais.
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        st.markdown("""
        <div class='feature-card'>
            <h3>💰 Controle Financeiro</h3>
            <ul>
                <li>Registro instantâneo de saídas financeiras por contextos.
                <li>Gráficos de pizza dinâmicos gerados via Plotly.
                <li>Acompanhamento total de despesas e limpeza de histórico.
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class='feature-card'>
            <h3>⏱️ Cronômetro Pomodoro</h3>
            <ul>
                <li>Ciclos tradicionais de 25 minutos de foco absoluto.
                <li>Descansos curtos de 5 minutos automáticos.
                <li>Métricas de tempo total e ciclos completados.
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

        st.markdown("""
        <div class='feature-card'>
            <h3>📝 To-do List</h3>
            <ul>
                <li>Painel dinâmico de marcação diária de checklists.
                <li>Mecanismo de descarte em massa para tarefas executadas.
                <li>Persistência simples de estado de checagem.
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        st.markdown("""
        <div class='feature-card'>
            <h3>📓 Bloco de Notas</h3>
            <ul>
                <li>Espaço livre para rascunhos e registros textuais.
                <li>Distribuição automática das notas em formato de painel grid.
                <li>Exclusão isolada preservando dados paralelos.
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PAGINA: ASSISTENTE VIRTUAL IA (VERITY)
# ==========================================

elif pagina == "🙂 Assistente IA":
    st.header("🙂 Assistente Virtual — Verity")
    st.caption("Sua inteligência artificial conectada às suas tarefas, finanças e notas.")
    st.divider()

    # Renderiza todas as mensagens salvas na memória
    for msg in state.historico_ia:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Entrada de texto do usuário
    if prompt := st.chat_input("Pergunte à Verity sobre a sua rotina ou dados..."):
        
        # Mostra o prompt imediatamente no chat
        with st.chat_message("user"):
            st.write(prompt)
        state.historico_ia.append({"role": "user", "content": prompt})

        # Processamento e chamada da API
        with st.chat_message("assistant"):
            placeholder_resposta = st.empty()
            
            if not api_key_usuario or api_key_usuario.strip() == "":
                placeholder_resposta.error("Erro de Configuração: Insira uma Chave de API do Gemini válida na barra lateral esquerda para ativar o Assistente.")
            else:
                try:
                    with st.spinner("Verity está analisando seus dados e pensando..."):
                        # Construção inteligente do Contexto de Dados do App
                        contexto_sistema = (
                            "Você é a Verity, a Assistente Virtual nativa do aplicativo 'Flowin', focado em produtividade e organização pessoal. "
                            "Apresente-se e responda como Verity. Seja empática, direta, organizada e use formatação markdown quando útil. "
                            "Aqui estão os dados reais antigos do usuário dentro do aplicativo para você usar como contexto nas respostas:\n\n"
                        )
                        
                        # Injetando tarefas
                        contexto_sistema += "--- TAREFAS AGENDADAS ---\n"
                        if state.tarefas:
                            for t in state.tarefas:
                                contexto_sistema += f"- Tarefa: {t['Nome']} | Prioridade: {t['Prioridade']} | Prazo: {t['Data']}\n"
                        else:
                            contexto_sistema += "O usuário não possui tarefas cadastradas no momento.\n"
                            
                        # Injetando finanças
                        contexto_sistema += "\n--- HISTÓRICO DE DESPESAS/FINANÇAS ---\n"
                        if state.gastos:
                            total_gasto = sum(g['Valor'] for g in state.gastos)
                            contexto_sistema += f"Gasto total registrado: R$ {total_gasto:.2f}\n"
                            for g in state.gastos:
                                contexto_sistema += f"- Item: {g['Descrição']} | Categoria: {g['Categoria']} | Valor: R$ {g['Valor']:.2f}\n"
                        else:
                            contexto_sistema += "Nenhum gasto registrado ainda.\n"
                            
                        # Injetando notas
                        contexto_sistema += "\n--- BLOCO DE NOTAS DO USUÁRIO ---\n"
                        if state.notas:
                            for n in state.notas:
                                contexto_sistema += f"Título: {n['titulo']}\nConteúdo: {n['conteudo']}\n\n"
                        else:
                            contexto_sistema += "Nenhuma nota salva.\n"
                        
                        contexto_sistema += f"\nTempo total de foco registrado no Pomodoro: {state.tempo_estudado} minutos.\n\n"
                        contexto_sistema += "Responda à pergunta do usuário considerando esses dados acima sempre que fizer sentido."

                        # Conversão do histórico interno do app para o formato esperado pela SDK oficial
                        historico_formatated = []
                        for m in state.historico_ia[:-1]: # ignora o último prompt que acabou de entrar
                            role_sdk = "user" if m["role"] == "user" else "model"
                            historico_formatated.append(genai.types.Content(
                                role=role_sdk,
                                parts=[genai.types.Part.from_text(text=m["content"])]
                            ))

                        # Inicializa o cliente usando a chave ativa da barra lateral e o modelo recomendado
                        client = genai.Client(api_key=api_key_usuario)
                        
                        # Inicia o chat com as diretrizes do sistema e histórico prévio
                        chat = client.chats.create(
                            model="gemini-2.5-flash",
                            config=genai.types.GenerateContentConfig(
                                system_instruction=contexto_sistema,
                                temperature=0.7
                            ),
                            history=historico_formatated
                        )
                        
                        # Envia a pergunta do usuário e obtém a resposta
                        resposta = chat.send_message(prompt)
                        texto_final = resposta.text
                        
                        # Renderiza o texto gerado na tela
                        placeholder_resposta.write(texto_final)
                        state.historico_ia.append({"role": "assistant", "content": texto_final})
                        
                except Exception as e:
                    placeholder_resposta.error(f"Ocorreu um erro ao falar com a IA: {e}")

# ==========================================
# PAGINA: TAREFAS
# ==========================================

elif pagina == "✅ Tarefas":
    st.header("✅ Área de Tarefas")

    # Função de Callback para remover tarefas por ID único de forma limpa e otimizada
    def remover_tarefa(id_tarefa):
        state.tarefas = [t for t in state.tarefas if t["id"] != id_tarefa]
        st.toast("Tarefa removida! 🗑️")

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

# ==========================================
# PAGINA: FINANÇAS
# ==========================================

elif pagina == "💰 Finanças":
    st.header("💰 Controle Financeiro")

    def remover_gasto(id_gasto):
        state.gastos = [g for g in state.gastos if g["id"] != id_gasto]
        st.toast("Gasto removido! 🗑️")

    def limpar_todos_gastos():
        state.gastos = []
        st.toast("Histórico de finanças limpo! 🧹")

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
                valor_formatado = f"R$ {gasto['Valor']:.2f}".replace('.', ',')
                col_val.markdown(f"<div class='item-custom'>{valor_formatado}</div>", unsafe_allow_html=True)
                col_btn.button("🗑️", key=f"del_fin_{gasto['id']}", on_click=remover_gasto, args=[gasto['id']])
            
            st.write("")
            st.button("🧹 Limpar Histórico Completo", on_click=limpar_todos_gastos)

        with col_grafico:
            st.subheader("📊 Gastos por Categoria")
            df_categoria = df.groupby("Categoria")["Valor"].sum().reset_index()
            fig = px.pie(df_categoria, values="Valor", names="Categoria", hole=0.4, color_discrete_sequence=px.colors.sequential.Purples_r)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=20, b=20, l=20, r=20), legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
            st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PAGINA: NOTAS
# ==========================================

elif pagina == "📓 Notas":
    st.header("📓 Bloco de Notas")
    st.caption("Guarde suas ideias, rascunhos e anotações rápidas")

    def remover_nota(id_nota):
        state.notas = [n for n in state.notas if n["id"] != id_nota]
        st.toast("Nota excluída! 🗑️")

    with st.form("form_nota", border=False):
        tit_nota = st.text_input("Título da Nota (Opcional)", placeholder="Ex: Ideias para o projeto")
        cont_nota = st.text_area("Conteúdo da Nota", placeholder="Digite sua anotação aqui...", height=150)
        
        if st.form_submit_button("Salvar Nota"):
            if cont_nota != "":
                titulo_final = tit_nota.strip() if tit_nota.strip() != "" else "Nota sem título"
                state.notas.append({
                    "id": str(uuid.uuid4()),
                    "titulo": titulo_final,
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
                st.markdown(f"""
                <div class='nota-container'>
                    <h3 style='color:#a855f7; margin-top:0; margin-bottom:10px;'>{nota['titulo']}</h3>
                    <p style='color:#e2e8f0; white-space: pre-wrap; font-size:15px; line-height:1.5;'>{nota['conteudo']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.button("🗑️ Excluir Nota", key=f"del_nota_{nota['id']}", on_click=remover_nota, args=[nota['id']])
                st.write("") 
    else:
        st.info("Nenhuma nota criada ainda.")

# ==========================================
# PAGINA: TO-DO LIST
# ==========================================

elif pagina == "📝 To-do List":
    @dataclass
    class Todo:
        text: str
        is_done: bool = False
        uid: uuid.UUID = field(default_factory=uuid.uuid4)

    if "todos" not in state:
        state.todos = [
            Todo(text="Comprar leite"),
            Todo(text="Lavar louça"),
            Todo(text="Estudar Python")
        ]

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

    st.title("📝 To-do List")
    with st.form(key="new_item_form", border=False):
        st.text_input("Nova tarefa", key="new_item_text")
        st.form_submit_button("Adicionar", on_click=add_todo)

    if state.todos:
        for i, todo in enumerate(state.todos):
            col1, col2 = st.columns([8,1])
            with col1:
                st.checkbox(todo.text, value=todo.is_done, on_change=check_todo, args=[i, not todo.is_done], key=f"todo-{todo.uid}")
            with col2:
                st.button("🗑️", on_click=remove_todo, args=[i], key=f"delete_{i}")
        st.button("Apagar concluídas", on_click=delete_all_checked)
    else:
        st.info("Nenhuma tarefa cadastrada.")

# ==========================================
# PAGINA: POMODORO
# ==========================================

elif pagina == "⏱️ Pomodoro":
    st.header("⏱️ Cronômetro Pomodoro")
    st.caption("Controle seu tempo de estudo de forma eficiente com pausas programadas.")

    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric(label="🎓 Total de Tempo Estudado", value=f"{state.tempo_estudado} min")
    with col_stat2:
        st.metric(label="🔄 Ciclos de Foco Completados", value=f"{state.tempo_estudado // 25}")

    st.divider()

    modo_selecionado = st.radio("Selecione o modo:", ["🎯 Foco (25 min)", "☕ Pausa Curta (5 min)"], horizontal=True)
    
    if modo_selecionado != state.modo_atual:
        state.modo_atual = modo_selecionado
        state.pomodoro_segundos_restantes = 25 * 60 if "Foco" in modo_selecionado else 5 * 60
        state.pomodoro_rodando = False

    texto_cronometro = st.empty()

    c_btn1, c_btn2, c_btn3 = st.columns([1, 1, 4])

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
    
    elif state.pomodoro_segundos_restantes == 0:
        state.pomodoro_rodando = False
        if "Foco" in state.modo_atual:
            state.tempo_estudado += 25  
            st.balloons()
            st.success("Excelente! +25 minutos computados no seu painel. Descanse um pouco!")
            state.modo_atual = "☕ Pausa Curta (5 min)"
            state.pomodoro_segundos_restantes = 5 * 60
        else:
            st.toast("Fim do descanso! 🎯")
            st.success("Pausa finalizada! Pronto para focar novamente?")
            state.modo_atual = "🎯 Foco (25 min)"
            state.pomodoro_segundos_restantes = 25 * 60
        st.rerun()
        
    else:
        mins, segs = divmod(state.pomodoro_segundos_restantes, 60)
        texto_cronometro.markdown(f"<div class='pomodoro-display'>{mins:02d}:{segs:02d}</div>", unsafe_allow_html=True)
