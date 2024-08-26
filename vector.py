import os
os.environ["AZURESEARCH_FIELDS_CONTENT_VECTOR"] = "embedding"
os.environ["AZURESEARCH_FIELDS_CONTENT"] = "text_chunk"
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

 
 
class Embeddings(AzureOpenAIEmbeddings):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    def _embed_documents(self, texts):
        return super().embed_documents(texts)
 
    def embed_query(self, query):
        return super().embed_query(query)
 
    def __call__(self, input):
        return self._embed_documents(input)
 
 
class VectorSearch:
 
    def __init__(self):
        self.embeddings = Embeddings(
            azure_deployment=os.getenv("RESOURCE_DEPLOYEMENT_NAME"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
 
    def client(self):
        return AzureSearch(
            azure_search_endpoint=os.getenv("SERVICE_ENDPOINT"),
            azure_search_key=os.getenv("RESOURCE_KEY"),
            index_name=os.getenv("INDEX_NAME"),
            embedding_function=self.embeddings,
        )
 
    def searchvector(self, query, *, k=5, score_threshold=0.6):
        vector_store = self.client()
 
        return vector_store.similarity_search_with_relevance_scores(
            query=query,
            k=k,
            score_threshold=score_threshold
        )
 