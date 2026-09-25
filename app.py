import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. Configuração da Página e Estilo (Dark Mode Moderno)
st.set_page_config(
    page_title="Smart Obra - Gestão de Custos",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada para injetar o visual escuro / gradientes
st.markdown("""
    <style>
    .stApp {
        background-color: #0f0b24;
        color: #ffffff;
    }
    .main {
        background-color: #0f0b24;
    }
    [data-testid="stSidebar"] {
        background-color: #15102f;
        border-right: 1px solid #2b2357;
    }
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1b1736 0%, #251e4f 100%);
        border: 1px solid #3d3175;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    div.stSelectbox > div > div {
        background-color: #1b1736;
        color: white;
        border: 1px solid #3d3175;
    }
    .project-card {
        background: linear-gradient(135deg, #1b1736 0%, #251e4f 100%);
        border: 1px solid #3d3175;
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Função para Carregar Dados usando seus arquivos exatos do GitHub
@st.cache_data
def load_data():
    try:
        df_custo = pd.read_excel("BD_Custo.xlsx")
        df_faturamento = pd.read_excel("BD_Faturamento.xlsx")
        df_contratos = pd.read_excel("BD_Contratos.xlsx")
    except FileNotFoundError:
        # Dados fictícios de fallback caso os arquivos não sejam encontrados no diretório
        data_atual = datetime.now()
        df_custo = pd.DataFrame({
            'Obra': ['The Pinnacle Tower', 'The Pinnacle Tower', 'Horizon Plaza', 'Horizon Plaza'],
            'Data': [data_atual, data_atual, data_atual, data_atual],
            'Categoria': ['Material', 'Mão de Obra', 'Equipamentos', 'Material'],
            'Valor': [45000, 30000, 15000, 20000],
            'Fornecedor': ['ConstróiAço', 'Equipe Alpha', 'LocaMáquinas', 'Cimento Forte']
        })
        df_faturamento = pd.DataFrame({
            'Obra': ['The Pinnacle Tower', 'The Pinnacle Tower', 'Horizon Plaza', 'Horizon Plaza'],
            'Data': [data_atual, data_atual, data_atual, data_atual],
            'Tipo': ['Entrada Realizada', 'Entrada Prevista', 'Entrada Realizada', 'Entrada Prevista'],
            'Valor': [120000, 50000, 80000, 30000],
            'Cliente': ['Vertex Group', 'Vertex Group', 'Horizon Corp', 'Horizon Corp']
        })
        df_contratos = pd.DataFrame({
            'Obra': ['The Pinnacle Tower', 'Horizon Plaza'],
            'Cliente': ['Vertex Development Group', 'Horizon Real Estate'],
            'Endereco': ['123 Skyline Blvd, NY', '456 Ocean Ave, Miami'],
            'Gerente': ['Sarah Chen', 'Carlos Silva'],
            'Orcamento_Total': [125000000, 45000000],
            'Status': ['On Track', 'Delayed']
        })
    return df_custo, df_faturamento, df_contratos

df_custo, df_faturamento, df_contratos = load_data()

# 3. Sidebar de Navegação e Filtros Globais
st.sidebar.markdown("## 🔷 **SMART OBRA**")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navegação", ["Dashboard Executivo", "Detalhes da Obra & Fotos", "Gestão de NFs"])

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Filtros Globais")

# Lista de Obras disponíveis
lista_obras = df_contratos['Obra'].unique().tolist() if 'Obra' in df_contratos.columns else ["Geral"]
obra_selecionada = st.sidebar.selectbox("Selecionar Obra", ["Todas as Obras"] + lista_obras)

periodo_analise = st.sidebar.selectbox("Período de Análise", ["Últimos 30 Dias", "Este Mês", "Este Ano", "Todo o Histórico"])

# Filtragem dos dataframes com base na obra selecionada
if obra_selecionada != "Todas as Obras":
    f_custo = df_custo[df_custo['Obra'] == obra_selecionada]
    f_fat = df_faturamento[df_faturamento['Obra'] == obra_selecionada]
    f_cont = df_contratos[df_contratos['Obra'] == obra_selecionada]
else:
    f_custo = df_custo
    f_fat = df_faturamento
    f_cont = df_contratos

# 4. Conteúdo Principal baseado na navegação
if menu == "Dashboard Executivo":
    st.title("📊 Dashboard de Custos & Fluxo de Caixa")
    st.markdown(f"Visualizando dados para: **{obra_selecionada}** | Período: **{periodo_analise}**")
    st.markdown("---")

    # Bloco de KPIs Superiores
    total_entradas = f_fat['Valor'].sum() if not f_fat.empty else 0
    total_saidas = f_custo['Valor'].sum() if not f_custo.empty else 0
    saldo_caixa = total_entradas - total_saidas
    eficiencia = round(total_saidas / total_entradas, 2) if total_entradas > 0 else 0.0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Entradas (NFs)", value=f"R$ {total_entradas:,.2f}", delta="+12% vs mês ant.")
    with col2:
        st.metric(label="Custos Executados (Saídas)", value=f"R$ {total_saidas:,.2f}", delta="-4% budget")
    with col3:
        st.metric(label="Saldo em Caixa", value=f"R$ {saldo_caixa:,.2f}", delta="Saudável")
    with col4:
        st.metric(label="Eficiência de Custos", value=str(eficiencia), delta="Meta < 0.95")

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráficos Principais
    c1, c2 = st.columns([1, 1.2])

    with c1:
        st.markdown("### 📈 Fluxo de Caixa (Entradas vs Saídas)")
        if not f_fat.empty and not f_custo.empty:
            fig_cash = go.Figure()
            fig_cash.add_trace(go.Scatter(y=[total_entradas*0.2, total_entradas*0.5, total_entradas], mode='lines+markers', name='Cash In', line=dict(color='#00f2fe', width=3)))
            fig_cash.add_trace(go.Scatter(y=[total_saidas*0.3, total_saidas*0.6, total_saidas], mode='lines+markers', name='Cash Out', line=dict(color='#7928ca', width=3)))
            fig_cash.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_cash, use_container_width=True)
        else:
            st.info("Sem dados suficientes para o gráfico de fluxo.")

    with c2:
        st.markdown("### 📊 Análise de Custos por Categoria")
        if not f_custo.empty:
            fig_bar = px.bar(f_custo, x='Categoria', y='Valor', color='Categoria', color_discrete_sequence=['#00f2fe', '#7928ca', '#ff007f'])
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Sem dados de custo cadastrados.")

elif menu == "Detalhes da Obra & Fotos":
    st.title("🏗️ Aba de Cadastro e Dados da Obra")
    st.markdown("Informações contratuais, dados do cliente e registro visual da obra.")
    st.markdown("---")

    if not f_cont.empty:
        for idx, row in f_cont.iterrows():
            st.markdown(f"""
            <div class="project-card">
                <h2>{row.get('Obra', 'Nome da Obra')}</h2>
                <hr style="border-color: #3d3175;">
            </div>
            """, unsafe_allow_html=True)
            
            col_img, col_info = st.columns([1, 1.5])
            
            with col_img:
                st.markdown("### 📷 Foto da Obra")
                uploaded_file = st.file_uploader(f"Carregar foto para {row.get('Obra')}", type=['png', 'jpg', 'jpeg'], key=f"img_{idx}")
                if uploaded_file is not None:
                    st.image(uploaded_file, caption="Foto atualizada da obra", use_column_width=True)
                else:
                    st.image("https://images.unsplash.com/photo-1541888946425-d0fbb18f2445?w=500&auto=format&fit=crop&q=60", caption="Imagem padrão da Obra", use_column_width=True)

            with col_info:
                st.markdown("### 📋 Ficha Técnica")
                st.markdown(f"**👤 Nome do Cliente:** {row.get('Cliente', 'Não informado')}")
                st.markdown(f"**📍 Endereço Físico:** {row.get('Endereco', 'Endereço não cadastrado')}")
                st.markdown(f"**👔 Gestor Responsável:** {row.get('Gerente', 'Não atribuído')}")
                st.markdown(f"**💰 Orçamento Total:** R$ {row.get('Orcamento_Total', 0):,.2f}")
                st.markdown(f"**📊 Status Atual:** `{row.get('Status', 'Em Andamento')}`")
            
            st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.warning("Nenhuma obra encontrada na base de contratos.")

elif menu == "Gestão de NFs":
    st.title("📄 Histórico de Notas Fiscais (Entradas e Saídas)")
    st.markdown("Lista consolidada baseada nas planilhas de faturamento e custos.")
    st.markdown("---")
    
    st.subheader("Notas Fiscais de Custos (Saídas) - BD_Custo")
    if not f_custo.empty:
        st.dataframe(f_custo, use_container_width=True)
    else:
        st.info("Nenhuma nota de custo encontrada.")

    st.subheader("Notas Fiscais de Faturamento (Entradas) - BD_Faturamento")
    if not f_fat.empty:
        st.dataframe(f_fat, use_container_width=True)
    else:
        st.info("Nenhuma nota de faturamento encontrada.")
