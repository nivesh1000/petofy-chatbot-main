import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    HnswParameters,
    VectorSearchAlgorithmKind,
    VectorSearchAlgorithmMetric,
    VectorSearchProfile,
)
from azure.search.documents import SearchClient
from chunkmaker import read_chunks
from embeddingmaker import generate_embeddings


load_dotenv()
service_endpoint =os.getenv("SERVICE_ENDPOINT")
key = os.getenv("RESOURCE_KEY")


def create_index():

    credential = AzureKeyCredential(key)
    index_name = "petofy-vector-data"

    index_client = SearchIndexClient(endpoint=service_endpoint, credential=credential)

    index_fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            sortable=True,
            filterable=True,
            facetable=True,
        ),
        SearchableField(name="text_chunk", type=SearchFieldDataType.String),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="demoHnswProfile",
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="demoHnsw",
                kind=VectorSearchAlgorithmKind.HNSW,
                parameters=HnswParameters(
                    m=4,
                    ef_construction=400,
                    ef_search=500,
                    metric=VectorSearchAlgorithmMetric.COSINE,
                ),
            ),
        ],
        profiles=[
            VectorSearchProfile(
                name="demoHnswProfile",
                algorithm_configuration_name="demoHnsw",
            ),
        ],
    )

    index = SearchIndex(
        name=index_name,
        fields=index_fields,
        vector_search=vector_search,
    )
    result = index_client.create_or_update_index(index)

    print(f" {result.name} created")
    index_client.close()


def upload_to_index():
    search_client = SearchClient(
        endpoint=service_endpoint,
        index_name=os.getenv("INDEX_NAME"),
        credential=AzureKeyCredential(key),
    )
    loc=os.getenv("SCRAPE_DATA_LOC")
    for i,chunk in enumerate(read_chunks(loc)):
        vectors=generate_embeddings(chunk)
        final_chunk=[{
                "id": str(i),
                "text_chunk": str(chunk),
                "embedding": vectors,
            }]
        search_client.upload_documents(documents=final_chunk)
    print("Documents uploaded")
    search_client.close()
create_index()
upload_to_index()