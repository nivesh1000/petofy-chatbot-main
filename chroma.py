import chromadb
from chunkmaker import read_chunks


class Chromaappender:
    def __init__(self, db_name, dblocation, sdloc) -> None:
        self.db_name = db_name
        self.dbloc = dblocation
        self.sdloc = sdloc
        self.client = chromadb.PersistentClient(path=f"{self.dbloc}")
        if self.exist_check() != 0:
            self.collection_add()

    def collection_add(self):
        self.collection = self.client.create_collection(name=self.db_name)
        for i, chunk in enumerate(read_chunks(self.sdloc)):
            self.collection.add(documents=chunk, ids=[f"{i}"])

    def exist_check(self):
        existing_collections = self.client.list_collections()
        if self.db_name in [col.name for col in existing_collections]:
            return 0
        
    def similarity_search(self,query_text):
        self.collection = self.client.get_collection(name=self.db_name)
        self.query_text = query_text
        results = self.collection.query(
        query_texts=[query_text], n_results=2, include=["documents", "distances"]
        )  
        documents = results["documents"]
        s = ""
        for doc in documents:
            s += doc[0]
        return s
