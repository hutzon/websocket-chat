import boto3
import os

# Inicializa el recurso de DynamoDB utilizando boto3
dynamodb = boto3.resource('dynamodb')

# Obtiene la referencia a la tabla de DynamoDB llamada 'WebSocketConnections'
table = dynamodb.Table('WebSocketConnections')

def lambda_handler(event, context):
    """
    Función Lambda que maneja las conexiones WebSocket y almacena información
    de la conexión en una tabla de DynamoDB.

    Parámetros:
    - event: Diccionario que contiene los datos del evento que activó el Lambda.
             Incluye información sobre la conexión WebSocket en 'requestContext'.
    - context: Objeto que proporciona información sobre el entorno de ejecución del Lambda.

    Retorna:
    - Un diccionario con:
        - 'statusCode': Código HTTP que indica el resultado de la operación.
        - 'body': Mensaje indicando si la conexión fue exitosa o fallida.
    """
    # Extrae el ID de la conexión, el nombre del dominio y la etapa del evento
    connection_id = event['requestContext']['connectionId']  # ID único de la conexión WebSocket
    domain_name = event['requestContext']['domainName']      # Nombre del dominio asociado a la conexión
    stage = event['requestContext']['stage']                 # Etapa (stage) del WebSocket (por ejemplo, 'dev', 'prod')

    try:
        # Guarda la información de la conexión en la tabla de DynamoDB
        table.put_item(Item={
            'connectionId': connection_id,  # Clave primaria: ID de la conexión
            'domainName': domain_name,      # Dominio del cliente conectado
            'stage': stage                  # Etapa del WebSocket
        })
        # Retorna un código de éxito HTTP 200 si la operación fue exitosa
        return {
            'statusCode': 200,
            'body': 'Connected'
        }
    except Exception as e:
        # Maneja errores y registra el mensaje de error en los logs
        print(f"Error saving connectionId: {e}")
        # Retorna un código de error HTTP 500 si algo falla
        return {
            'statusCode': 500,
            'body': 'Failed to connect'
        }