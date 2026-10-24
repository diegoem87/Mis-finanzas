import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import requests
import json
import os
from datetime import datetime, timezone, timedelta

st.set_page_config(
    page_title="Jardín Financiero",
    layout="wide",
    page_icon="🌿"
)

DATA_FILE = "datos_finanzas.json"

PALETA_PASTEL = [
    "#818CF8",  # Índigo suave
    "#34D399",  # Esmeralda pastel
    "#F472B6",  # Rosa moderno
    "#60A5FA",  # Azul claro elegante
    "#FBBF24",  # Ámbar suave
    "#A78BFA",  # Violeta pastel
    "#2DD4BF",  # Turquesa claro
    "#FB7185",  # Coral fino
    "#4ADE80",  # Verde claro
    "#94A3B8"   # Pizarra neutra
]

# ----------------- NAVEGACIÓN CON FLECHAS DEL TECLADO -----------------
def activar_navegacion_flechas():
    js_code = """
    <script>
    const doc = window.parent.document;
    if (!doc.flechasNavegacionActivas) {
        doc.addEventListener('keydown', function(e) {
            const active = doc.activeElement;
            if (!active || active.tagName !== 'INPUT') return;

            if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
                const inputs = Array.from(
                    doc.querySelectorAll(
                        'input:not([disabled]):not([type="hidden"]):not([type="checkbox"])'
                    )
                ).filter(el => el.offsetParent !== null);

                const idx = inputs.indexOf(active);
                if (idx !== -1) {
                    e.preventDefault();
                    e.stopPropagation();
                    const nextIdx = e.key === 'ArrowDown' ? idx + 1 : idx - 1;
                    if (nextIdx >= 0 && nextIdx < inputs.length) {
                        inputs[nextIdx].focus();
                        if (inputs[nextIdx].select) {
                            inputs[nextIdx].select();
                        }
                    }
                }
            }
        }, true);
        doc.flechasNavegacionActivas = true;
    }
    </script>
    """
    components.html(js_code, height=0, width=0)

