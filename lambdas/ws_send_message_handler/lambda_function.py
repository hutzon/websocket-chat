import boto3
import json
import os

# Inicializa el recurso de DynamoDB utilizando boto3
dynamodb = boto3.resource('dynamodb')

# Obtiene la referencia a la tabla de DynamoDB llamada 'WebSocketConnections'
table = dynamodb.Table('WebSocketConnections')

def lambda_handler(event, context):
    """
    Función Lambda que maneja la recepción de mensajes en una conexión WebSocket.
    Envía el mensaje recibido a todos los clientes conectados, incluyendo el cliente que lo envió.

    Parámetros:
    - event: Diccionario que contiene los datos del evento que activó el Lambda.
             Incluye información sobre la conexión WebSocket en 'requestContext'.
    - context: Objeto que proporciona información sobre el entorno de ejecución del Lambda.

    Funcionalidad:
    - Extrae el ID de la conexión, el dominio y la etapa del evento.
    - Utiliza la API de gestión de WebSocket para enviar mensajes.
    - Envía el `connectionId` al cliente que envió el mensaje.
    - Difunde el mensaje recibido a todos los clientes conectados.

    Retorna:
    - Un diccionario con:
        - 'statusCode': Código HTTP que indica el resultado de la operación.
        - 'body': Mensaje indicando si el envío fue exitoso.
    """
    # Extrae información del evento
    connection_id = event['requestContext']['connectionId']  # ID único de la conexión WebSocket
    domain_name = event['requestContext']['domainName']      # Nombre del dominio asociado a la conexión
    stage = event['requestContext']['stage']                 # Etapa (stage) del WebSocket

    # Configura el cliente de la API de gestión de WebSocket
    endpoint = f"https://{domain_name}/{stage}"  # URL del endpoint de WebSocket
    apig_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint)

    # Procesa el mensaje recibido del cliente
    try:
        body = json.loads(event.get('body', '{}'))  # Decodifica el cuerpo del mensaje
        message = body.get('data', 'Mensaje vacío')  # Obtiene el mensaje enviado por el cliente
    except json.JSONDecodeError:
        # Retorna un error si el mensaje no es válido
        return {'statusCode': 400, 'body': 'Mensaje no válido'}

    # Lee todas las conexiones activas desde la tabla de DynamoDB
    try:
        connections = table.scan().get('Items', [])  # Obtiene todos los registros de conexiones
    except Exception as e:
        print("Error leyendo conexiones:", e)  # Log del error
        return {'statusCode': 500, 'body': 'Error leyendo conexiones'}

    # Envía el connectionId al cliente que envió el mensaje
    try:
        apig_management_client.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps({'connectionId': connection_id})  # Envía el ID de conexión al cliente
        )
    except Exception as e:
        print(f"Error enviando su propio connectionId: {e}")  # Log del error

    # Envía el mensaje a todos los clientes conectados
    for conn in connections:
        try:
            apig_management_client.post_to_connection(
                ConnectionId=conn['connectionId'],  # ID de conexión del cliente
                Data=json.dumps({
                    'from': connection_id,  # ID del remitente
                    'message': message     # Mensaje enviado
                })
            )
        except Exception as e:
            print(f"Error enviando a {conn['connectionId']}: {e}")  # Log del error

    # Retorna una respuesta indicando que el mensaje fue enviado
    return {
        'statusCode': 200,
        'body': 'Mensaje enviado a todos los conectados'
    }