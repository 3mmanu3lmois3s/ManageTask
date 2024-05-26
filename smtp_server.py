import asyncio
from aiosmtpd.controller import Controller
from email.message import EmailMessage

# Definimos una clase que maneja los datos recibidos por el servidor SMTP
class CustomSMTPHandler:
    # Método que maneja la recepción de datos del mensaje
    async def handle_DATA(self, server, session, envelope):
        # Imprimimos información sobre el remitente y destinatarios del mensaje
        print('Receiving message from:', session.peer)
        print('Message addressed from:', envelope.mail_from)
        print('Message addressed to  :', envelope.rcpt_tos)
        # Imprimimos el contenido del mensaje
        print('Message data          :\n', envelope.content.decode('utf8', errors='replace'))
        # Respondemos que el mensaje fue aceptado para entrega
        return '250 Message accepted for delivery'

# Función para ejecutar el servidor SMTP
def run():
    # Creamos una instancia del manejador personalizado
    handler = CustomSMTPHandler()
    # Creamos un controlador para el servidor SMTP en localhost y puerto 1025
    controller = Controller(handler, hostname='127.0.0.1', port=1025)
    # Iniciamos el servidor SMTP
    controller.start()
    print('SMTP server is running on port 1025...')
    
    try:
        # Mantenemos el servidor corriendo indefinidamente
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        # Al recibir una interrupción (Ctrl+C), paramos el servidor
        print('SMTP server is stopping...')
        controller.stop()

# Si el script se ejecuta directamente, iniciamos el servidor SMTP
if __name__ == "__main__":
    run()

"""
Notas de Seguridad:
- Este código inicia un servidor SMTP en localhost en el puerto 1025 para propósitos de desarrollo y prueba.
- En producción, no se debe utilizar un servidor SMTP de esta manera ya que:
    * No hay autenticación para el envío de correos.
    * No hay cifrado de las comunicaciones (como TLS/SSL).
    * Es susceptible a abuso si se deja accesible externamente.
- Recomendaciones para producción:
    * Utilizar un servicio de correo electrónico seguro y confiable (por ejemplo, SendGrid, Amazon SES, Gmail SMTP).
    * Configurar autenticación (por ejemplo, mediante OAuth o credenciales seguras).
    * Asegurarse de que las comunicaciones estén cifradas (utilizando TLS/SSL).
    * Implementar medidas de seguridad adicionales como listas blancas de IP, y límites de tasa para prevenir abuso.
"""
