import os
import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, 
    ConversationHandler, ContextTypes
)

# ID de chat y token del bot (⚠️ NO COMPARTAS ESTO PÚBLICAMENTE)
BOT_TOKEN = "8148820292:AAEUw51nAxTCkQc6HBU_pFPWpdvMUPevEKo"
YOUR_CHAT_ID = 5666918269  # Cambia esto por tu chat ID

# Configurar logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Estados de la conversación
DESCRIPCION, NOMBRE, EQUIPO = range(3)

# Archivo con palabras prohibidas
PALABRAS_ARCHIVO = "palabras_prohibidas.txt"

# Función para leer palabras prohibidas desde un archivo
def cargar_palabras_prohibidas():
    if not os.path.exists(PALABRAS_ARCHIVO):
        return set()
    with open(PALABRAS_ARCHIVO, "r", encoding="utf-8") as file:
        return {line.strip().lower() for line in file}

# Función para verificar si un mensaje contiene palabras prohibidas
def contiene_palabra_prohibida(texto):
    palabras_prohibidas = cargar_palabras_prohibidas()
    palabras_mensaje = set(texto.lower().split())
    return any(palabra in palabras_prohibidas for palabra in palabras_mensaje)

# Función de inicio
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf'Hola {user.mention_html()}! Por favor, describe el problema que estás experimentando.'
    )
    return DESCRIPCION

# Función para recibir la descripción del problema
async def descripcion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    if contiene_palabra_prohibida(texto):
        await update.message.reply_text("⚠️ Tu mensaje contiene palabras no permitidas.")
        return DESCRIPCION  

    context.user_data['descripcion'] = texto
    await update.message.reply_text('Gracias. Ahora, ¿cuál es tu nombre?')
    return NOMBRE

# Función para recibir el nombre del usuario
async def nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    if contiene_palabra_prohibida(texto):
        await update.message.reply_text("⚠️ Tu mensaje contiene palabras no permitidas.")
        return NOMBRE  

    context.user_data['nombre'] = texto
    await update.message.reply_text('Perfecto. ¿Qué equipo estás utilizando?')
    return EQUIPO

# Función para recibir el equipo y enviar el ticket a tu chat de Telegram
async def equipo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    if contiene_palabra_prohibida(texto):
        await update.message.reply_text("⚠️ Tu mensaje contiene palabras no permitidas.")
        return EQUIPO  

    context.user_data['equipo'] = texto
    descripcion = context.user_data.get('descripcion')
    nombre = context.user_data.get('nombre')
    equipo = context.user_data.get('equipo')

    # Crear el mensaje del ticket
    ticket_message = f"""
    📌 *Nuevo Ticket de Soporte* 📌

    **Descripción del problema:** {descripcion}
    **Nombre del usuario:** {nombre}
    **Equipo:** {equipo}
    """

    # Enviar el mensaje al chat de Telegram
    try:
        await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=ticket_message, parse_mode="Markdown")
        await update.message.reply_text('✅ Tu ticket ha sido enviado exitosamente.')
    except Exception as e:
        logger.error(f'Error al enviar el mensaje: {e}')
        await update.message.reply_text('⚠️ Hubo un error al enviar tu ticket. Inténtalo más tarde.')

    return ConversationHandler.END

# Función para cancelar la conversación
async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('❌ Operación cancelada.')
    return ConversationHandler.END

# Función de depuración: responde cualquier texto recibido
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    print(f"Mensaje recibido: {texto}")
    if contiene_palabra_prohibida(texto):
        await update.message.reply_text("⚠️ Tu mensaje contiene palabras no permitidas.")
    else:
        await update.message.reply_text(f"Recibí tu mensaje: {texto}")

# Función principal para configurar el bot
def main():
    print("Iniciando el bot...")

    # Crear la aplicación del bot con el token
    application = Application.builder().token(BOT_TOKEN).build()

    # Definir la conversación
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            DESCRIPCION: [MessageHandler(filters.TEXT & ~filters.COMMAND, descripcion)],
            NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, nombre)],
            EQUIPO: [MessageHandler(filters.TEXT & ~filters.COMMAND, equipo)],
        },
        fallbacks=[CommandHandler('cancel', cancelar)],
    )

    # Añadir el manejador de conversación al bot
    application.add_handler(conversation_handler)

    # Manejador para responder cualquier mensaje recibido (depuración)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("El bot está corriendo... Esperando mensajes.")
    application.run_polling()

if __name__ == '__main__':
    main()
