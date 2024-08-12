from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')

client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
def analyser(prompt):
    request = AnalyzeTextOptions(text=prompt)
    return client.analyze_text(request)
