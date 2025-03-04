from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, State
import logging

# Habilitar el registro de logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir los estados de la conversación
(DESCRIPCION, NOMBRE, EQUIPO) = range(3)

# Tu ID de chat y token del bot
YOUR_CHAT_ID = 5666918269  # ID de chat obtenido del JSON
BOT_TOKEN = '8148820292:AAEUw51nAxTCkQc6HBU_pFPWpdvMUPevEKo'

# Función de inicio
async def start(update: Update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf'Hola {user.mention_html()}! Por favor, describe el problema que estás experimentando.'
    )
    return DESCRIPCION

# Función para recibir la descripción del problema
async def descripcion(update: Update, context):
    context.user_data['descripcion'] = update.message.text
    await update.message.reply_text('Gracias. Ahora, ¿cuál es tu nombre?')
    return NOMBRE

# Función para recibir el nombre del usuario
async def nombre(update: Update, context):
    context.user_data['nombre'] = update.message.text
    await update.message.reply_text('Perfecto. ¿Qué equipo estás utilizando?')
    return EQUIPO

# Función para recibir el equipo y enviar el ticket a tu chat de Telegram
async def equipo(update: Update, context):
    context.user_data['equipo'] = update.message.text
    descripcion = context.user_data.get('descripcion')
    nombre = context.user_data.get('nombre')
    equipo = context.user_data.get('equipo')

    # Crear el mensaje del ticket
    ticket_message = f"""
    Nuevo Ticket de Soporte:

    Descripción del problema: {descripcion}
    Nombre del usuario: {nombre}
    Equipo: {equipo}
    """

    # Enviar el mensaje al chat de Telegram
    try:
        await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=ticket_message)
        await update.message.reply_text('Tu ticket ha sido enviado exitosamente.')
    except Exception as e:
        logger.error(f'Error al enviar el mensaje: {e}')
        await update.message.reply_text('Hubo un error al enviar tu ticket. Por favor, inténtalo nuevamente más tarde.')

    return ConversationHandler.END

# Función para cancelar la conversación
async def cancelar(update: Update, context):
    await update.message.reply_text('Operación cancelada.')
    return ConversationHandler.END

# Función principal para configurar el bot
def main():
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

    # Ejecutar el bot
    application.run_polling()

if __name__ == '__main__':
    main()
