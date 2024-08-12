from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

key = "c1f73014bf3b4b4ab523305c237f6e3d"
endpoint = "https://content-safety-check.cognitiveservices.azure.com/"

client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
def analyser(prompt):
    request = AnalyzeTextOptions(text=prompt)
    return client.analyze_text(request)
