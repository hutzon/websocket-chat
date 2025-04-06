import boto3

# Inicializa el recurso de DynamoDB utilizando boto3
dynamodb = boto3.resource('dynamodb')

# Obtiene la referencia a la tabla de DynamoDB llamada 'WebSocketConnections'
table = dynamodb.Table('WebSocketConnections')

def lambda_handler(event, context):
    """
    Función Lambda que maneja la desconexión de un cliente WebSocket.
    Elimina el registro de la conexión del cliente en la tabla de DynamoDB.

    Parámetros:
    - event: Diccionario que contiene los datos del evento que activó el Lambda.
             Incluye información sobre la conexión WebSocket en 'requestContext'.
    - context: Objeto que proporciona información sobre el entorno de ejecución del Lambda.

    Funcionalidad:
    - Extrae el ID de la conexión (connectionId) del evento.
    - Elimina el registro correspondiente en la tabla de DynamoDB.
    - Retorna una respuesta indicando si la desconexión fue exitosa o fallida.

    Retorna:
    - Un diccionario con:
        - 'statusCode': Código HTTP que indica el resultado de la operación.
        - 'body': Mensaje indicando si la desconexión fue exitosa o fallida.
    """
    # Extrae el ID de la conexión desde el contexto del evento
    connection_id = event['requestContext']['connectionId']  # ID único de la conexión WebSocket

    try:
        # Elimina el registro de la conexión en la tabla de DynamoDB
        table.delete_item(Key={'connectionId': connection_id})
        # Retorna un código de éxito HTTP 200 si la operación fue exitosa
        return {
            'statusCode': 200,
            'body': 'Disconnected'
        }
    except Exception as e:
        # Maneja errores y registra el mensaje de error en los logs
        print(f"Error deleting connectionId: {e}")
        # Retorna un código de error HTTP 500 si algo falla
        return {
            'statusCode': 500,
            'body': 'Failed to disconnect'
        }