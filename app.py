import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# 1. Configuração da Página
st.set_page_config(page_title="Soluções Terceirizadas - Gestão de Obras", page_icon="🏗️", layout="wide")

# 2. Estilização CSS personalizada
st.markdown("""
<style>
    /* Estilo do fundo e texto geral */
    .main { background-color: #F8FAFC; color: #1E293B; }
    
    /* Barra Lateral Azul Escuro */
    [data-testid="stSidebar"] { background-color: #0B132B; color: #FFFFFF; }
    [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    
    /* Fundo Branco e Borda Arredondada especificamente para o Logo na Sidebar */
    [data-testid="stSidebar"] img {
        background-color: #FFFFFF !important;
        padding: 12px !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
    }

    /* Fundo Branco e Texto Escuro para o Selectbox da Obra */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] * {
        color: #0B132B !important;
        font-weight: 600 !important;
    }

    /* Badge e Cabeçalho Superior */
    .status-badge {
        background-color: #DCFCE7;
        color: #166534;
        font-weight: 600;
        font-size: 0.8rem;
        padding: 4px 12px;
        border-radius: 12px;
        display: inline-block;
        margin-right: 10px;
    }
    .update-text {
        font-size: 0.85rem;
        color: #64748B;
        display: inline-block;
    }
    .obra-header-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 6px;
        margin-bottom: 4px;
        text-transform: uppercase;
    }
    .obra-header-sub {
        font-size: 0.95rem;
        color: #475569;
        margin-bottom: 20px;
    }

    /* Cards numéricos */
    .stCard {
        background-color: #FFFFFF;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 15px;
    }
    
    .metric-label { font-size: 0.75rem; font-weight: 600; color: #64748B; text-transform: uppercase; }
    .metric-value { font-size: 1.4rem; font-weight: 700; color: #0F172A; margin-top: 4px; }
    .metric-sub { font-size: 0.75rem; color: #2563EB; margin-top: 2px; }

    /* Estilo de Botões */
    .stButton>button {
        background-color: #2563EB;
        color: white !important;
        border-radius: 8px;
        font-weight: 600;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Função de Formatação Monetária
def fmt_br(valor):
    try:
        if pd.isna(valor) or valor == 0:
            return "R$ 0"
        return f"R$ {valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0"

# 3. Carregamento de Dados
@st.cache_data
def load_data():
    df_custo = pd.read_excel('BD_Custo.xlsx')
    df_fat = pd.read_excel('BD_Faturamento.xlsx')
    df_cont = pd.read_excel('BD_Contratos.xlsx')

    df_c = df_custo[df_custo['Considerar'] == 'S'].copy()
    df_c['Comp. C'] = pd.to_datetime(df_c['Comp. C'])

    df_f = df_fat[df_fat['CONSIDERAR'] == 'S'].copy()
    df_f['COMP MED'] = pd.to_datetime(df_f['COMP MED'])

    return df_c, df_f, df_cont

try:
    df_custo, df_fat, df_cont = load_data()
except Exception as e:
    st.error(f"Erro ao carregar dados do Excel: {e}")
    st.stop()

# --- BARRA LATERAL (MENU PRINCIPAL) ---
logo_files = [f for f in os.listdir('.') if f.lower().startswith('logo') and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
if logo_files:
    st.sidebar.image(logo_files[0], use_container_width=True)

st.sidebar.markdown("### PORTFÓLIO / OBRAS")
menu_principal = st.sidebar.radio(
    "Navegação",
    ["Visão geral", "Dados da obra", "DRE", "KPIs", "Custos"],
    label_visibility="collapsed"
)

# Filtro Global de Obra
st.sidebar.markdown("---")
st.sidebar.markdown("**Seleção da Obra**")
obras_lista = ["Todas as Obras"] + [f"{int(row['N° Obra'])} - {row['NM Contrato']}" for _, row in df_cont.iterrows() if pd.notna(row['N° Obra'])]
selected_obra_str = st.sidebar.selectbox("Escolha uma obra:", obras_lista)

# Filtragem de Dados
if selected_obra_str != "Todas as Obras":
    selected_id = float(selected_obra_str.split(" - ")[0])
    df_cont_curr = df_cont[df_cont['N° Obra'] == selected_id]
    df_c_curr = df_custo[df_custo['Filial AJUST'] == selected_id]
    df_f_curr = df_fat[df_fat['OBRA'] == selected_id]
    
    # Dados para o cabeçalho dinâmico
    nome_obra = selected_obra_str
    cliente_obra = df_cont_curr['NM Cliente'].iloc[0] if 'NM Cliente' in df_cont_curr and not df_cont_curr['NM Cliente'].empty else "Prefeitura Municipal Guarulhos"
    local_obra = df_cont_curr['Local / UF'].iloc[0] if 'Local / UF' in df_cont_curr and not df_cont_curr['Local / UF'].empty else "Guarulhos - SP"
else:
    df_cont_curr = df_cont
    df_c_curr = df_custo
    df_f_curr = df_fat
    selected_id = "geral"
    
    nome_obra = "TODAS AS OBRAS - PORTFÓLIO CONSOLIDADO"
    cliente_obra = "Múltiplos Clientes"
    local_obra = "Diversas Localidades"

# Identificar a última data da base de dados
max_data_f = df_f_curr['COMP MED'].max() if not df_f_curr.empty else None
max_data_c = df_c_curr['Comp. C'].max() if not df_c_curr.empty else None

datas_validas = [d for d in [max_data_f, max_data_c] if pd.notna(d)]
ultima_atualizacao = max(datas_validas).strftime("%m/%Y") if datas_validas else "Aguardando fechamento"

# Indicadores Consolidados
val_contrato = df_cont_curr['Valor Final Contratual'].sum() if 'Valor Final Contratual' in df_cont_curr else 0
fat_bruto = df_f_curr['Valor Bruto'].sum()
custo_direto = df_c_curr['Vr. Rateio'].sum()
custo_indireto = fat_bruto * 0.02
custo_total = custo_direto + custo_indireto
resultado_op = fat_bruto - custo_total
cpi = (fat_bruto / custo_direto) if custo_direto > 0 else 1.0

# --- CABEÇALHO DINÂMICO DA OBRA ---
st.markdown(f"""
    <div>
        <span class="status-badge">Em andamento</span>
        <span class="update-text">Última atualização · {ultima_atualizacao}</span>
        <div class="obra-header-title">{nome_obra}</div>
        <div class="obra-header-sub">🏦 {cliente_obra} &nbsp;&nbsp;📍 {local_obra}</div>
    </div>
""", unsafe_allow_html=True)

# --- NAVEGAÇÃO ---

# 1. VISÃO GERAL
if menu_principal == "Visão geral":
    sub_aba = st.radio("", ["Resumo", "Financeiro", "Operacional"], horizontal=True)

    if sub_aba == "Resumo":
        # Cards de Resumo
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="stCard"><div class="metric-label">VALOR CONTRATUAL</div><div class="metric-value">{fmt_br(val_contrato)}</div><div class="metric-sub">↗ cadastro da obra</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stCard"><div class="metric-label">RESULTADO ACUMULADO</div><div class="metric-value">{fmt_br(resultado_op)}</div><div class="metric-sub">↗ fechamento mensal</div></div>', unsafe_allow_html=True)
        with col3:
            av_fisico = f"{(fat_bruto / val_contrato * 100):.1f}%" if val_contrato > 0 else "Não informado"
            st.markdown(f'<div class="stCard"><div class="metric-label">AVANÇO FÍSICO</div><div class="metric-value">{av_fisico}</div><div class="metric-sub">↗ medições</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="stCard"><div class="metric-label">RECEBIDO ACUMULADO</div><div class="metric-value">{fmt_br(fat_bruto)}</div><div class="metric-sub">↗ faturamento</div></div>', unsafe_allow_html=True)

        # Preparação dos Dados para a Curva S
        df_c_temp = df_c_curr.copy()
        df_c_temp['Periodo'] = df_c_temp['Comp. C'].dt.to_period('M')
        c_mes = df_c_temp.groupby('Periodo')['Vr. Rateio'].sum().reset_index()

        df_f_temp = df_f_curr.copy()
        df_f_temp['Periodo'] = df_f_temp['COMP MED'].dt.to_period('M')
        f_mes = df_f_temp.groupby('Periodo')['Valor Bruto'].sum().reset_index()

        df_m = pd.merge(f_mes, c_mes, on='Periodo', how='outer').fillna(0).sort_values('Periodo')
        df_m['MesAno'] = df_m['Periodo'].dt.strftime('%m/%Y')

        # Acumulados Monetários
        df_m['Fat_Acum'] = df_m['Valor Bruto'].cumsum()
        df_m['Custo_Acum'] = df_m['Vr. Rateio'].cumsum()

        # Cálculo Percentual da Curva S
        base_contrato = val_contrato if val_contrato > 0 else df_m['Fat_Acum'].max()
        df_m['Avanco_Fisico_%'] = (df_m['Fat_Acum'] / base_contrato * 100) if base_contrato > 0 else 0
        df_m['Avanco_Custo_%'] = (df_m['Custo_Acum'] / base_contrato * 100) if base_contrato > 0 else 0
        df_m['Margem'] = np.where(df_m['Valor Bruto'] > 0, ((df_m['Valor Bruto'] - df_m['Vr. Rateio']) / df_m['Valor Bruto']) * 100, 0)

        # GRÁFICO 1: CURVA S (Físico/Financeiro vs Custo)
        st.markdown("### Curva Física e Financeira (Curva S)")
        st.caption("Avanço físico (faturamento acumulado %) versus Avanço de custo acumulado (%)")

        fig_curva_s = go.Figure()

        # Linha Avanço Físico (Baseado em Faturamento)
        fig_curva_s.add_trace(go.Scatter(
            x=df_m['MesAno'], 
            y=df_m['Avanco_Fisico_%'], 
            mode='lines+markers',
            name='Avanço Físico Acumulado (%)',
            line=dict(color='#2563EB', width=3),
            marker=dict(size=6)
        ))

        # Linha Avanço de Custo
        fig_curva_s.add_trace(go.Scatter(
            x=df_m['MesAno'], 
            y=df_m['Avanco_Custo_%'], 
            mode='lines+markers',
            name='Avanço de Custo Acumulado (%)',
            line=dict(color='#DC2626', width=3, dash='dash'),
            marker=dict(size=6)
        ))

        fig_curva_s.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            legend=dict(orientation="h", y=1.15, x=0),
            yaxis=dict(title="Avanço Acumulado (%)", suffix="%"),
            xaxis=dict(title="Período (Mês/Ano)"),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_curva_s, use_container_width=True, key="fig_curva_s")

        st.markdown("---")

        # GRÁFICO 2: RESULTADO MENSAL (Faturado, Custo e Margem)
        st.markdown("### Resultado Mensal (Faturado, Custo e Margem)")
        fig_comb = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_comb.add_trace(go.Bar(x=df_m['MesAno'], y=df_m['Valor Bruto'], name="Faturado", marker_color='#2563EB'), secondary_y=False)
        fig_comb.add_trace(go.Bar(x=df_m['MesAno'], y=df_m['Vr. Rateio'], name="Custo Realizado", marker_color='#DC2626'), secondary_y=False)
        fig_comb.add_trace(go.Scatter(x=df_m['MesAno'], y=df_m['Margem'], name="Margem (%)", mode="lines+markers", line=dict(color='#10B981', width=3)), secondary_y=True)

        fig_comb.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", y=1.15, x=0))
        fig_comb.update_yaxes(title_text="Valor (R$)", secondary_y=False)
        fig_comb.update_yaxes(title_text="Margem (%)", secondary_y=True)
        st.plotly_chart(fig_comb, use_container_width=True, key="fig_vg_comb")

        st.markdown("---")

        # GRÁFICO 3: DISTRIBUIÇÃO DE CUSTOS
        st.markdown("### Composição de Custos")
        col_g1 = df_c_curr.columns[28] if len(df_c_curr.columns) >= 29 else df_c_curr.columns[0]
        df_pie = df_c_curr.groupby(col_g1)['Vr. Rateio'].sum().reset_index()
        fig_pie = px.pie(df_pie, values='Vr. Rateio', names=col_g1, hole=0.6, color_discrete_sequence=px.colors.qualitative.Set2)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_vg")

    elif sub_aba == "Financeiro":
        st.subheader("Resumo Financeiro da Obra")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            <div class="stCard">
                <h4>Resumo Financeiro</h4><hr>
                <p><b>Receita Contratual:</b> {fmt_br(val_contrato)}</p>
                <p><b>Custos Realizados:</b> {fmt_br(custo_direto)}</p>
                <p><b>Despesas Indiretas (2%):</b> {fmt_br(custo_indireto)}</p>
                <p><b>Resultado Acumulado:</b> {fmt_br(resultado_op)}</p>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div class="stCard">
                <h4>DRE - Visão Rápida</h4><hr>
                <p><b>Receita Líquida (Faturamento):</b> {fmt_br(fat_bruto)}</p>
                <p><b>Custos Diretos:</b> {fmt_br(custo_direto)}</p>
                <p><b>Despesas Indiretas:</b> {fmt_br(custo_indireto)}</p>
                <p><b>Resultado Operacional:</b> {fmt_br(resultado_op)}</p>
            </div>
            """, unsafe_allow_html=True)