# ----------------- GRÁFICO 2D ESTILIZADO -----------------
def crear_torta_2d(df, col_valores, col_nombres):
    valores = df[col_valores].tolist()
    nombres = df[col_nombres].tolist()
    total = sum(valores) if sum(valores) > 0 else 1.0
    n = len(valores)

    colores = [PALETA_PASTEL[i % len(PALETA_PASTEL)] for i in range(n)]

    posiciones = [
        "outside" if (v / total) < 0.09 else "inside"
        for v in valores
    ]

    fig = go.Figure(data=[go.Pie(
        labels=nombres,
        values=valores,
        hole=0.42,
        sort=True,
        direction="clockwise",
        textposition=posiciones,
        textinfo="label+percent",
        insidetextorientation="horizontal",
        pull=[0.015] * n,
        automargin=True,
        textfont=dict(
            size=13,
            color="#334155",
            family="Inter, system-ui, sans-serif"
        ),
        marker=dict(
            colors=colores,
            line=dict(color="#FFFFFF", width=2.5)
        ),
        showlegend=False
    )])

    fig.update_layout(
        uniformtext=dict(minsize=12, mode="show"),
        height=400,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def formatear_cant(valor):
    try:
        num = float(valor)
        if num.is_integer():
            return str(int(num))
        return f"{num:.6f}".rstrip("0").rstrip(".")
    except Exception:
        return str(valor)

def clasificar_costo_existente(nombre):
    n = nombre.upper().strip()
    if any(k in n for k in ["INMOBILIARIO", "CISI", "COSI", "AUTOMOTOR", "IMPUESTO", "MONOTRIBUTO"]):
        return "Impuestos"
    if any(k in n for k in ["SAT", "EDET", "GAS", "CLARO", "LUZ", "AGUA", "INTERNET", "SERVICIO"]):
        return "Servicios"
    if any(k in n for k in ["NETFLIX", "DISNEY", "SPOTIFY", "FLOW", "YOUTUBE"]):
        return "Suscripciones"
    if any(k in n for k in ["NAFTA", "SEGURO", "AUTO", "PATENTE", "COCHERA"]):
        return "Vehículo y Movilidad"
    if any(k in n for k in ["GABINETE", "INSUMO", "CONSULTORIO"]):
        return "Gabinete"
    return "Hogar y Otros"

# ----------------- GESTIÓN Y PERSISTENCIA -----------------
def cargar_datos():
    criptos_base = ["BTC", "ETH", "USDT", "SOL", "BNB", "ADA", "XRP", "DOT", "DOGE"]
    acciones_base = [
        "AAPL (Apple)", "KO (Coca-Cola)", "MELI (MercadoLibre)",
        "SPY (S&P 500)", "MSFT (Microsoft)", "GOOGL (Google)",
        "NVDA (Nvidia)", "TSLA (Tesla)", "AMZN (Amazon)", "YPFD (YPF)"
    ]

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

                for c in data.get("costos", []):
                    c.setdefault("activo", True)
                    if "grupo" not in c or not c["grupo"]:
                        c["grupo"] = clasificar_costo_existente(c.get("categoria", ""))

                for ing in data.get("ingresos", []):
                    ing.setdefault("activo", True)
                    if "grupo" not in ing or not ing["grupo"]:
                        nom_low = ing.get("concepto", "").lower()
                        if "farmacia" in nom_low or "sac" in nom_low:
                            ing["grupo"] = "Farmacia"
                        elif "jubil" in nom_low:
                            ing["grupo"] = "Jubilación"
                        else:
                            ing["grupo"] = "Otros Ingresos"

                cats_base_c = ["Impuestos", "Servicios", "Suscripciones", "Vehículo y Movilidad", "Hogar y Otros", "Gabinete"]
                cats_c = list(dict.fromkeys(
                    data.get("categorias_costos", cats_base_c)
                    + [c["grupo"] for c in data.get("costos", [])]
                ))
                data["categorias_costos"] = cats_c

                cats_base_i = ["Farmacia", "Jubilación", "Terapias"]
                cats_i = list(dict.fromkeys(
                    data.get("categorias_ingresos", cats_base_i)
                    + [i["grupo"] for i in data.get("ingresos", [])]
                ))
                data["categorias_ingresos"] = cats_i

                for inv in data.get("inversiones", []):
                    inv.setdefault("activo_inv", True)
                    if inv.get("tipo") == "Acciones / CEDEARs":
                        inv["tipo"] = "Acciones"
                    elif inv.get("tipo") == "Efectivo / Banco":
                        inv["tipo"] = "Pesos ARS"

                criptos_actuales = data.get("criptos_guardadas", criptos_base)
                for inv in data.get("inversiones", []):
                    if inv.get("tipo") == "Criptomonedas":
                        sim = inv.get("simbolo", "").upper().strip()
                        if sim and sim not in criptos_actuales:
                            criptos_actuales.append(sim)
                data["criptos_guardadas"] = criptos_actuales

                acciones_actuales = data.get("acciones_guardadas", acciones_base)
                data["acciones_guardadas"] = acciones_actuales
                return data
        except Exception:
            pass

    return {
        "categorias_costos": [
            "Impuestos",
            "Servicios",
            "Suscripciones",
            "Vehículo y Movilidad",
            "Hogar y Otros"
        ],
        "costos": [
            {"grupo": "Impuestos", "categoria": "INMOBILIARIO", "monto": 2462, "activo": True},
            {"grupo": "Impuestos", "categoria": "CISI", "monto": 2659, "activo": True},
            {"grupo": "Impuestos", "categoria": "AUTOMOTOR", "monto": 2667, "activo": True},
            {"grupo": "Servicios", "categoria": "SAT", "monto": 36000, "activo": True},
            {"grupo": "Servicios", "categoria": "EDET", "monto": 60000, "activo": True},
            {"grupo": "Servicios", "categoria": "GAS", "monto": 16000, "activo": True},
            {"grupo": "Servicios", "categoria": "CLARO + RECARGA", "monto": 29000, "activo": True},
            {"grupo": "Suscripciones", "categoria": "NETFLIX", "monto": 15000, "activo": True},
            {"grupo": "Suscripciones", "categoria": "DISNEY", "monto": 9000, "activo": True},
            {"grupo": "Vehículo y Movilidad", "categoria": "NAFTA", "monto": 86000, "activo": True},
            {"grupo": "Vehículo y Movilidad", "categoria": "SEGURO", "monto": 28000, "activo": True}
        ],
        "categorias_ingresos": [
            "Farmacia",
            "Jubilación",
            "Terapias"
        ],
        "ingresos": [
            {"grupo": "Farmacia", "concepto": "Sueldo Farmacia", "monto": 650000, "activo": True},
            {"grupo": "Farmacia", "concepto": "SAC (Aguinaldo proporcional)", "monto": 54000, "activo": True},
            {"grupo": "Jubilación", "concepto": "Jubilación", "monto": 320000, "activo": True}
        ],
        "precio_terapia": 30000,
        "criptos_guardadas": criptos_base,
        "acciones_guardadas": acciones_base,
        "inversiones": [
            {
                "tipo": "Criptomonedas",
                "activo": "BTC",
                "simbolo": "BTC",
                "cantidad": 0.5,
                "plataforma": "BINANCE",
                "activo_inv": True
            },
            {
                "tipo": "Otros",
                "activo": "FRASCO NX",
                "simbolo": "ARS",
                "cantidad": 100000,
                "plataforma": "NX APP",
                "activo_inv": True
            }
        ]
    }

def guardar_datos(datos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

# ----------------- COTIZACIONES EXTERNAS -----------------
@st.cache_data(ttl=180)
def obtener_cotizaciones(simbolos_acciones, simbolos_cripto):
    cotiz = {
        "dolar_blue": 1555.0,
        "BTC": 82000.0,
        "ETH": 2600.0,
        "USDT": 1.0,
        "SOL": 150.0,
        "BNB": 580.0,
        "ADA": 0.75,
        "XRP": 1.10,
        "DOT": 6.50,
        "DOGE": 0.22,
        "AAPL": 230.0,
        "KO": 68.0,
        "MELI": 2050.0,
        "SPY": 580.0,
        "MSFT": 420.0,
        "GOOGL": 175
