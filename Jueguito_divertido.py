import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Protocolo de Sincronización Bio-Eléctrica", page_icon="🔬")
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { background-color: #800020; color: white; border-radius: 10px; }
    h1 { color: #800020; }
    </style>
    """, unsafe_allow_html=True)

# --- ESTADO DEL JUEGO ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'failed' not in st.session_state:
    st.session_state.failed = False

# --- BASE DE DATOS DE PREGUNTAS ---
questions = [
    # NIVEL 1: SEGURIDAD BIO-SEMÁNTICA 
    {"q": "Para iniciar (Inicie todas sus respuestas con mayúscula y revise que estas no tengan errores ortográficos, por favor): ¿En qué mes nació la ingeniera de este sistema (en palabras)?", "a": "Junio", "type": "text"},
    {"q": "¿Cómo se llama la futura suegra del ingeniero?", "a": "Magaly", "type": "text"},
    {"q": "¿Qué significa 'Ohana' según el Experimento 626?", "a": "Familia", "type": "text"},
    {"q": "En 'Canción de Hielo y Fuego', ¿qué familia tiene por lema 'Winter is Coming'?", "a": "Stark", "type": "text"},
    {"q": "¿Qué sabor prefiere el sistema operativo de la Ingeniera de este sistema?", "a": "Salado", "type": "choice", "ops": ["Dulce", "Salado"]},
    {"q": "¿En qué estación el sistema alcanza su máxima eficiencia térmica?", "a": "Invierno", "type": "choice", "ops": ["Verano", "Invierno"]},
    {"q": "Si la ingeniera se pierde en el SUPERMERCADO, ¿en qué pasillo es más probable que la encuentres?", "a": "Snacks", "type": "choice", "ops": ["Congelados","Lácteos","Snacks","Libros"]},
    {"q": "¿En qué fecha se produjo el primer contacto de los ingenieros (texto sin el año)?", "a": "Cinco de febrero", "type": "text"},
    {"q": "Si el sistema genera una versión v2.0 masculina, ¿cómo se llamaría?", "a": "Dante", "type": "text"},
    {"q": "Si el sistema genera una versión v2.0 femenina, ¿cómo se llamaría?", "a": "Eli", "type": "text"},
    {"q": "Si la ingeniera tuviera un dragón, ¿de qué color sería?", "a": "Negro", "type": "choice", "ops": ["Blanco","Dorado","Negro"]},
    {"q": "¿Cuál fue el color del sostén de la ingeniera el día que se conocieron?", "a": "No tenía", "type": "choice","ops": ["Negro","Rosa","Blanco","No tenía"]},

    
    # NIVEL 2: INGENIERÍA ELÉCTRICA 
    {"q": "En un inductor, ¿la corriente se atrasa o se adelanta respecto al voltaje?", "a": "Se atrasa", "type": "choice", "ops": ["Se atrasa", "Se adelanta"]},
    {"q": "Si tenemos una carga puramente resistiva, ¿cuál es el factor de potencia (en palabras)?", "a": "Uno", "type": "text"},
    {"q": "¿Cuál es la unidad de medida de la reactancia?", "a": "Ohm", "type": "text"},
    {"q": "Leyes de Kirchhoff: La suma algebraica de las corrientes en un nodo es igual a... (en palabras)", "a": "Cero", "type": "text"},
    {"q": "¿Qué componente eléctrico se opone a los cambios bruscos de voltaje?", "a": "Capacitor", "type": "text"},
    {"q": "Si el Amor ($V$) es igual a la Intensidad ($I$) por la Resistencia ($R$), y nuestra resistencia a los problemas es 0, ¿cuánto tiende a ser nuestro amor (en palabras)?","a":"Infinito","type": "text"},

    
    # NIVEL 3: BIOTECNOLOGÍA
    {"q": "¿Cuál es el dogma central: ADN -> ARN -> ...?", "a": "Proteína", "type": "text"},
    {"q": "¿En qué dirección se sintetiza siempre una cadena de ADN?", "a": "5 a 3", "type": "choice", "ops": ["5 a 3", "3 a 5"]},
    {"q": "¿Cómo se llama el proceso de copiar una secuencia de ADN a ARN?", "a": "Transcripción", "type": "text"},
    {"q": "Si la temperatura sube demasiado, ¿qué le pasa a la estructura de una enzima?", "a": "Se desnaturaliza", "type": "text"},
    {"q": "¿Cuál es la moneda energética principal de la célula?", "a": "ATP", "type": "text"},
    {"q": "¿Qué organelo celular es como una 'Central Eléctrica'?", "a": "Mitocondria", "type": "text"},
]

# --- LÓGICA DE NAVEGACIÓN ---
def check_answer(user_input, correct_answer):
    if user_input.lower().strip() == correct_answer.lower().strip():
        st.session_state.current_q += 1
        st.session_state.score += 5
        st.rerun()
    else:
        st.session_state.failed = True

# --- INTERFAZ ---
if not st.session_state.failed and st.session_state.current_q < len(questions):
    st.title(f"🚀 Challenge Nivel {st.session_state.current_q + 1}")
    
    # Mostrar vidas restantes
    cols = st.columns([2, 1])
    with cols[1]:
        st.metric("Vidas ❤️", st.session_state.attempts)
    
    st.progress(st.session_state.current_q / len(questions))
    
    q_data = questions[st.session_state.current_q]
    st.subheader(q_data["q"])
    
    if q_data["type"] == "text":
        user_ans = st.text_input("Escribe tu respuesta:", key=f"q{st.session_state.current_q}")
    else:
        user_ans = st.radio("Selecciona:", q_data["ops"], key=f"q{st.session_state.current_q}")
        
    if st.button("Validar Respuesta"):
        if user_ans:
            check_answer(user_ans, q_data["a"])
        else:
            st.warning("Debes ingresar algo, ingeniero.")

elif st.session_state.failed:
    st.error("❌ ERROR CRÍTICO: Demasiados intentos fallidos. Sistema bloqueado.")
    if st.button("Reiniciar desde Cero"):
        st.session_state.clear()
        st.rerun()

else:
    # --- PANTALLA FINAL ---
    st.balloons()
    st.title("🏆 PROCESANDO RESULTADOS...")
    
    # MENSAJE DE SUSTO SI TUVO ERRORES
    if st.session_state.total_errors > 0:
        st.warning(f"⚠️ Se detectaron {st.session_state.total_errors} fallos en la matriz de memoria. Estuviste cerca del colapso del sistema.")
        time.sleep(2)
        st.info("Re-calibrando sentimientos... Por favor, espera.")
        time.sleep(3)
    
    st.success("Sincronización completada con éxito.")
    
    # Gráfico de Corazón
    t = np.linspace(0, 2 * np.pi, 1000)
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    fig, ax = plt.subplots(figsize=(4,4))
    ax.plot(x, y, color='#800020', linewidth=3)
    ax.fill_between(x, y, color='#800020', alpha=0.3)
    ax.axis('off')
    st.pyplot(fig)
    
    st.markdown("### Entonces... Ingeniero Civil Eléctrico:")
    st.markdown("## ¿Quieres ser el pololo de esta Ingeniera Civil Biotec?")
    
    if st.button("SÍ, ACEPTO EL VÍNCULO"):
        st.snow()
        st.success("¡CONEXIÓN ESTABLECIDA! Próximo hito: Eli y Dante.")
    