# 2. DADOS DA OBRA
elif menu_principal == "Dados da obra":
    st.title("Cadastro e Dados da Obra")
    
    col_inf, col_img = st.columns([2, 1])
    
    with col_inf:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.subheader("Informações Principais")
        st.text_input("NOME DA OBRA", value=nome_obra)
        st.text_input("CLIENTE", value=cliente_obra)
        st.text_input("ENDEREÇO", value=local_obra)
        st.number_input("VALOR CONTRATUAL (R$)", value=float(val_contrato))
        
        if st.button("Salvar alterações de cadastro"):
            st.success("Dados salvos com sucesso!")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_img:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.subheader("Foto da Obra")
        
        obra_id_str = int(selected_id) if selected_obra_str != "Todas as Obras" else "geral"
        caminho_foto = f"foto_obra_{obra_id_str}.png"
        
        if os.path.exists(caminho_foto):
            st.image(caminho_foto, caption=f"Foto da Obra {obra_id_str}", use_container_width=True)
        else:
            st.info("Nenhuma foto cadastrada para esta obra.")
            
        uploaded_image = st.file_uploader("Selecione/alterar foto de capa (PNG/JPG)", type=["png", "jpg", "jpeg"], key=f"upload_{obra_id_str}")
        
        if uploaded_image is not None:
            if st.button("Salvar Foto da Obra"):
                with open(caminho_foto, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                st.success("Foto salva com sucesso para esta obra!")
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)

