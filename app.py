import streamlit as st

# Configuração da página para ocupar a largura inteira
st.set_page_config(
    page_title="Smart Obra - Dashboard",
    page_icon="🏗️",
    layout="wide"
)

# Código HTML e CSS injetado corretamente com st.markdown e aspas triplas
html_code = """
<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Obra - Dashboard de Custos e Fluxo de Caixa</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        darkBg: '#0b0d19',
                        sidebarBg: '#121528',
                        cardBg: '#181b34',
                        cardBorder: '#272b52',
                        neonCyan: '#00f2fe',
                        neonPurple: '#7928ca',
                        neonPink: '#ff007f',
                        accentBlue: '#4facfe'
                    }
                }
            }
        }
    </script>
    <!-- Font Inter & Lucide Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0b0d19;
            color: #f3f4f6;
        }
        .glass-card {
            background: rgba(24, 27, 52, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .glass-sidebar {
            background: rgba(18, 21, 40, 0.95);
            backdrop-filter: blur(16px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        .glow-cyan {
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.15);
        }
        .glow-pink {
            box-shadow: 0 0 20px rgba(255, 0, 127, 0.15);
        }
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #0b0d19;
        }
        ::-webkit-scrollbar-thumb {
            background: #272b52;
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #3b4279;
        }
    </style>
</head>
<body class="min-h-screen flex overflow-x-hidden">

    <!-- Sidebar Navigation -->
    <aside class="w-64 glass-sidebar fixed inset-y-0 left-0 z-50 flex flex-col justify-between transition-transform duration-300 transform -translate-x-full lg:translate-x-0" id="sidebar">
        <div>
            <!-- Logo Brand -->
            <div class="h-20 flex items-center px-6 gap-3 border-b border-white/5">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-400 to-purple-600 flex items-center justify-center glow-cyan shadow-lg">
                    <i data-lucide="box" class="w-6 h-6 text-white"></i>
                </div>
                <div>
                    <h1 class="font-bold text-lg tracking-wider bg-gradient-to-r from-white via-cyan-200 to-cyan-400 bg-clip-text text-transparent">SMART OBRA</h1>
                    <span class="text-xs text-cyan-400/80 font-medium">Gestão de NFs & Custos</span>
                </div>
            </div>
            <!-- Search bar inside sidebar -->
            <div class="px-4 py-4">
                <div class="relative">
                    <i data-lucide="search" class="w-4 h-4 text-gray-400 absolute left-3 top-3"></i>
                    <input type="text" placeholder="Buscar projeto, NF..." class="w-full bg-[#121528] text-sm text-gray-200 pl-9 pr-4 py-2 rounded-xl border border-white/10 focus:outline-none focus:border-cyan-400 transition-colors">
                </div>
            </div>
            <!-- Menu Links -->
            <div class="px-4 space-y-1">
                <p class="text-xs font-semibold text-gray-500 uppercase px-3 mb-2 tracking-wider">Navegação</p>
                <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-xl bg-gradient-to-r from-purple-900/50 to-indigo-900/30 text-cyan-300 border border-purple-500/30 font-medium transition-all group">
                    <i data-lucide="layout-dashboard" class="w-5 h-5 text-cyan-400"></i>
                    <span>Dashboard Geral</span>
                </a>
                <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 font-medium transition-all group">
                    <i data-lucide="file-text" class="w-5 h-5 text-gray-400 group-hover:text-cyan-400"></i>
                    <span>Notas Fiscais (NFs)</span>
                </a>
                <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 font-medium transition-all group">
                    <i data-lucide="trending-up" class="w-5 h-5 text-gray-400 group-hover:text-cyan-400"></i>
                    <span>Fluxo de Caixa</span>
                </a>
                <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 font-medium transition-all group">
                    <i data-lucide="pie-chart" class="w-5 h-5 text-gray-400 group-hover:text-cyan-400"></i>
                    <span>Análise de Custos</span>
                </a>
                <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 font-medium transition-all group">
                    <i data-lucide="hard-hat" class="w-5 h-5 text-gray-400 group-hover:text-cyan-400"></i>
                    <span>Obras & Canteiros</span>
                </a>
            </div>
            <!-- Management Section -->
            <div class="px-4 mt-6 space-y-1">
                <p class="text-xs font-semibold text-gray-500 uppercase px-3 mb-2 tracking-wider">Administração</p>
                <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 font-medium transition-all">
                    <i data-lucide="users" class="w-5 h-5 text-gray-400"></i>
                    <span>Fornecedores</span>
                </a>
                <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 font-medium transition-all">
                    <i data-lucide="settings" class="w-5 h-5 text-gray-400"></i>
                    <span>Configurações</span>
                </a>
            </div>
        </div>
        <!-- Pro Upgrade Box -->
        <div class="p-4 m-4 rounded-2xl bg-gradient-to-b from-purple-900/40 to-indigo-950/60 border border-purple-500/20 text-center relative overflow-hidden">
            <div class="absolute -right-6 -bottom-6 w-24 h-24 bg-purple-500/10 rounded-full blur-xl pointer-events-none"></div>
            <div class="w-10 h-10 mx-auto mb-2 rounded-xl bg-purple-500/20 flex items-center justify-center border border-purple-400/30 text-purple-300">
                <i data-lucide="shield-check" class="w-5 h-5"></i>
            </div>
            <h4 class="font-semibold text-sm text-white mb-1">Módulo Avançado IA</h4>
            <p class="text-xs text-gray-400 mb-3">Previsão automática de estouro de orçamento.</p>
            <button onclick="showNotification('Módulo IA Ativado com Sucesso!')" class="w-full py-2 bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white font-medium text-xs rounded-xl shadow-lg shadow-purple-500/20 transition-all cursor-pointer">
                Sincronizar ERP
            </button>
        </div>
    </aside>

    <!-- Main Wrapper -->
    <main class="flex-1 lg:ml-64 flex flex-col min-w-0">
        <!-- Top Header Bar -->
        <header class="h-20 glass-card border-b border-white/5 px-6 lg:px-8 flex items-center justify-between sticky top-0 z-40">
            <div class="flex items-center gap-4">
                <button onclick="toggleSidebar()" class="lg:hidden p-2 rounded-xl bg-white/5 text-gray-300 hover:text-white">
                    <i data-lucide="menu" class="w-6 h-6"></i>
                </button>
                <div>
                    <h2 class="text-xl font-bold text-white flex items-center gap-2">
                        Dashboard Financeiro <span class="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-medium">Live Sync</span>
                    </h2>
                    <p class="text-xs text-gray-400">Acompanhamento em tempo real de notas fiscais, custos e fluxo de caixa.</p>
                </div>
            </div>
            <!-- User Profile -->
            <div class="flex items-center gap-4">
                <div class="relative">
                    <button onclick="showNotification('Nenhuma nova notificação pendente.')" class="p-2 rounded-xl bg-white/5 text-gray-300 hover:text-white hover:bg-white/10 transition-colors relative">
                        <i data-lucide="bell" class="w-5 h-5"></i>
                        <span class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-pink-500 animate-pulse"></span>
                    </button>
                </div>
                <div class="flex items-center gap-3 pl-4 border-l border-white/10">
                    <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&h=100&fit=crop&crop=faces" alt="Avatar Gestor" class="w-10 h-10 rounded-xl object-cover border border-cyan-500/30">
                    <div class="hidden sm:block text-left">
                        <p class="text-sm font-semibold text-white">Mariana Costa</p>
                        <p class="text-xs text-cyan-400">Engenheira Gestora</p>
                    </div>
                </div>
            </div>
        </header>

        <!-- Dynamic Control Filter Bar -->
        <div class="px-6 lg:px-8 pt-6 pb-4 flex flex-wrap items-center justify-between gap-4 bg-transparent">
            <!-- Project Selection dropdown/buttons -->
            <div class="flex flex-wrap items-center gap-3">
                <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Obra Selecionada:</span>
                <div class="flex bg-[#181b34] p-1 rounded-xl border border-white/10">
                    <button onclick="filterByObra('todas')" id="btn-obra-todas" class="px-4 py-1.5 rounded-lg text-xs font-semibold transition-all bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow">Todas as Obras</button>
                    <button onclick="filterByObra('alpha')" id="btn-obra-alpha" class="px-4 py-1.5 rounded-lg text-xs font-medium text-gray-300 hover:text-white transition-all">Residencial Alpha</button>
                    <button onclick="filterByObra('corporate')" id="btn-obra-corporate" class="px-4 py-1.5 rounded-lg text-xs font-medium text-gray-300 hover:text-white transition-all">Torre Corporate</button>
                </div>
            </div>
            <!-- Period Filter Pills -->
            <div class="flex flex-wrap items-center gap-2">
                <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider mr-1">Período:</span>
                <button onclick="filterByPeriod('today')" id="period-today" class="px-3 py-1.5 rounded-xl text-xs font-medium bg-white/5 text-gray-300 hover:bg-white/10 transition-all border border-white/5">Hoje</button>
                <button onclick="filterByPeriod('weekly')" id="period-weekly" class="px-3 py-1.5 rounded-xl text-xs font-medium bg-white/5 text-gray-300 hover:bg-white/10 transition-all border border-white/5">Semanal</button>
                <button onclick="filterByPeriod('monthly')" id="period-monthly" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 transition-all">Mensal</button>
                <button onclick="filterByPeriod('custom')" id="period-custom" class="px-3 py-1.5 rounded-xl text-xs font-medium bg-white/5 text-gray-300 hover:bg-white/10 transition-all border border-white/5 flex items-center gap-1.5">
                    <i data-lucide="calendar" class="w-3.5 h-3.5"></i> Personalizado
                </button>
            </div>
        </div>

        <!-- Main Dashboard Content Area -->
        <div class="px-6 lg:px-8 pb-12 space-y-6">
            
            <!-- 4 Top KPI Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                <div class="glass-card p-5 rounded-2xl relative overflow-hidden group hover:border-cyan-500/40 transition-all">
                    <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-cyan-500/10 rounded-full blur-xl group-hover:bg-cyan-500/20 transition-all"></div>
                    <div class="flex items-center justify-between mb-3">
                        <div class="w-10 h-10 rounded-xl bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center text-cyan-300">
                            <i data-lucide="arrow-down-left" class="w-5 h-5"></i>
                        </div>
                        <span class="text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full flex items-center gap-1">
                            <i data-lucide="trending-up" class="w-3 h-3"></i> +12.4%
                        </span>
                    </div>
                    <p class="text-xs font-medium text-gray-400 uppercase tracking-wider mb-1">Entradas (Receitas NFs)</p>
                    <h3 class="text-2xl font-bold text-white mb-2" id="kpi-revenue">R$ 1.482.900</h3>
                    <div class="flex items-center justify-between text-xs text-gray-400 border-t border-white/5 pt-3 mt-1">
                        <span id="kpi-revenue-target">Previsto: R$ 1.600.000</span>
                        <span class="text-cyan-400 font-medium" id="kpi-revenue-percent">92.6% Realizado</span>
                    </div>
                </div>

                <div class="glass-card p-5 rounded-2xl relative overflow-hidden group hover:border-blue-500/40 transition-all">
                    <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-blue-500/10 rounded-full blur-xl group-hover:bg-blue-500/20 transition-all"></div>
                    <div class="flex items-center justify-between mb-3">
                        <div class="w-10 h-10 rounded-xl bg-blue-500/20 border border-blue-500/30 flex items-center justify-center text-blue-300">
                            <i data-lucide="arrow-up-right" class="w-5 h-5"></i>
                        </div>
                        <span class="text-xs font-semibold text-amber-400 bg-amber-500/10 px-2.5 py-1 rounded-full flex items-center gap-1">
                            <i data-lucide="alert-circle" class="w-3 h-3"></i> 78% Orçamento
                        </span>
                    </div>
                    <p class="text-xs font-medium text-gray-400 uppercase tracking-wider mb-1">Custos Executados (Saídas)</p>
                    <h3 class="text-2xl font-bold text-white mb-2" id="kpi-costs">R$ 984.500</h3>
                    <div class="flex items-center justify-between text-xs text-gray-400 border-t border-white/5 pt-3 mt-1">
                        <span id="kpi-costs-pending">A pagar (30d): R$ 142.000</span>
                        <span class="text-blue-400 font-medium">No Prazo</span>
                    </div>
                </div>

                <div class="glass-card p-5 rounded-2xl relative overflow-hidden group hover:border-purple-500/40 transition-all">
                    <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-purple-500/10 rounded-full blur-xl group-hover:bg-purple-500/20 transition-all"></div>
                    <div class="flex items-center justify-between mb-3">
                        <div class="w-10 h-10 rounded-xl bg-purple-500/20 border border-purple-500/30 flex items-center justify-center text-purple-300">
                            <i data-lucide="wallet" class="w-5 h-5"></i>
                        </div>
                        <span class="text-xs font-semibold text-purple-300 bg-purple-500/10 px-2.5 py-1 rounded-full flex items-center gap-1">
                            Saudável
                        </span>
                    </div>
                    <p class="text-xs font-medium text-gray-400 uppercase tracking-wider mb-1">Saldo em Caixa da Obra</p>
                    <h3 class="text-2xl font-bold text-white mb-2" id="kpi-balance">R$ 498.400</h3>
                    <div class="flex items-center justify-between text-xs text-gray-400 border-t border-white/5 pt-3 mt-1">
                        <span>Fundo de Reserva</span>
                        <span class="text-purple-300 font-medium">+15.2% vs Mês Ant.</span>
                    </div>
                </div>

                <div class="glass-card p-5 rounded-2xl relative overflow-hidden group hover:border-pink-500/40 transition-all">
                    <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-pink-500/10 rounded-full blur-xl group-hover:bg-pink-500/20 transition-all"></div>
                    <div class="flex items-center justify-between mb-3">
                        <div class="w-10 h-10 rounded-xl bg-pink-500/20 border border-pink-500/30 flex items-center justify-center text-pink-300">
                            <i data-lucide="activity" class="w-5 h-5"></i>
                        </div>
                        <span class="text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full">
                            Eficiente
                        </span>
                    </div>
                    <p class="text-xs font-medium text-gray-400 uppercase tracking-wider mb-1">Índice de Desempenho (IDC)</p>
                    <h3 class="text-2xl font-bold text-white mb-2" id="kpi-idc">0.94</h3>
                    <div class="flex items-center justify-between text-xs text-gray-400 border-t border-white/5 pt-3 mt-1">
                        <span>Meta: < 1.00</span>
                        <span class="text-pink-400 font-medium">Ótimo</span>
                    </div>
                </div>
            </div>

            <!-- Central Section: Charts & Analytics -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="glass-card p-6 rounded-2xl lg:col-span-2 flex flex-col justify-between">
                    <div class="flex items-center justify-between mb-6">
                        <div>
                            <h3 class="font-bold text-lg text-white">Evolução do Fluxo de Caixa (Entradas vs. Saídas)</h3>
                            <p class="text-xs text-gray-400">Projeção diária acumulada com base nas notas fiscais emitidas e pagas.</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="inline-flex items-center gap-1.5 text-xs text-cyan-400 font-medium">
                                <span class="w-2.5 h-2.5 rounded-full bg-cyan-400"></span> Entradas
                            </span>
                            <span class="inline-flex items-center gap-1.5 text-xs text-purple-400 font-medium ml-2">
                                <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span> Saídas
                            </span>
                        </div>
                    </div>
                    <div class="h-64 w-full relative flex items-end pt-8 pb-2 px-2">
                        <div class="absolute inset-x-0 top-0 h-full flex flex-col justify-between pointer-events-none opacity-20">
                            <div class="border-b border-gray-600 w-full"></div>
                            <div class="border-b border-gray-600 w-full"></div>
                            <div class="border-b border-gray-600 w-full"></div>
                            <div class="border-b border-gray-600 w-full"></div>
                        </div>
                        <svg class="absolute inset-0 w-full h-full overflow-visible p-4" preserveAspectRatio="none" viewBox="0 0 600 200">
                            <defs>
                                <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                                    <stop offset="0%" stop-color="#00f2fe" stop-opacity="0.3"/>
                                    <stop offset="100%" stop-color="#00f2fe" stop-opacity="0.0"/>
                                </linearGradient>
                                <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                                    <stop offset="0%" stop-color="#7928ca" stop-opacity="0.3"/>
                                    <stop offset="100%" stop-color="#7928ca" stop-opacity="0.0"/>
                                </linearGradient>
                            </defs>
                            <path d="M 0 140 Q 100 80, 200 110 T 400 50 T 600 30" fill="none" stroke="#00f2fe" stroke-width="3" stroke-linecap="round"/>
                            <path d="M 0 170 Q 100 120, 200 150 T 400 100 T 600 90" fill="none" stroke="#7928ca" stroke-width="3" stroke-linecap="round"/>
                        </svg>
                        <div class="absolute bottom-0 inset-x-4 flex justify-between text-[11px] text-gray-400 font-medium">
                            <span>01 Seg</span>
                            <span>05 Sex</span>
                            <span>10 Seg</span>
                            <span>15 Sex</span>
                            <span>20 Seg</span>
                            <span>25 Sex</span>
                            <span>30 Sáb</span>
                        </div>
                    </div>
                </div>

                <div class="glass-card p-6 rounded-2xl flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="font-bold text-base text-white">Custos por Categoria (NFs)</h3>
                            <button onclick="showNotification('Exibindo comparativo detalhado por centro de custo.')" class="text-xs text-cyan-400 hover:underline">Ver Todos</button>
                        </div>
                        <p class="text-xs text-gray-400 mb-6">Distribuição percentual dos gastos executados por etapa da obra.</p>
                    </div>
                    <div class="space-y-4">
                        <div>
                            <div class="flex justify-between text-xs font-medium mb-1.5">
                                <span class="text-gray-300">Estrutura & Concreto</span>
                                <span class="text-cyan-400">R$ 380.000 (38%)</span>
                            </div>
                            <div class="w-full bg-white/5 h-2.5 rounded-full overflow-hidden">
                                <div class="bg-gradient-to-r from-cyan-400 to-blue-500 h-full rounded-full" style="width: 38%"></div>
                            </div>
                        </div>
                        <div>
                            <div class="flex justify-between text-xs font-medium mb-1.5">
                                <span class="text-gray-300">Instalações Elétricas / Hidráulicas</span>
                                <span class="text-purple-400">R$ 245.000 (25%)</span>
                            </div>
                            <div class="w-full bg-white/5 h-2.5 rounded-full overflow-hidden">
                                <div class="bg-gradient-to-r from-purple-500 to-indigo-500 h-full rounded-full" style="width: 25%"></div>
                            </div>
                        </div>
                        <div>
                            <div class="flex justify-between text-xs font-medium mb-1.5">
                                <span class="text-gray-300">Acabamento & Revestimento</span>
                                <span class="text-pink-400">R$ 195.000 (20%)</span>
                            </div>
                            <div class="w-full bg-white/5 h-2.5 rounded-full overflow-hidden">
                                <div class="bg-gradient-to-r from-pink-500 to-purple-500 h-full rounded-full" style="width: 20%"></div>
                            </div>
                        </div>
                        <div>
                            <div class="flex justify-between text-xs font-medium mb-1.5">
                                <span class="text-gray-300">Mão de Obra & Administrativo</span>
                                <span class="text-emerald-400">R$ 164.500 (17%)</span>
                            </div>
                            <div class="w-full bg-white/5 h-2.5 rounded-full overflow-hidden">
                                <div class="bg-gradient-to-r from-emerald-400 to-teal-500 h-full rounded-full" style="width: 17%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Toast Notification -->
    <div id="toast-notification" class="fixed bottom-6 right-6 z-50 transform translate-y-32 opacity-0 transition-all duration-300 ease-in-out">
        <div class="glass-card px-5 py-3.5 rounded-2xl border border-cyan-500/30 flex items-center gap-3 shadow-2xl shadow-cyan-500/10">
            <div class="w-8 h-8 rounded-xl bg-cyan-500/20 flex items-center justify-center text-cyan-300">
                <i data-lucide="info" class="w-4 h-4"></i>
            </div>
            <div>
                <h5 class="font-semibold text-xs text-white" id="toast-title">Aviso do Sistema</h5>
                <p class="text-[11px] text-gray-300" id="toast-message">Operação realizada com sucesso.</p>
            </div>
        </div>
    </div>

    <!-- JavaScript Application Logic -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            lucide.createIcons();
        });
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('-translate-x-full');
        }
        function showNotification(message) {
            const toast = document.getElementById('toast-notification');
            const msgEl = document.getElementById('toast-message');
            msgEl.textContent = message;
            toast.classList.remove('translate-y-32', 'opacity-0');
            toast.classList.add('translate-y-0', 'opacity-100');
            setTimeout(() => {
                toast.classList.remove('translate-y-0', 'opacity-100');
                toast.classList.add('translate-y-32', 'opacity-0');
            }, 3500);
        }
        function filterByObra(obraId) {
            showNotification('Filtro aplicado: ' + obraId);
        }
        function filterByPeriod(periodId) {
            showNotification('Período alterado para: ' + periodId);
        }
    </script>
</body>
</html>
"""

# Renderiza o HTML completo dentro do Streamlit ajustando a altura da tela
st.components.v1.html(html_code, height=950, scrolling=True)
