import streamlit as datetime_alias # Solo para evitar conflictos de nombres
from datetime import datetime
import streamlit as st

# Configuración de la página (Debe ser lo primero)
st.set_page_config(
    page_title="FinanzasPro - Panel Financiero",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inyección de Estilos CSS Profesionales (Modo Oscuro Corporativo)
st.markdown(
    """
    <style>
    /* Importar fuente Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fondo principal y de la barra lateral */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    [data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1e293b;
    }

    /* Tarjetas de métricas y contenedores personalizados */
    .metric-card {
        background-color: #020617;
        border: 1px solid #1e293b;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }

    .card-border-amber { border-left: 4px solid #f59e0b; }
    .card-border-emerald { border-left: 4px solid #10b981; }
    .card-border-blue { border-left: 4px solid #3b82f6; }

    /* Estilo para los textos pequeños de las tarjetas */
    .card-title {
        color: #94a3b8;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    .card-value {
        color: #ffffff;
        font-size: 1.875rem;
        font-weight: 700;
        letter-spacing: -0.025em;
    }

    .card-subvalue {
        display: inline-block;
        background-color: #0f172a;
        border: 1px solid #1e293b;
        color: #cbd5e1;
        font-size: 0.75rem;
        padding: 0.25rem 0.6rem;
        border-radius: 0.375rem;
        margin-top: 0.5rem;
        margin-bottom: 0.75rem;
    }

    /* Ocultar elementos predeterminados molestos de Streamlit para que luzca limpio */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    # Logo y Título
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 2rem;">
            <div style="background-color: #2563eb; padding: 10px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);">
                📊
            </div>
            <div>
                <h2 style="color: white; font-size: 1.1rem; font-weight: 700; margin: 0;">FinanzasPro</h2>
                <p style="color: #94a3b8; font-size: 0.75rem; margin: 0;">Panel de Control</p>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Fecha y Hora Actual
    st.markdown(
        """
        <div style="background-color: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 1rem; margin-bottom: 1.5rem;">
            <p style="color: #94a3b8; font-size: 0.75rem; font-weight: 500; margin: 0;">Fecha Actual</p>
            <p style="color: #e2e8f0; font-size: 0.9rem; font-weight: 600; margin: 2px 0;">Sábado, 24 de Octubre</p>
            <p style="color: #64748b; font-size: 0.75rem; margin: 0;">13:45 hs</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Indicadores de Mercado
    st.markdown(
        '<p style="color: #94a3b8; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">Mercado</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background-color: rgba(15, 23, 42, 0.5); border: 1px solid #1e293b; border-radius: 8px; padding: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 8px; height: 8px; background-color: #10b981; border-radius: 50%;"></div>
                <span style="color: #cbd5e1; font-size: 0.8rem; font-weight: 500;">Dólar Blue</span>
            </div>
            <span style="color: #34d399; background-color: rgba(6, 78, 59, 0.4); border: 1px solid rgba(6, 78, 59, 0.5); font-size: 0.75rem; font-weight: 600; padding: 2px 8px; border-radius: 4px;">1,565 ARS</span>
        </div>
        
        <div style="background-color: rgba(15, 23, 42, 0.5); border: 1px solid #1e293b; border-radius: 8px; padding: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 8px; height: 8px; background-color: #f59e0b; border-radius: 50%;"></div>
                <span style="color: #cbd5e1; font-size: 0.8rem; font-weight: 500;">Bitcoin</span>
            </div>
            <span style="color: #fbbf24; background-color: rgba(120, 53, 15, 0.4); border: 1px solid rgba(120, 53, 15, 0.5); font-size: 0.75rem; font-weight: 600; padding: 2px 8px; border-radius: 4px;">82,000 USD</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Botón Cerrar Sesión
    st.markdown("<div style='margin-top: 5rem;'></div>", unsafe_allow_html=True)
    if st.button(
        "🚪 Cerrar Sesión", use_container_width=True, type="secondary"
    ):
        st.info("Sesión cerrada (simulación).")


# ==========================================
# CONTENIDO PRINCIPAL
# ==========================================

# Pestañas Superiores simuladas con radio buttons horizontales o selectores limpios
pestana = st.radio(
    "Navegación",
    ["📊 Costos e Inversiones", "💎 Cartera de Inversiones"],
    label_visibility="collapsed",
    horizontal=True,
)

st.markdown(
    "<hr style='border: none; border-top: 1px solid #1e293b; margin: 1.5rem 0;'>",
    unsafe_allow_html=True,
)

if "Costos e Inversiones" in pestana:

    # --- TARJETAS DE MÉTRICAS ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="metric-card card-border-amber">
                <div class="card-title">Costo Mensual</div>
                <div class="card-value">286,788 <span style="font-size: 1rem; color: #94a3b8; font-weight: 600;">ARS</span></div>
                <div class="card-subvalue">≈ 183.25 USD</div>
                <div style="border-top: 1px solid #0f172a; padding-top: 10px; display: flex; justify-content: space-between; font-size: 0.75rem; color: #94a3b8;">
                    <span>Ítems activos</span>
                    <span style="color: #e2e8f0; font-weight: 600;">11</span>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="metric-card card-border-emerald">
                <div class="card-title">Ingreso Mensual</div>
                <div class="card-value">1,024,000 <span style="font-size: 1rem; color: #94a3b8; font-weight: 600;">ARS</span></div>
                <div class="card-subvalue">≈ 654.31 USD</div>
                <div style="border-top: 1px solid #0f172a; padding-top: 10px; display: flex; justify-content: space-between; font-size: 0.75rem; color: #94a3b8;">
                    <span>Ítems activos</span>
                    <span style="color: #e2e8f0; font-weight: 600;">3</span>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card card-border-blue">
                <div class="card-title">Ahorro Mensual</div>
                <div class="card-value">737,212 <span style="font-size: 1rem; color: #94a3b8; font-weight: 600;">ARS</span></div>
                <div class="card-subvalue">≈ 471.06 USD</div>
                <div style="border-top: 1px solid #0f172a; padding-top: 10px; display: flex; justify-content: space-between; font-size: 0.75rem; color: #94a3b8;">
                    <span>Resultado</span>
                    <span style="color: #34d399; font-weight: 600;">Positivo (Ganancia)</span>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SECCIÓN CALCULADORA ---
    with st.expander(
        "🧮 Calculadora de Terapias: Sesiones necesarias según tus números activos",
        expanded=True,
    ):
        col_calc1, col_calc2 = st.columns([1, 1], gap="large")

        with col_calc1:
            st.markdown(
                "<p style='color: #cbd5e1; font-size: 0.8rem; font-weight: 600; text-transform: uppercase;'>Valor por sesión de terapia (ARS):</p>",
                unsafe_allow_html=True,
            )
            valor_sesion = st.number_input(
                "Valor sesión",
                value=30000,
                step=1000,
                label_visibility="collapsed",
            )
            usd_sesion = valor_sesion / 1565  # Usando valor del dólar blue de referencia
            st.markdown(
                f"<p style='color: #94a3b8; font-size: 0.8rem; margin-top: 8px;'>Equivale a <b style='color: #e2e8f0;'>{usd_sesion:.2f} USD</b> por sesión.</p>",
                unsafe_allow_html=True,
            )

        with col_calc2:
            st.markdown(
                """
                <div style="background: linear-gradient(to bottom right, rgba(6, 78, 59, 0.4), #0f172a); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 1.25rem;">
                    <div style="display: flex; align-items: flex-start; gap: 12px;">
                        <div style="background-color: rgba(16, 185, 129, 0.2); color: #34d399; padding: 8px; border-radius: 8px; font-size: 1.1rem;">
                            ✨
                        </div>
                        <div>
                            <h4 style="color: #34d399; font-size: 0.9rem; font-weight: 600; margin: 0 0 6px 0;">¡Tus costos activos están 100% cubiertos!</h4>
                            <p style="color: #cbd5e1; font-size: 0.75rem; line-height: 1.5; margin: 0;">
                                Con los ingresos que tenés tildados hoy, cubrís todos tus gastos y te queda un ahorro a favor de 
                                <b style="color: white;">737,212 ARS</b> (471.06 USD) por mes.
                            </p>
                        </div>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )

else:
    st.markdown(
        "<h3 style='color: #94a3b8; text-align: center; margin-top: 4rem;'>Sección Cartera de Inversiones en desarrollo...</h3>",
        unsafe_allow_html=True,
    )