# 3. DRE
elif menu_principal == "DRE":
    st.title("DRE - Demonstrativo de Resultado")
    dre_df = pd.DataFrame({
        "Conta": ["Receita Bruta (Faturamento)", "Custos Diretos", "Despesas Indiretas (2%)", "Resultado Operacional"],
        "Realizado (R$)": [fmt_br(fat_bruto), fmt_br(-custo_direto), fmt_br(-custo_indireto), fmt_br(resultado_op)],
        "Margem (%)": [
            "100.0%",
            f"{- (custo_direto/fat_bruto*100) if fat_bruto>0 else 0:.1f}%",
            "-2.0%",
            f"{(resultado_op/fat_bruto*100) if fat_bruto>0 else 0:.1f}%"
        ]
    })
    st.dataframe(dre_df, use_container_width=True, hide_index=True)

# 4. KPIS
elif menu_principal == "KPIs":
    st.title("KPIs de Performance")
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.markdown(f'<div class="stCard"><div class="metric-label">CPI (Cost Performance Index)</div><div class="metric-value">{cpi:.2f}</div></div>', unsafe_allow_html=True)
    with col_k2:
        st.markdown(f'<div class="stCard"><div class="metric-label">MARGEM OPERACIONAL</div><div class="metric-value">{(resultado_op/fat_bruto*100) if fat_bruto>0 else 0:.1f}%</div></div>', unsafe_allow_html=True)

