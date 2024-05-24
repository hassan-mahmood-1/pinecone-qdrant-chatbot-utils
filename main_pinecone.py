from pinecone import Pinecone, ServerlessSpec
import os
from langchain_pinecone import PineconeVectorStore as lang_pinecone
pinecone_key=os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_key)




class managerPinecone:

    def create_index_pinecone_serverless(index):
        try:
            serverless_spec = ServerlessSpec(cloud="aws", region = "us-west-2")
            check=pc.list_indexes().names()
            if index not in check:
                pc.create_index(name=index, metric="cosine",spec=serverless_spec,dimension=384)
                return True
            return False
        except Exception as ex:
            return str(ex)
        
    def check_index(index):
        try:
            check=pc.list_indexes().names()
            if index not in check:
                return False
            return True
        except Exception as ex:
            return str(ex)
    
    def del_index_pinecone(index):
        try:
            check=pc.list_indexes().names()
            if index not in check:
                del_index=pc.delete_index(index)
                return del_index
            else:
                return False
        except Exception as ex:
            return str(ex)
        
    def data_upsert(all_texts, embed_fn,index):
        try:
            vector= lang_pinecone.from_documents(all_texts, embed_fn, index_name=index) 
            return True
        except Exception as ex:
            return str(ex)
        

    def initialize_pinecone(index,embed_fn):
        try:
            vectordb = lang_pinecone(index= index, embedding=embed_fn, text_key="text")
            return vectordb
        except Exception as ex:
            return str(ex)
        

    def migration_serverless_to_serverless(merged_list,source_index,dest_index):
        for vec_id in merged_list:
            try:
                vector_info = source_index.fetch([vec_id])
                #get vector info 
                pageNo = vector_info['vectors'][vec_id]['metadata']['page_number']
                pageUrl=vector_info['vectors'][vec_id]['metadata']['page_url']
                text=vector_info['vectors'][vec_id]['metadata']['text']
                title=vector_info['vectors'][vec_id]['metadata']['title']
                embeddings=vector_info['vectors'][vec_id]['_data_store']['values'] 
                #Now lets call the upsert function 
                upsert_response = dest_index.upsert(vectors=[
                {
                    "id": vec_id,
                    "values": embeddings,
                    "metadata": {
                        "page_number":pageNo,
                        "page_url":pageUrl,
                        "text":text,
                        "title":title
                    }
                }])
            except:
                continue   

    def fetch_index_ids(index_name):
        try:
            all_ids=[]
            for ids in index_name.list():
                all_ids.append(ids)
            merged_list = [item for sublist in all_ids for item in sublist]
            return merged_list
        except Exception as ex:
            return str(ex)

