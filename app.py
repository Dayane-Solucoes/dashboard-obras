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
    
    /* Fundo Branco e Borda Arredondada para o Logo na Sidebar */
    [data-testid="stSidebar"] img {
        background-color: #FFFFFF !important;
        padding: 12px !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
    }

    /* Selectbox da Obra */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] * {
        color: #0B132B !important;
        font-weight: 600 !important;
    }

    /* Estilo do Cabeçalho da Obra Selecionada */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 4px;
        line-height: 1.2;
    }
    
    .sub-info {
        font-size: 0.88rem;
        color: #64748B !important;
        font-weight: 500;
        margin-bottom: 20px;
    }

    .status-pill {
        background-color: #DCFCE7;
        color: #166534 !important;
        padding: 2px 8px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.78rem;
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

    /* Estilos do Resumo Financeiro */
    .resumo-header {
        color: #3B82F6;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 15px;
    }
    .card-resumo {
        padding: 6px 0;
    }
    .card-resumo-label {
        font-size: 0.85rem;
        color: #64748B;
        font-weight: 500;
    }
    .card-resumo-val-green {
        font-size: 1.15rem;
        color: #16A34A;
        font-weight: 700;
    }
    .card-resumo-val-red {
        font-size: 1.15rem;
        color: #DC2626;
        font-weight: 700;
    }
    .card-resumo-val-blue {
        font-size: 1.15rem;
        color: #2563EB;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Função de Formatação Monetária
def fmt_br(valor):
    try:
        if pd.isna(valor) or valor == 0:
            return "R$ 0,00"
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

# 3. Carregamento de Dados
@st.cache_data(ttl=600)
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
else:
    df_cont_curr = df_cont
    df_c_curr = df_custo
    df_f_curr = df_fat

# Cálculo da Última Atualização
max_dt_custo = df_c_curr['Comp. C'].max() if not df_c_curr.empty else None
max_dt_fat = df_f_curr['COMP MED'].max() if not df_f_curr.empty else None
dates_found = [d for d in [max_dt_custo, max_dt_fat] if pd.notna(d)]
last_update_str = max(dates_found).strftime("%d/%m/%Y") if dates_found else "Aguardando fechamento"

# Indicadores Consolidados
val_contrato = df_cont_curr['Valor Final Contratual'].sum() if 'Valor Final Contratual' in df_cont_curr else 0
fat_bruto = df_f_curr['Valor Bruto'].sum()
custo_direto = df_c_curr['Vr. Rateio'].sum()
custo_indireto = fat_bruto * 0.02
custo_total = custo_direto + custo_indireto
resultado_op = fat_bruto - custo_total
cpi = (fat_bruto / custo_direto) if custo_direto > 0 else 1.0

# --- EXTRAÇÃO DO PREVISTO (DA PLANILHA CONTRATOS) ---
rec_previsto = float(val_contrato)

col_custo_previsto = None
possiveis_colunas = ['Custo Previsto', 'Valor Previsto', 'Orcamento', 'Orcado', 'Custo Orçado', 'Custo Orcado', 'Valor Orçado']

for col in df_cont_curr.columns:
    if str(col).strip().lower() in [p.lower() for p in possiveis_colunas]:
        col_custo_previsto = col
        break

if col_custo_previsto and col_custo_previsto in df_cont_curr:
    desp_previsto = float(df_cont_curr[col_custo_previsto].sum(min_count=1))
    if pd.isna(desp_previsto):
        desp_previsto = 0.0
else:
    desp_previsto = 0.0

saldo_orcado_previsto = rec_previsto - desp_previsto
resultado_previsto = rec_previsto - desp_previsto

rec_realizado = fat_bruto
desp_realizado = custo_total
# CORREÇÃO: Saldo orçado realizado = Receita realizada - Despesa realizada
saldo_orcado_realizado = rec_realizado - desp_realizado
resultado_realizado = rec_realizado - desp_realizado

# Cálculo de Margens Percentuais
margem_prevista_pct = (resultado_previsto / rec_previsto * 100) if rec_previsto > 0 else 0.0
margem_realizada_pct = (resultado_realizado / rec_realizado * 100) if rec_realizado > 0 else 0.0

# Define metadados da obra para exibição no cabeçalho
if selected_obra_str != "Todas as Obras":
    nome_obra_display = selected_obra_str
    cliente_display = df_cont_curr['NM Contrato'].values[0] if not df_cont_curr.empty and 'NM Contrato' in df_cont_curr else "Cliente não cadastrado"
    local_display = "Guarulhos - SP"
else:
    nome_obra_display = "PORTFÓLIO GERAL DE OBRAS"
    cliente_display = "Todos os Clientes"
    local_display = "Múltiplas Localidades"

# --- FUNÇÃO PARA CRIAR O GRÁFICO DE VELOCÍMETRO ---
def criar_grafico_velocimetro():
    meta_contrato = float(val_contrato) if val_contrato > 0 else 1.0 
    faturado_atual = float(fat_bruto)
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = faturado_atual,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "<b>Faturamento vs Contrato</b>", 'font': {'size': 16}},
        delta = {'reference': meta_contrato, 'increasing': {'color': "green"}},
        number = {'prefix': "R$ ", 'valueformat': ",.2f"},
        gauge = {
            'axis': {'range': [None, meta_contrato], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#2563EB"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#E2E8F0",
            'steps': [
                {'range': [0, meta_contrato * 0.5], 'color': '#F1F5F9'},
                {'range': [meta_contrato * 0.5, meta_contrato], 'color': '#E2E8F0'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': meta_contrato
            }
        }
    ))
    
    fig_gauge.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=320,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig_gauge

# --- NAVEGAÇÃO ---

# 1. VISÃO GERAL
if menu_principal == "Visão geral":
    st.markdown(f"""
    <div>
        <div class="main-title">{nome_obra_display}</div>
        <div class="sub-info">
            <span class="status-pill">Em andamento</span> | 
            <b>Cliente:</b> {cliente_display} | 
            📍 <b>Local:</b> {local_display} | 
            📅 <b>Última atualização:</b> {last_update_str}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    sub_aba = st.radio("", ["Resumo", "Financeiro", "Operacional"], horizontal=True)

    if sub_aba == "Resumo":
        # Cards de Indicadores
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="stCard"><div class="metric-label">VALOR CONTRATUAL</div><div class="metric-value">{fmt_br(val_contrato)}</div><div class="metric-sub">↗ cadastro da obra</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stCard"><div class="metric-label">RESULTADO ACUMULADO</div><div class="metric-value">{fmt_br(resultado_op)}</div><div class="metric-sub">↗ fechamento mensal</div></div>', unsafe_allow_html=True)
        with col3:
            avanco_pct = (fat_bruto / val_contrato * 100) if val_contrato > 0 else 0
            st.markdown(f'<div class="stCard"><div class="metric-label">AVANÇO FÍSICO (FAT)</div><div class="metric-value">{avanco_pct:.1f}%</div><div class="metric-sub">↗ medições</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="stCard"><div class="metric-label">RECEBIDO ACUMULADO</div><div class="metric-value">{fmt_br(fat_bruto)}</div><div class="metric-sub">↗ faturamento</div></div>', unsafe_allow_html=True)

        # Preparação dos dados para a Curva S e gráficos
        df_c_temp = df_c_curr.copy()
        df_c_temp['Periodo'] = df_c_temp['Comp. C'].dt.to_period('M')
        c_mes = df_c_temp.groupby('Periodo')['Vr. Rateio'].sum().reset_index()

        df_f_temp = df_f_curr.copy()
        df_f_temp['Periodo'] = df_f_temp['COMP MED'].dt.to_period('M')
        f_mes = df_f_temp.groupby('Periodo')['Valor Bruto'].sum().reset_index()

        df_m = pd.merge(f_mes, c_mes, on='Periodo', how='outer').fillna(0).sort_values('Periodo')
        df_m['MesAno'] = df_m['Periodo'].dt.strftime('%m/%Y')
        
        df_m['Fat_Acumulado'] = df_m['Valor Bruto'].cumsum()
        df_m['Custo_Acumulado'] = df_m['Vr. Rateio'].cumsum()
        df_m['Margem'] = np.where(df_m['Valor Bruto'] > 0, ((df_m['Valor Bruto'] - df_m['Vr. Rateio']) / df_m['Valor Bruto']) * 100, 0)

        # --- 1. PRIMEIRO: GRÁFICO CURVA S ---
        st.markdown("### Curva S - Avanço Físico (Faturamento) vs. Avanço de Custo")
        fig_curva_s = go.Figure()
        
        fig_curva_s.add_trace(go.Scatter(
            x=df_m['MesAno'], 
            y=df_m['Fat_Acumulado'], 
            name="Avanço Físico Acumulado (Faturamento)", 
            mode="lines+markers", 
            line=dict(color='#2563EB', width=4)
        ))
        
        fig_curva_s.add_trace(go.Scatter(
            x=df_m['MesAno'], 
            y=df_m['Custo_Acumulado'], 
            name="Avanço de Custo Acumulado", 
            mode="lines+markers", 
            line=dict(color='#DC2626', width=4, dash='dash')
        ))

        fig_curva_s.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            legend=dict(orientation="h", y=1.15),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        fig_curva_s.update_yaxes(title_text="Valor Acumulado (R$)")
        st.plotly_chart(fig_curva_s, use_container_width=True, key="fig_curva_s")

        st.markdown("---")

        # --- 2. SEGUNDO: GRÁFICO DE BARRAS MENSAL ---
        st.markdown("### Resultado Mensal (Faturado, Custo e Margem)")
        fig_comb = make_subplots(specs=[[{"secondary_y": True}]])
        fig_comb.add_trace(go.Bar(x=df_m['MesAno'], y=df_m['Valor Bruto'], name="Faturado", marker_color='#2563EB'), secondary_y=False)
        fig_comb.add_trace(go.Bar(x=df_m['MesAno'], y=df_m['Vr. Rateio'], name="Custo Realizado", marker_color='#DC2626'), secondary_y=False)
        fig_comb.add_trace(go.Scatter(x=df_m['MesAno'], y=df_m['Margem'], name="Margem (%)", mode="lines+markers", line=dict(color='#10B981', width=3)), secondary_y=True)

        fig_comb.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", y=1.1))
        fig_comb.update_yaxes(title_text="Valor (R$)", secondary_y=False)
        fig_comb.update_yaxes(title_text="Margem (%)", secondary_y=True)
        st.plotly_chart(fig_comb, use_container_width=True, key="fig_vg_comb")

        st.markdown("---")

        # --- 3. TERCEIRO: VELOCÍMETRO (ESQUERDA) E ROSCA (DIREITA) ---
        col_graf_1, col_graf_2 = st.columns(2)
        
        with col_graf_1:
            st.markdown("### Progresso do Faturamento")
            fig_gauge = criar_grafico_velocimetro()
            st.plotly_chart(fig_gauge, use_container_width=True, key="fig_gauge_resumo")

        with col_graf_2:
            st.markdown("### Composição e Distribuição de Custos")
            col_g1 = df_c_curr.columns[28] if len(df_c_curr.columns) >= 29 else df_c_curr.columns[0]
            df_pie = df_c_curr.groupby(col_g1)['Vr. Rateio'].sum().reset_index()
            fig_pie = px.pie(df_pie, values='Vr. Rateio', names=col_g1, hole=0.55, color_discrete_sequence=px.colors.qualitative.Set2)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=320, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_pie, use_container_width=True, key="pie_vg")

    elif sub_aba == "Financeiro":
        # --- BLOCO DE RESUMO FINANCEIRO ---
        st.markdown('<div class="resumo-header">Resumo financeiro</div>', unsafe_allow_html=True)

        classe_res_previsto = "card-resumo-val-red" if resultado_previsto < 0 else "card-resumo-val-green"
        classe_res_realizado = "card-resumo-val-red" if resultado_realizado < 0 else "card-resumo-val-green"

        # Linha 1: Visão Previsto
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        with col_r1:
            st.markdown(f'''
            <div class="card-resumo">
                <div class="card-resumo-label">Receitas (previsto)</div>
                <div class="card-resumo-val-green">{fmt_br(rec_previsto)}</div>
            </div>
            ''', unsafe_allow_html=True)

        with col_r2:
            st.markdown(f'''
            <div class="card-resumo">
                <div class="card-resumo-label">Despesas (previsto)</div>
                <div class="card-resumo-val-red">{fmt_br(desp_previsto)}</div>
            </div>
            ''', unsafe_allow_html=True)

        with col_r3:
            st.markdown(f'''
            <div class="card-resumo">
                <div class="card-resumo-label">Saldo Orçado (previsto)</div>
                <div class="card-resumo-val-blue">{fmt_br(saldo_orcado_previsto)}</div>
            </div>
            ''', unsafe_allow_html=True)

        with col_r4:
            st.markdown(f'''
            <div class="card-resumo">
                <div class="card-resumo-label">Resultado (previsto) - Margem: {margem_prevista_pct:.1f}%</div>
                <div class="{classe_res_previsto}">{fmt_br(resultado_previsto)}</div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Linha 2: Visão Realizado
        col_r5, col_r6, col_r7, col_r8 = st.columns(4)
        with col_r5:
            st.markdown(f'''
            <div class="card-resumo">
                <div class="card-resumo-label">Receitas (realizado)</div>
                <div class="card-resumo-val-green">{fmt_br(rec_realizado)}</div>
            </div>
            ''', unsafe_allow_html=True)

        with col_r6:
            st.markdown(f'''
            <div class="card-resumo">
                <div class="card-resumo-label">Despesas (realizado)</div>
                <div class="card-resumo-val-red">{fmt_br(desp_realizado)}</div>
            </div>
            ''', unsafe_allow_html=True)

        with col_r7:
            st.markdown(f'''
            <div class="card-resumo">
                <div class="card-resumo-label">Saldo Orçado (realizado)</div>
                <div class="card-resumo-val-blue">{fmt_br(saldo_orcado_realizado)}</div>
            </div>
            ''', unsafe_allow_html=True)

        with col_r8:
            st.markdown(f'''
            <div class="card-resumo">
                <div class="card-resumo-label">Resultado (realizado) - Margem: {margem_realizada_pct:.1f}%</div>
                <div class="{classe_res_realizado}">{fmt_br(resultado_realizado)}</div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown("---")

        # --- GRÁFICO DE VELOCÍMETRO (GAUGE CHART) ---
        st.subheader("Progresso do Faturamento vs. Valor Total do Contrato")
        fig_gauge_fin = criar_grafico_velocimetro()
        st.plotly_chart(fig_gauge_fin, use_container_width=True, key="fig_velocimetro_faturamento")

        st.markdown("---")

        # --- DRE RESUMIDA LOGO ABAIXO ---
        st.subheader("DRE - Visão Financeira Resumida")
        
        dre_resumo_df = pd.DataFrame({
            "Descrição": ["Receita Bruta (Faturamento)", "Custos Diretos", "Despesas Indiretas (2%)", "Resultado Operacional"],
            "Orçado / Previsto (R$)": [fmt_br(rec_previsto), fmt_br(-desp_previsto), "R$ 0,00", fmt_br(resultado_previsto)],
            "Realizado (R$)": [fmt_br(fat_bruto), fmt_br(-custo_direto), fmt_br(-custo_indireto), fmt_br(resultado_op)],
            "Margem Realizada (%)": [
                "100,0%",
                f"{- (custo_direto/fat_bruto*100) if fat_bruto>0 else 0:.1f}%".replace(".", ","),
                "-2,0%",
                f"{(resultado_op/fat_bruto*100) if fat_bruto>0 else 0:.1f}%".replace(".", ",")
            ]
        })
        st.dataframe(dre_resumo_df, use_container_width=True, hide_index=True)

# 2. DADOS DA OBRA
elif menu_principal == "Dados da obra":
    st.markdown(f"""
    <div>
        <div class="main-title">CADASTRO DA OBRA</div>
        <div class="sub-info">
            <b>Obra:</b> {nome_obra_display} | 📍 <b>Local:</b> {local_display} | 📅 <b>Última atualização:</b> {last_update_str}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_inf, col_img = st.columns([2, 1])
    
    with col_inf:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.subheader("Informações Principais")
        st.text_input("NOME DA OBRA", value=selected_obra_str)
        st.text_input("CLIENTE", value=cliente_display)
        st.text_input("ENDEREÇO", value=local_display)
        st.number_input("VALOR CONTRATUAL (R$)", value=float(val_contrato))
        
        if st.button("Salvar alterações de cadastro"):
            st.success("Dados salvos com sucesso!")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_img:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.subheader("Foto da Obra")
        
        obra_id = int(selected_id) if selected_obra_str != "Todas as Obras" else "geral"
        caminho_foto = f"foto_obra_{obra_id}.png"
        
        if os.path.exists(caminho_foto):
            st.image(caminho_foto, caption=f"Foto da Obra {obra_id}", use_container_width=True)
        else:
            st.info("Nenhuma foto cadastrada para esta obra.")
            
        uploaded_image = st.file_uploader("Selecione/alterar foto de capa (PNG/JPG)", type=["png", "jpg", "jpeg"], key=f"upload_{obra_id}")
        
        if uploaded_image is not None:
            if st.button("Salvar Foto da Obra"):
                with open(caminho_foto, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                st.success("Foto salva com sucesso!")
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)

# 3. DRE
elif menu_principal == "DRE":
    st.markdown(f"""
    <div>
        <div class="main-title">DEMONSTRATIVO DE RESULTADO (DRE)</div>
        <div class="sub-info">
            <b>Obra:</b> {nome_obra_display} | 📅 <b>Última atualização:</b> {last_update_str}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    dre_df = pd.DataFrame({
        "Conta DRE": [
            "Receita Bruta (Faturamento)", 
            "Custos Diretos", 
            "Despesas Indiretas (2%)", 
            "Resultado Operacional"
        ],
        "Orçado (R$)": [
            fmt_br(rec_previsto), 
            fmt_br(-desp_previsto), 
            fmt_br(0), 
            fmt_br(resultado_previsto)
        ],
        "Realizado (R$)": [
            fmt_br(fat_bruto), 
            fmt_br(-custo_direto), 
            fmt_br(-custo_indireto), 
            fmt_br(resultado_op)
        ],
        "Margem Realizada (%)": [
            "100,0%",
            f"{- (custo_direto/fat_bruto*100) if fat_bruto>0 else 0:.1f}%".replace(".", ","),
            "-2,0%",
            f"{(resultado_op/fat_bruto*100) if fat_bruto>0 else 0:.1f}%".replace(".", ",")
        ]
    })
    st.dataframe(dre_df, use_container_width=True, hide_index=True)

# 4. KPIS
elif menu_principal == "KPIs":
    st.markdown(f"""
    <div>
        <div class="main-title">INDICADORES CHAVE DE PERFORMANCE (KPIs)</div>
        <div class="sub-info">
            <b>Obra:</b> {nome_obra_display} | 📅 <b>Última atualização:</b> {last_update_str}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.markdown(f'<div class="stCard"><div class="metric-label">CPI (Cost Performance Index)</div><div class="metric-value">{cpi:.2f}</div></div>', unsafe_allow_html=True)
    with col_k2:
        st.markdown(f'<div class="stCard"><div class="metric-label">MARGEM OPERACIONAL</div><div class="metric-value">{(resultado_op/fat_bruto*100) if fat_bruto>0 else 0:.1f}%</div></div>', unsafe_allow_html=True)

# 5. CUSTOS
elif menu_principal == "Custos":
    st.markdown(f"""
    <div>
        <div class="main-title">ANÁLISE DETALHADA DE CUSTOS</div>
        <div class="sub-info">
            <b>Obra:</b> {nome_obra_display} | 📅 <b>Última atualização:</b> {last_update_str}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
