
import json

def lambda_handler(event, context):
    """
    Función Lambda que actúa como manejador predeterminado para rutas desconocidas
    en una conexión WebSocket.

    Parámetros:
    - event: Diccionario que contiene los datos del evento que activó el Lambda.
             Incluye información sobre la conexión WebSocket en 'requestContext'.
    - context: Objeto que proporciona información sobre el entorno de ejecución del Lambda.

    Funcionalidad:
    - Extrae información clave del evento, como el ID de la conexión, la clave de la ruta (routeKey)
      y el cuerpo del mensaje (body).
    - Registra en los logs información sobre la ruta desconocida y los datos de la conexión.
    - Retorna una respuesta indicando que no se encontró una acción coincidente para la ruta.

    Retorna:
    - Un diccionario con:
        - 'statusCode': Código HTTP 200 indicando que la solicitud fue procesada.
        - 'body': Mensaje en formato JSON indicando que se activó la ruta predeterminada.
    """
    # Extrae el ID de la conexión desde el contexto del evento
    connection_id = event['requestContext']['connectionId']  # ID único de la conexión WebSocket
    # Extrae la clave de la ruta (routeKey) que activó el evento
    route_key = event['requestContext']['routeKey']          # Ruta específica del WebSocket
    # Obtiene el cuerpo del mensaje enviado, si existe
    body = event.get('body', '')                             # Cuerpo del mensaje enviado por el cliente

    # Registra en los logs información sobre la ruta desconocida y los datos de la conexión
    print(f"[Default Handler] Unknown routeKey: {route_key}")  # Log de la ruta desconocida
    print(f"Connection ID: {connection_id}")                  # Log del ID de la conexión
    print(f"Raw body: {body}")                                # Log del cuerpo del mensaje

    # Retorna una respuesta indicando que no se encontró una acción coincidente
    return {
        'statusCode': 200,  # Código HTTP de éxito
        'body': json.dumps('Default route triggered. No matching action found.')  # Mensaje en formato JSON
    }