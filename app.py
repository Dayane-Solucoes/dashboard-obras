import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Configuração da Página
st.set_page_config(page_title="Dashboard Executivo de Obras", page_icon="🏗️", layout="wide")

# Estilização CSS
st.markdown("""
<style>
    .metric-card { background-color: #1E222D; padding: 15px; border-radius: 10px; border-left: 5px solid #00D1B2; }
</style>
""", unsafe_allow_html=True)

# Função para formatar valores no padrão brasileiro sem centavos
def fmt_br(valor):
    try:
        return f"R$ {valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0"

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
    st.error(f"Erro ao carregar os arquivos de Excel. Verifique se os nomes dos arquivos no GitHub estão idênticos. Detalhes: {e}")
    st.stop()

# --- BARRA LATERAL (SIDEBAR) ---
# 1. LOGO DA EMPRESA
logo_path = 'logo.png' # Suporta logo.png, logo.jpg, logo.jpeg
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
elif os.path.exists('logo.jpg'):
    st.sidebar.image('logo.jpg', use_container_width=True)
elif os.path.exists('logo.jpeg'):
    st.sidebar.image('logo.jpeg', use_container_width=True)
else:
    st.sidebar.info("💡 Para exibir sua logo, envie um arquivo chamado 'logo.png' para o seu repositório no GitHub.")

st.sidebar.title("Filtros do Portfólio")
status_list = ["Todos"] + list(df_cont['Status'].dropna().unique())
selected_status = st.sidebar.selectbox("Status da Obra", status_list)

df_cont_filtered = df_cont[df_cont['Status'] == selected_status] if selected_status != "Todos" else df_cont
obras_disponiveis = df_cont_filtered['N° Obra'].dropna().unique()

obra_options = ["Todas as Obras"] + [f"{int(obra)} - {df_cont[df_cont['N° Obra']==obra]['NM Contrato'].values[0]}" for obra in obras_disponiveis if obra in df_cont['N° Obra'].values]
selected_obra_str = st.sidebar.selectbox("Selecione a Obra", obra_options)

if selected_obra_str != "Todas as Obras":
    selected_obra_id = float(selected_obra_str.split(" - ")[0])
    df_cont_curr = df_cont_filtered[df_cont_filtered['N° Obra'] == selected_obra_id]
    df_c_curr = df_custo[df_custo['Filial AJUST'] == selected_obra_id]
    df_f_curr = df_fat[df_fat['OBRA'] == selected_obra_id]
else:
    df_cont_curr = df_cont_filtered
    df_c_curr = df_custo[df_custo['Filial AJUST'].isin(obras_disponiveis)]
    df_f_curr = df_fat[df_fat['OBRA'].isin(obras_disponiveis)]

tab_curva, tab_12m, tab_dre, tab_kpi = st.tabs([
    "📈 Curva S & Evolução", 
    "📊 Últimos 12 Meses", 
    "📋 DRE & Impostos", 
    "🎯 KPIs de Obras"
])

val_contratado = df_cont_curr['Valor Final Contratual'].sum()
fat_bruto = df_f_curr['Valor Bruto'].sum()
custo_realizado = df_c_curr['Vr. Rateio'].sum()
resultado_bruto = fat_bruto - custo_realizado
margem_pct = (resultado_bruto / fat_bruto * 100) if fat_bruto > 0 else 0

# --- ABA 1: CURVA S ---
with tab_curva:
    st.header("Evolução Financeira & Curva S")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Valor Contratual", fmt_br(val_contratado))
    c2.metric("Faturamento Bruto", fmt_br(fat_bruto))
    c3.metric("Custo Realizado", fmt_br(custo_realizado))
    c4.metric("Resultado Bruto", fmt_br(resultado_bruto), delta=f"{margem_pct:.1f}% Margem")

    df_c_temp = df_c_curr.copy()
    df_c_temp['MesAno'] = df_c_temp['Comp. C'].dt.to_period('M').dt.to_timestamp()
    c_m = df_c_temp.groupby('MesAno')['Vr. Rateio'].sum().reset_index()

    df_f_temp = df_f_curr.copy()
    df_f_temp['MesAno'] = df_f_temp['COMP MED'].dt.to_period('M').dt.to_timestamp()
    f_m = df_f_temp.groupby('MesAno')['Valor Bruto'].sum().reset_index()

    df_curva = pd.merge(c_m, f_m, on='MesAno', how='outer').fillna(0)
    df_curva = df_curva.sort_values('MesAno')

    df_curva['Custo Acumulado'] = df_curva['Vr. Rateio'].cumsum()
    df_curva['Faturamento Acumulado'] = df_curva['Valor Bruto'].cumsum()

    fig_curva = go.Figure()
    fig_curva.add_trace(go.Scatter(x=df_curva['MesAno'].dt.strftime('%m/%Y'), y=df_curva['Faturamento Acumulado'], mode='lines+markers', name='Faturamento Acumulado', line=dict(color='#00D1B2', width=3)))
    fig_curva.add_trace(go.Scatter(x=df_curva['MesAno'].dt.strftime('%m/%Y'), y=df_curva['Custo Acumulado'], mode='lines+markers', name='Custo Realizado Acumulado', line=dict(color='#FF3860', width=3)))
    fig_curva.update_layout(template="plotly_dark", hovermode="x unified")
    st.plotly_chart(fig_curva, use_container_width=True)

