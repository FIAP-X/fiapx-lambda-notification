import os
import json
import unittest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler, extract_user_id, get_user_email

class TestLambdaHandler(unittest.TestCase):

    @patch('lambda_function.boto3.client')
    def test_lambda_handler_success(self, mock_boto_client):

        os.environ['REGION_NAME'] = 'us-east-1'
        os.environ['LAMBDA_AWS_ACCESS_KEY_ID'] = 'fake-access-key'
        os.environ['LAMBDA_AWS_SECRET_ACCESS_KEY'] = 'fake-secret-key'
        os.environ['COGNITO_USER_POOL_ID'] = 'fake-user-pool-id'

        mock_cognito_client = MagicMock()
        mock_boto_client.return_value = mock_cognito_client
        
        event = {
            'Records': [
                {'body': json.dumps({'Records': [{'s3': {'object': {'key': 'folder/user123'}}}]})}
            ]
        }
        context = MagicMock()
        context.aws_request_id = 'fake-request-id'

        mock_cognito_client.admin_get_user.return_value = {
            'UserAttributes': [
                {'Name': 'email', 'Value': 'user123@example.com'}
            ]
        }

        response = lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 200)
        self.assertIn("Mensagens processadas", response['body'])
        mock_cognito_client.admin_get_user.assert_called_once_with(
            UserPoolId='fake-user-pool-id',
            Username='user123'
        )

    def test_extract_user_id_valid(self):
        message = {'Records': [{'s3': {'object': {'key': 'folder/user123'}}}]}
        user_id = extract_user_id(message)
        self.assertEqual(user_id, 'user123')

    def test_extract_user_id_invalid(self):
        message = {'Records': [{'s3': {}}]}
        user_id = extract_user_id(message)
        self.assertEqual(user_id, 'Usuário não identificado')

    @patch('lambda_function.boto3.client')
    def test_get_user_email_success(self, mock_boto_client):
        mock_cognito_client = MagicMock()
        mock_boto_client.return_value = mock_cognito_client

        mock_cognito_client.admin_get_user.return_value = {
            'UserAttributes': [
                {'Name': 'email', 'Value': 'user123@example.com'}
            ]
        }

        email = get_user_email(mock_cognito_client, 'fake-user-pool-id', 'user123')
        self.assertEqual(email, 'user123@example.com')

    @patch('lambda_function.boto3.client')
    def test_get_user_email_not_found(self, mock_boto_client):
        mock_cognito_client = MagicMock()
        mock_boto_client.return_value = mock_cognito_client

        mock_cognito_client.admin_get_user.side_effect = mock_cognito_client.exceptions.UserNotFoundException

        with self.assertRaises(mock_cognito_client.exceptions.UserNotFoundException) as context:
            get_user_email(mock_cognito_client, 'fake-user-pool-id', 'user123')

        self.assertIn("UserNotFoundException", str(context.exception))

    @patch('lambda_function.boto3.client')
    def test_get_user_email_error(self, mock_boto_client):
        mock_cognito_client = MagicMock()
        mock_boto_client.return_value = mock_cognito_client

        mock_cognito_client.admin_get_user.side_effect = Exception("Unknown error")

        with self.assertRaises(Exception) as context:
            get_user_email(mock_cognito_client, 'fake-user-pool-id', 'user123')

        self.assertIn("Erro ao buscar dados do usuário user123 no Cognito", str(context.exception))

if __name__ == '__main__':
    unittest.main()