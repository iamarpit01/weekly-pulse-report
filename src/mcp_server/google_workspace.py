from typing import List
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage
from src.logger import get_logger
from src.mcp_server.auth import get_credentials

logger = get_logger(__name__)

def get_docs_service():
    creds = get_credentials()
    return build('docs', 'v1', credentials=creds)

def get_gmail_service():
    creds = get_credentials()
    return build('gmail', 'v1', credentials=creds)

def docs_read_document(document_id: str) -> str:
    """Reads the text content of a Google Doc."""
    service = get_docs_service()
    doc = service.documents().get(documentId=document_id).execute()
    
    content = ""
    for el in doc.get('body').get('content', []):
        if 'paragraph' in el:
            for element in el.get('paragraph').get('elements'):
                if 'textRun' in element:
                    content += element.get('textRun').get('content')
    return content

def docs_append_text(document_id: str, text: str) -> str:
    """Appends markdown/text to the end of a Google Doc."""
    service = get_docs_service()
    
    doc = service.documents().get(documentId=document_id).execute()
    content = doc.get('body').get('content')
    
    # Calculate the end index to append the new text
    end_index = content[-1]['endIndex'] - 1 if content else 1
    
    requests = [
        {
            'insertText': {
                'location': {
                    'index': end_index,
                },
                'text': "\n" + text + "\n\n"
            }
        }
    ]

    result = service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()
    return str(result)

def _create_message(to: List[str], subject: str, html_body: str):
    message = EmailMessage()
    message.set_content("Please enable HTML to view this email.")
    message.add_alternative(html_body, subtype='html')
    message['To'] = ", ".join(to)
    message['Subject'] = subject
    
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': encoded_message}

def gmail_create_draft(to: List[str], subject: str, html_body: str) -> str:
    """Creates a draft email in Gmail."""
    service = get_gmail_service()
    raw_msg = _create_message(to, subject, html_body)
    
    draft = service.users().drafts().create(
        userId='me', body={'message': raw_msg}).execute()
    
    return f"Draft created successfully. Draft ID: {draft['id']}"

def gmail_send_message(to: List[str], subject: str, html_body: str) -> str:
    """Sends an email directly via Gmail."""
    service = get_gmail_service()
    raw_msg = _create_message(to, subject, html_body)
    
    sent_message = service.users().messages().send(
        userId='me', body=raw_msg).execute()
    
    return f"Message sent successfully. Message ID: {sent_message['id']}"
