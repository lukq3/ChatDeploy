import streamlit as st
from groq import Groq


st.set_page_config(page_title="Mi chat de IA", page_icon= "colocar un icono encontrado en internet", layout= "centered")

st.title("Mi primera  Aplicacion de Streamlit")

nombre = st.text_input("Cual es tu nombre?")

if st.button("Saludar"):
    st.write(f'Hola {nombre}!, Bienvenido a mi Chatbot!') 

modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def configurar_pagina():
#titulo 
    st.title("Mi Chat de Inteligencia Artificial")
    st.sidebar.title("Configuración de la IA")
    elegirModelo = st.sidebar.selectbox("Elegi un modelo", options=modelos, index=0) 
    return elegirModelo 

#modelo = configurar_pagina()      

def crear_usuario_groq():
    claveSecreta = st.secrets["clave_api"]
    return Groq(api_key=claveSecreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model= modelo,
        messages = [{"role": "user", "content": mensajeDeEntrada}],
        stream = True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes=[]

#clienteUsuario = crear_usuario_groq()
#inicializar_estado()
#mensaje = st.chat_input("Por favor, escribí un mensaje")

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content":contenido, "avatar":avatar})
    
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border= True)
    with contenedorDelChat:
        mostrar_historial()


def generar_respuesta (chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat()
    mensaje = st.chat_input("Por favor, escribí un mensaje")
    if mensaje:
        actualizar_historial("user", mensaje, "🗣️")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)

        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant",respuesta_completa, "🤖")

                st.rerun()


if __name__ == "__main__":
    main()

