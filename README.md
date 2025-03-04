# Bot de Soporte en Telegram

Este es un bot de Telegram que permite a los usuarios crear tickets de soporte enviando una descripción del problema, su nombre, y el equipo que están utilizando. El bot luego envía esta información a un chat de Telegram específico para que los administradores puedan revisar y gestionar los tickets.

## Características

- Conversación guiada para que los usuarios ingresen:
  - Descripción del problema.
  - Su nombre.
  - El equipo que están utilizando.
- Envío automático del ticket a un chat de Telegram configurado con el ID del administrador.
- Soporte para cancelar la operación en cualquier momento de la conversación.

## Requisitos

- Python 3.7+
- Paquetes de Python: `python-telegram-bot`

## Instalación

1. Clonar este repositorio:

```bash
git clone https://github.com/IranEme/ChatbotApiTelegram/
cd ChatbotApiTelegram
```

2. Instalar las dependencias:

```bash
pip install python-telegram-bot --upgrade
```

3. Configurar tu ID de chat y el token del bot:

Abre el archivo principal y reemplaza los siguientes valores con los tuyos:

```python
YOUR_CHAT_ID = 'TU_CHAT_ID'
BOT_TOKEN = 'TU_TOKEN_DEL_BOT'
```

Para obtener el token de tu bot, utiliza [BotFather](https://t.me/botfather) en Telegram. Para obtener el `chat_id`, puedes iniciar una conversación con el bot y obtener el JSON de la respuesta para verificar el ID.

## Uso

1. Ejecutar el bot:

```bash
python itebot.py
```

2. Iniciar una conversación en Telegram usando el comando `/start`.

3. El bot te pedirá la descripción del problema, tu nombre y el equipo que utilizas. Al completar la conversación, el bot enviará el ticket al chat especificado.

4. En cualquier momento, puedes cancelar el proceso escribiendo `/cancel`.

## Estados del Bot

- **/start**: Inicia la conversación y pide la descripción del problema.
- **Descripción**: El usuario proporciona la descripción de su problema.
- **Nombre**: El usuario proporciona su nombre.
- **Equipo**: El usuario proporciona el equipo que está utilizando.
- **/cancel**: Cancela la conversación en cualquier momento.

## Ejemplo de Ticket

```text
Nuevo Ticket de Soporte:

Descripción del problema: El equipo no enciende.
Nombre del usuario: Juan Pérez
Equipo: Laptop Dell
```

## Contribuir

Si deseas contribuir a este proyecto, siéntete libre de abrir un pull request o una issue en GitHub.


