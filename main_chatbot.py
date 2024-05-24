from langchain.document_loaders import Docx2txtLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document










class fileProcessing():
    def __init__(self, chunk_size=750) -> None:
        self.chunk_size = chunk_size



    def get_pdf_splits(self, pdf_file: str, filename: str):
        try:
            loader = PyMuPDFLoader(pdf_file)
            pages = loader.load()
            textsplit = RecursiveCharacterTextSplitter(
                separators=["\n\n", ".", "\n"],
                chunk_size=self.chunk_size, chunk_overlap=15,
                length_function=len)
            doc_list = []
            for pg in pages:
                pg_splits = textsplit.split_text(pg.page_content)
                for page_sub_split in pg_splits:
                    metadata = {"source": filename}
                    doc_string = Document(page_content=page_sub_split, metadata=metadata)
                    doc_list.append(doc_string)
            return doc_list
            # return pages
        except Exception as e:
            raise Exception(str(e))
    


    def get_docx_splits(self, docx_file: str, filename: str):
        try:
            loader = Docx2txtLoader(str(docx_file))
            txt = loader.load()
            textsplit = RecursiveCharacterTextSplitter(
                separators=["\n\n", ".", "\n"],
                chunk_size=self.chunk_size, chunk_overlap=15,
                length_function=len)

            doc_list = textsplit.split_text(txt[0].page_content)
            new_doc_list = []
            for page_sub_split in doc_list:
                metadata = {"source": filename}
                doc_string = Document(page_content=page_sub_split, metadata=metadata)
                new_doc_list.append(doc_string)
            return new_doc_list
        except Exception as e:
            raise Exception(str(e))