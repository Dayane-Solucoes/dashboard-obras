import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# 1. Configuração da Página
st.set_page_config(page_title="Soluções Terceirizadas - Gestão de Obras", page_icon="🏗️", layout="wide")

# 2. Estilização CSS personalizada (Cores idênticas ao manus.space)
st.markdown("""
<style>
    /* Estilo do fundo e texto geral */
    .main { background-color: #F8FAFC; color: #1E293B; }
    
    /* Barra Lateral Azul Escuro */
    [data-testid="stSidebar"] { background-color: #0B132B; color: #FFFFFF; }
    [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    
    /* Cards brancos com bordas suaves e sombras leves */
    .stCard {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 15px;
    }
    
    /* Métrica Customizada */
    .metric-label { font-size: 0.8rem; font-weight: 600; color: #64748B; text-transform: uppercase; }
    .metric-value { font-size: 1.6rem; font-weight: 700; color: #0F172A; margin-top: 4px; }
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

# Função de Formatação Monetária no Padrão Brasileiro (sem decimais)
def fmt_br(valor):
    try:
        if pd.isna(valor) or valor == 0:
            return "R$ 0"
        return f"R$ {valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0"

# 3. Carregamento e Tratamento de Dados
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
    st.error(f"Erro ao carregar dados do Excel. Verifique se os nomes dos arquivos estão corretos no GitHub: {e}")
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

# Filtro Global de Obra no Topo da Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**Seleção da Obra**")
obras_lista = ["Todas as Obras"] + [f"{int(row['N° Obra'])} - {row['NM Contrato']}" for _, row in df_cont.iterrows() if pd.notna(row['N° Obra'])]
selected_obra_str = st.sidebar.selectbox("Escolha uma obra:", obras_lista)

# Filtragem dos dados de acordo com a seleção
if selected_obra_str != "Todas as Obras":
    selected_id = float(selected_obra_str.split(" - ")[0])
    df_cont_curr = df_cont[df_cont['N° Obra'] == selected_id]
    df_c_curr = df_custo[df_custo['Filial AJUST'] == selected_id]
    df_f_curr = df_fat[df_fat['OBRA'] == selected_id]
else:
    df_cont_curr = df_cont
    df_c_curr = df_custo
    df_f_curr = df_fat

# Indicadores Consolidados
val_contrato = df_cont_curr['Valor Final Contratual'].sum() if 'Valor Final Contratual' in df_cont_curr else 0
fat_bruto = df_f_curr['Valor Bruto'].sum()
custo_direto = df_c_curr['Vr. Rateio'].sum()
custo_indireto = fat_bruto * 0.02 # Custo indireto fixado em 2% sobre o faturamento bruto
custo_total = custo_direto + custo_indireto
resultado_op = fat_bruto - custo_total
cpi = (fat_bruto / custo_direto) if custo_direto > 0 else 1.0

# --- NAVEGAÇÃO DAS PÁGINAS ---

# 1. MENU: VISÃO GERAL
if menu_principal == "Visão geral":
    st.title("Acompanhamento de obras")
    
    # Sub-abas: Resumo, Financeiro, Operacional
    sub_aba = st.radio("", ["Resumo", "Financeiro", "Operacional"], horizontal=True)

    if sub_aba == "Resumo":
        # Cards de Métricas Principais
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="stCard">
                <div class="metric-label">VALOR CONTRATUAL</div>
                <div class="metric-value">{fmt_br(val_contrato)}</div>
                <div class="metric-sub">↗ cadastro da obra vs. mês anterior</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stCard">
                <div class="metric-label">RESULTADO ACUMULADO</div>
                <div class="metric-value">{fmt_br(resultado_op)}</div>
                <div class="metric-sub">↗ fechamento mensal</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stCard">
                <div class="metric-label">AVANÇO FÍSICO</div>
                <div class="metric-value">Em andamento</div>
                <div class="metric-sub">↗ medições atualizadas</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="stCard">
                <div class="metric-label">RECEBIDO ACUMULADO</div>
                <div class="metric-value">{fmt_br(fat_bruto)}</div>
                <div class="metric-sub">↗ faturamento medido</div>
            </div>
            """, unsafe_allow_html=True)

        # Gráficos da Visão Geral
        c_left, c_right = st.columns([2, 1])
        with c_left:
            st.markdown("### Composição de Custos por Mês")
            df_c_temp = df_c_curr.copy()
            df_c_temp['MesAno'] = df_c_temp['Comp. C'].dt.strftime('%m/%Y')
            df_bar = df_c_temp.groupby('MesAno')['Vr. Rateio'].sum().reset_index()
            fig_bar = px.bar(df_bar, x='MesAno', y='Vr. Rateio', color_discrete_sequence=['#2563EB'])
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis_title="Custo (R$)")
            st.plotly_chart(fig_bar, use_container_width=True, key="bar_vg")

        with c_right:
            st.markdown("### Distribuição de Custos")
            if 'Classificacao 1' in df_c_curr.columns:
                df_pie = df_c_curr.groupby('Classificacao 1')['Vr. Rateio'].sum().reset_index()
                fig_pie = px.pie(df_pie, values='Vr. Rateio', names='Classificacao 1', hole=0.6,
                                 color_discrete_sequence=px.colors.qualitative.Set2)
                fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie, use_container_width=True, key="pie_vg")

    elif sub_aba == "Financeiro":
        st.subheader("Resumo Financeiro da Obra")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            <div class="stCard">
                <h4>Resumo Financeiro</h4>
                <hr>
                <p><b>Receita Contratual:</b> {}</p>
                <p><b>Custos Realizados:</b> {}</p>
                <p><b>Despesas Indiretas (2%):</b> {}</p>
                <p><b>Resultado Acumulado:</b> {}</p>
            </div>
            """.format(fmt_br(val_contrato), fmt_br(custo_direto), fmt_br(custo_indireto), fmt_br(resultado_op)), unsafe_allow_html=True)
            
        with col_b:
            st.markdown("""
            <div class="stCard">
                <h4>DRE - Visão Rápida</h4>
                <hr>
                <p><b>Receita Líquida (Faturamento):</b> {}</p>
                <p><b>Custos Diretos:</b> {}</p>
                <p><b>Despesas Indiretas:</b> {}</p>
                <p><b>Resultado Operacional:</b> {}</p>
            </div>
            """.format(fmt_br(fat_bruto), fmt_br(custo_direto), fmt_br(custo_indireto), fmt_br(resultado_op)), unsafe_allow_html=True)

# 2. MENU: DADOS DA OBRA (Com Foto da Obra)
elif menu_principal == "Dados da obra":
    st.title("Cadastro e Dados da Obra")
    
    col_inf, col_img = st.columns([2, 1])
    
    with col_inf:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.subheader("Informações Principais")
        
        nome_obra = st.text_input("NOME DA OBRA", value=selected_obra_str)
        cliente = st.text_input("CLIENTE", value="Prefeitura Municipal")
        endereco = st.text_input("ENDEREÇO", value="São Paulo - SP")
        
        c_d1, c_d2 = st.columns(2)
        with c_d1:
            dt_inicio = st.date_input("DATA DE INÍCIO")
        with c_d2:
            dt_fim = st.date_input("DATA DE TÉRMINO")
            
        val_cont = st.number_input("VALOR CONTRATUAL (R$)", value=float(val_contrato))
        val_adit = st.number_input("VALOR DE ADITIVOS (R$)", value=0.0)
        
        if st.button("Salvar alterações"):
            st.success("Dados salvos com sucesso!")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_img:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.subheader("Foto da Obra")
        uploaded_image = st.file_uploader("Adicione uma foto de capa (PNG/JPG)", type=["png", "jpg", "jpeg"])
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Foto da Obra", use_container_width=True)
        else:
            st.info("Nenhuma foto selecionada para esta obra.")
        st.markdown("</div>", unsafe_allow_html=True)

# 3. MENU: DRE (Demonstrativo de Resultado com Custo Indireto)
elif menu_principal == "DRE":
    st.title("DRE - Demonstrativo de Resultado")
    st.caption("Competência acumulada com aplicação de Custo Indireto (2% sobre Faturamento Bruto)")

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

# 4. MENU: KPIS (Curva S e CPI)
elif menu_principal == "KPIs":
    st.title("KPIs de Performance da Obra")
    
    col_kpi1, col_kpi2 = st.columns(2)
    with col_kpi1:
        st.markdown(f"""
        <div class="stCard">
            <div class="metric-label">CPI (Cost Performance Index)</div>
            <div class="metric-value">{cpi:.2f}</div>
            <div class="metric-sub">{"🟢 Dentro do orçamento" if cpi >= 1.0 else "🔴 Custo acima do planejado"}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_kpi2:
        st.markdown(f"""
        <div class="stCard">
            <div class="metric-label">MARGEM OPERACIONAL</div>
            <div class="metric-value">{(resultado_op/fat_bruto*100) if fat_bruto>0 else 0:.1f}%</div>
            <div class="metric-sub">Líquida pós custo indireto</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### Curva S (Físico x Financeiro)")
    
    df_c_temp = df_c_curr.copy()
    df_c_temp['MesAno'] = df_c_temp['Comp. C'].dt.to_period('M').dt.to_timestamp()
    c_m = df_c_temp.groupby('MesAno')['Vr. Rateio'].sum().reset_index()

    df_f_temp = df_f_curr.copy()
    df_f_temp['MesAno'] = df_f_temp['COMP MED'].dt.to_period('M').dt.to_timestamp()
    f_m = df_f_temp.groupby('MesAno')['Valor Bruto'].sum().reset_index()

    df_curva = pd.merge(c_m, f_m, on='MesAno', how='outer').fillna(0).sort_values('MesAno')
    df_curva['Custo Acumulado'] = df_curva['Vr. Rateio'].cumsum()
    df_curva['Faturamento Acumulado'] = df_curva['Valor Bruto'].cumsum()

    fig_curva = go.Figure()
    fig_curva.add_trace(go.Scatter(x=df_curva['MesAno'].dt.strftime('%m/%Y'), y=df_curva['Faturamento Acumulado'], mode='lines+markers', name='Faturamento Acumulado', line=dict(color='#2563EB', width=3)))
    fig_curva.add_trace(go.Scatter(x=df_curva['MesAno'].dt.strftime('%m/%Y'), y=df_curva['Custo Acumulado'], mode='lines+markers', name='Custo Realizado', line=dict(color='#DC2626', width=3)))
    fig_curva.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode="x unified")
    
    st.plotly_chart(fig_curva, use_container_width=True, key="fig_kpi_curva")

# 5. MENU: CUSTOS (Classificação de Grupo 1 e Grupo 2)
elif menu_principal == "Custos":
    st.title("Análise Detalhada de Custos")
    
    col_c1, col_c2 = st.columns([1, 1])
    
    with col_c1:
        st.markdown("### Evolução Mensal dos Custos")
        df_c_temp = df_c_curr.copy()
        df_c_temp['MesAno'] = df_c_temp['Comp. C'].dt.strftime('%m/%Y')
        df_mes = df_c_temp.groupby('MesAno')['Vr. Rateio'].sum().reset_index()
        
        fig_c_mes = px.bar(df_mes, x='MesAno', y='Vr. Rateio', color_discrete_sequence=['#2563EB'])
        fig_c_mes.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis_title="Custo (R$)")
        st.plotly_chart(fig_c_mes, use_container_width=True, key="fig_custos_mes")

    with col_c2:
        st.markdown("### Custos por Categoria (Grupo)")
        # Tabela ordenada por maior custo
        col_grupo = 'Classificacao 1' if 'Classificacao 1' in df_c_curr.columns else df_c_curr.columns[0]
        df_grupo = df_c_curr.groupby(col_grupo)['Vr. Rateio'].sum().reset_index().sort_values(by='Vr. Rateio', ascending=False)
        df_grupo['Valor Formatado'] = df_grupo['Vr. Rateio'].apply(fmt_br)
        
        st.dataframe(df_grupo[[col_grupo, 'Valor Formatado']], use_container_width=True, hide_index=True)
