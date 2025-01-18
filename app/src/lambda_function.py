import os
import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    region_name = os.environ['REGION_NAME']
    access_key_id = os.environ['LAMBDA_AWS_ACCESS_KEY_ID']
    secret_access_key = os.environ['LAMBDA_AWS_SECRET_ACCESS_KEY']
    session_token = os.environ.get('LAMBDA_AWS_SESSION_TOKEN', None)
    cognito_user_pool_id = os.environ['COGNITO_USER_POOL_ID']

    cognito_client = boto3.client(
        'cognito-idp',
        region_name=region_name,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token
    )

    for record in event['Records']:
        message = json.loads(record['body'])
        user_id = extract_user_id(message)

        try:
            email = get_user_email(cognito_client, cognito_user_pool_id, user_id)
            
            if email:
                logger.info(f"Processamento bem-sucedido. Usuário: {user_id}, E-mail: {email}")
            else:
                logger.warning(f"E-mail não encontrado para o usuário {user_id}")

        except Exception as e:
            logger.error(f"Erro ao buscar o e-mail do usuário {user_id}: {str(e)} | Request ID: {context.aws_request_id}")

    # Devido a limitações do lab aws o SES não foi integrado!
    return {
        "statusCode": 200,
        "body": json.dumps("Mensagens processadas e logs registrados.")
    }

def extract_user_id(message):
    try:
        return message['Records'][0]['s3']['object']['key'].split('/')[1]
    except KeyError:
        return 'Usuário não identificado'

def get_user_email(cognito_client, user_pool_id, user_id):
    try:
        response = cognito_client.admin_get_user(
            UserPoolId=user_pool_id,
            Username=user_id
        )
        
        for attribute in response['UserAttributes']:
            if attribute['Name'] == 'email':
                return attribute['Value']
        
        return None
    except cognito_client.exceptions.UserNotFoundException:
        raise Exception(f"Usuário {user_id} não encontrado no Cognito.")
    except Exception as e:
        raise Exception(f"Erro ao buscar dados do usuário {user_id} no Cognito: {str(e)}")