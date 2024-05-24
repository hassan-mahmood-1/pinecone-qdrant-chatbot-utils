from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
from qdrant_client import QdrantClient

load_dotenv()
qdrant_url = os.getenv("qdrant_url")
qdrant_api_key = os.getenv("qdrant_api_key")



#embedding model
embed_model = "BAAI/bge-small-en-v1.5"
embed_fn = HuggingFaceEmbeddings(model_name=embed_model)

class managerQdrant:

    def create_new_vectorstore_qdrant(doc_list, collection_name):
        try:
            qdrant = Qdrant.from_documents(
                documents=doc_list,
                embedding=embed_fn,
                url=qdrant_url,
                prefer_grpc=True,
                api_key=qdrant_api_key,
                collection_name=collection_name,
            )
            return qdrant
        except Exception as ex:
            raise Exception({"Error": str(ex)})
        

    def load_local_vectordb_using_qdrant(collection_name):
        try:
            qdrant_client = QdrantClient(
                url=qdrant_url,
                # prefer_grpc=True,
                api_key=qdrant_api_key,
            )
            qdrant_store = Qdrant(qdrant_client, collection_name, embed_fn)
            return qdrant_store
        except Exception as e:
            raise Exception(f"error while loading vectordb:'{str(e)}'")
    



    def delete_vectordb_using_qdrant( vectordb_folder_path):
        try:
            qdrant_client = QdrantClient(
                url=qdrant_url, 
                prefer_grpc=True,
                api_key=qdrant_api_key,
            )
            qdrant_client.delete_collection(collection_name=vectordb_folder_path)
        except Exception as e:
            raise Exception(str(e)) 
        return True 
