import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account
from src.logger import get_logger

logger = get_logger(__name__)

# Scopes required for Docs and Gmail
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.send'
]

def get_credentials():
    creds = None
    
    # 1. Check for Service Account first (Best for Cron/Automated jobs)
    service_account_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if service_account_file and os.path.exists(service_account_file):
        logger.info(f"Authenticating via Service Account: {service_account_file}")
        creds = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES)
        return creds
        
    # 2. Fallback to User OAuth2 (Requires browser login once)
    logger.info("Authenticating via User OAuth2 Credentials")
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError("Missing 'credentials.json' for OAuth2 flow. Please download it from GCP Console or set GOOGLE_APPLICATION_CREDENTIALS for a service account.")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    return creds