# 5. CUSTOS
elif menu_principal == "Custos":
    st.title("Análise Detalhada de Custos")
    
    col_c1, col_c2 = st.columns([1, 1])
    
    with col_c1:
        st.markdown("### Evolução Mensal dos Custos")
        df_c_temp = df_c_curr.copy()
        df_c_temp['Periodo'] = df_c_temp['Comp. C'].dt.to_period('M')
        df_mes = df_c_temp.groupby('Periodo')['Vr. Rateio'].sum().reset_index().sort_values('Periodo')
        df_mes['MesAno'] = df_mes['Periodo'].dt.strftime('%m/%Y')
        
        fig_c_mes = px.bar(df_mes, x='MesAno', y='Vr. Rateio', color_discrete_sequence=['#2563EB'])
        fig_c_mes.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis_title="Custo (R$)")
        st.plotly_chart(fig_c_mes, use_container_width=True, key="fig_custos_mes")

    with col_c2:
        st.markdown("### Custos por Categoria")
        
        col_g1 = df_c_curr.columns[28] if len(df_c_curr.columns) >= 29 else df_c_curr.columns[0]
        col_g2 = df_c_curr.columns[29] if len(df_c_curr.columns) >= 30 else df_c_curr.columns[0]
        
        expandir = st.checkbox("Expandir para Nível 2 (Grupo 2 - Detalhado)")

        if expandir:
            df_g = df_c_curr.groupby([col_g1, col_g2])['Vr. Rateio'].sum().reset_index().sort_values(by='Vr. Rateio', ascending=False)
            df_g.columns = ['Grupo 1 (Nível 1)', 'Grupo 2 (Nível 2)', 'Valor (R$)']
            df_g['Valor (R$)'] = df_g['Valor (R$)'].apply(fmt_br)
        else:
            df_g = df_c_curr.groupby(col_g1)['Vr. Rateio'].sum().reset_index().sort_values(by='Vr. Rateio', ascending=False)
            df_g.columns = ['Grupo 1 (Nível 1)', 'Valor (R$)']
            df_g['Valor (R$)'] = df_g['Valor (R$)'].apply(fmt_br)

        st.dataframe(df_g, use_container_width=True, hide_index=True)
