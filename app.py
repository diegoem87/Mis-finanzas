import pandas as pd
import streamlit as st

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Panel Financiero",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS personalizados para mejorar la estética general
st.markdown(
    """
    <style>
        .main {
            background-color: #f8fafc;
        }
        .stMetric {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .css-1dp5vir {
            background-color: #ffffff;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# ESTADO DE LA SESIÓN
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "inversiones" not in st.session_state:
    st.session_state.inversiones = pd.DataFrame(
        {
            "Tipo": ["Acciones", "Criptomonedas", "Bienes Raíces"],
            "Activo": [
                "Tecnología Global (ETF)",
                "Bitcoin (BTC)",
                "Fondo Inmobiliario",
            ],
            "Invertido": [5000.0, 2500.0, 10000.0],
            "Valor Actual": [5710.0, 2712.5, 9880.0],
            "Rendimiento (%)": [14.2, 8.5, -1.2],
        }
    )

# ==========================================
# 1. PANTALLA DE INICIO DE SESIÓN (LOGIN)
# ==========================================
if not st.session_state.authenticated:
    st.markdown(
        "<br><br><h1 style='text-align: center; color: #1e293b;'>🔐 Inicio de Sesión</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #64748b;'>Ingresa tus credenciales para acceder al panel de control</p><br>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        with st.form("login_form"):
            user_input = st.text_input("Usuario")
            pass_input = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Ingresar", use_container_width=True)

            if submit:
                if user_input and pass_input:
                    st.session_state.authenticated = True
                    st.session_state.username = user_input
                    st.rerun()
                else:
                    st.error("Por favor, completa todos los campos.")

# ==========================================
# 2. PANEL PRINCIPAL (DASHBOARD)
# ==========================================
else:
    # Barra lateral de navegación
    with st.sidebar:
        st.markdown(f"### 👤 ¡Hola, {st.session_state.username}!")
        st.markdown("---")
        if st.button("Cerrar Sesión", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()

    # Encabezado Principal
    st.title("📊 Panel Financiero y de Inversiones")
    st.markdown(
        "Monitorea tus ingresos, costos y el rendimiento de tu portafolio en tiempo real."
    )
    st.markdown("---")

    # --- SECCIÓN: GRÁFICOS DE INGRESOS Y COSTOS ---
    st.subheader("📈 Análisis de Ingresos y Costos")

    df_finanzas = pd.DataFrame(
        {
            "Mes": [
                "Enero",
                "Febrero",
                "Marzo",
                "Abril",
                "Mayo",
                "Junio",
            ],
            "Ingresos": [12000, 15000, 14000, 18000, 22000, 25000],
            "Costos": [8000, 9000, 8500, 11000, 13000, 14000],
        }
    )
    df_finanzas.set_index("Mes", inplace=True)

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("**Evolución Financiera ($)**")
        st.bar_chart(df_finanzas)

    with col_g2:
        st.markdown("**Distribución de Costos Operativos**")
        df_costos = pd.DataFrame(
            {
                "Categoría": [
                    "Operativos",
                    "Personal",
                    "Marketing",
                    "Tecnología",
                    "Otros",
                ],
                "Porcentaje": [35, 30, 15, 12, 8],
            }
        )
        df_costos.set_index("Categoría", inplace=True)
        st.bar_chart(df_costos)

    st.markdown("---")

    # --- SECCIÓN: INVERSIONES ---
    st.subheader("💰 Portafolio de Inversiones")

    cols_inv = st.columns(len(st.session_state.inversiones))
    for idx, row in st.session_state.inversiones.iterrows():
        with cols_inv[idx]:
            st.markdown(f"**{row['Activo']}**")
            st.caption(f"Tipo: {row['Tipo']}")
            st.metric(
                label="Valor Actual",
                value=f"${row['Valor Actual']:,.2f}",
                delta=f"{row['Rendimiento (%)']}%",
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Formulario para agregar nuevas inversiones
    with st.expander("➕ Agregar nueva inversión al portafolio"):
        with st.form("nueva_inversion_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                tipo_nuevo = st.selectbox(
                    "Tipo de Activo",
                    [
                        "Acciones",
                        "Criptomonedas",
                        "Bienes Raíces",
                        "Renta Fija",
                        "Otros",
                    ],
                )
                activo_nuevo = st.text_input(
                    "Nombre del Activo (ej. Tesla, Ethereum)"
                )
            with col_f2:
                invertido_nuevo = st.number_input(
                    "Monto Inicial Invertido ($)", min_value=0.0, value=1000.0
                )
                valor_actual_nuevo = st.number_input(
                    "Valor Actual ($)", min_value=0.0, value=1050.0
                )

            btn_agregar = st.form_submit_button(
                "Guardar Inversión", use_container_width=True
            )

            if btn_agregar:
                if activo_nuevo:
                    rendimiento = (
                        (valor_actual_nuevo - invertido_nuevo)
                        / invertido_nuevo
                    ) * 100
                    nueva_fila = pd.DataFrame(
                        {
                            "Tipo": [tipo_nuevo],
                            "Activo": [activo_nuevo],
                            "Invertido": [invertido_nuevo],
                            "Valor Actual": [valor_actual_nuevo],
                            "Rendimiento (%)": [round(rendimiento, 2)],
                        }
                    )
                    st.session_state.inversiones = pd.concat(
                        [st.session_state.inversiones, nueva_fila],
                        ignore_index=True,
                    )
                    st.success("¡Inversión agregada correctamente!")
                    st.rerun()
                else:
                    st.warning(
                        "Por favor, ingresa el nombre del activo antes de guardar."
                    )