# --- ABA 2: ÚLTIMOS 12 MESES (NOVO GRÁFICO) ---
with tab_12m:
    st.header("Análise Mensal dos Últimos 12 Meses")

    df_c_m = df_c_curr.copy()
    df_c_m['MesAno'] = df_c_m['Comp. C'].dt.to_period('M').dt.to_timestamp()
    c_12 = df_c_m.groupby('MesAno')['Vr. Rateio'].sum().reset_index()

    df_f_m = df_f_curr.copy()
    df_f_m['MesAno'] = df_f_m['COMP MED'].dt.to_period('M').dt.to_timestamp()
    f_12 = df_f_m.groupby('MesAno')['Valor Bruto'].sum().reset_index()

    df_12m = pd.merge(c_12, f_12, on='MesAno', how='outer').fillna(0)
    df_12m = df_12m.sort_values('MesAno').tail(12)

    df_12m['Resultado'] = df_12m['Valor Bruto'] - df_12m['Vr. Rateio']
    df_12m['Margem_Pct'] = np.where(df_12m['Valor Bruto'] > 0, (df_12m['Resultado'] / df_12m['Valor Bruto']) * 100, 0)
    df_12m['MesAno_Label'] = df_12m['MesAno'].dt.strftime('%m/%Y')

    fig_12m = go.Figure()

    # Barras de Faturamento
    fig_12m.add_trace(go.Bar(
        x=df_12m['MesAno_Label'],
        y=df_12m['Valor Bruto'],
        name='Faturamento Bruto',
        marker_color='#00D1B2'
    ))

    # Barras de Custo
    fig_12m.add_trace(go.Bar(
        x=df_12m['MesAno_Label'],
        y=df_12m['Vr. Rateio'],
        name='Custo Realizado',
        marker_color='#FF3860'
    ))

    # Linha de Margem (%)
    fig_12m.add_trace(go.Scatter(
        x=df_12m['MesAno_Label'],
        y=df_12m['Margem_Pct'],
        name='Margem (%)',
        yaxis='y2',
        mode='lines+markers+text',
        text=[f"{m:.1f}%" for m in df_12m['Margem_Pct']],
        textposition="top center",
        line=dict(color='#FFDD57', width=3)
    ))

    fig_12m.update_layout(
        template="plotly_dark",
        barmode='group',
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title="Valor (R$)"),
        yaxis2=dict(
            title="Margem (%)",
            overlaying='y',
            side='right',
            showgrid=False
        )
    )

    st.plotly_chart(fig_12m, use_container_width=True)

# --- ABA 3: DRE OPERACIONAL ---
with tab_dre:
    st.header("Demonstrativo de Resultado (DRE Operacional)")
    fat_liquido = df_f_curr['Valor Líquido NF'].sum()
    
    dre_data = pd.DataFrame({
        "Rubrica": ["Faturamento Bruto", "Faturamento Líquido", "Custos Realizados", "Resultado Operacional"],
        "Valor (R$)": [fmt_br(fat_bruto), fmt_br(fat_liquido), fmt_br(-custo_realizado), fmt_br(resultado_bruto)]
    })
    st.dataframe(dre_data, use_container_width=True, hide_index=True)

# --- ABA 4: RANKING DE OBRAS ---
with tab_kpi:
    st.header("Ranking por Obra")
    c_o = df_custo[df_custo['Considerar']=='S'].groupby('Filial AJUST')['Vr. Rateio'].sum().reset_index()
    f_o = df_fat[df_fat['CONSIDERAR']=='S'].groupby('OBRA')['Valor Bruto'].sum().reset_index()
    df_k = pd.merge(df_cont, c_o, left_on='N° Obra', right_on='Filial AJUST', how='left').fillna(0)
    df_k = pd.merge(df_k, f_o, left_on='N° Obra', right_on='OBRA', how='left').fillna(0)
    df_k['Resultado'] = df_k['Valor Bruto'] - df_k['Vr. Rateio']
    
    fig_b = px.bar(
        df_k.sort_values('Resultado'), 
        x='Resultado', 
        y='NM Contrato', 
        orientation='h', 
        color='Resultado', 
        template="plotly_dark"
    )
    st.plotly_chart(fig_b, use_container_width=True)
    df_k['Resultado'] = df_k['Valor Bruto'] - df_k['Vr. Rateio']
    fig_b = px.bar(df_k.sort_values('Resultado'), x='Resultado', y='NM Contrato', orientation='h', color='Resultado', template="plotly_dark")
    st.plotly_chart(fig_b, use_container_width=True)
