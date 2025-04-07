from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def load_data_and_index(pdf_path):
    print("Загрузка и индексация PDF...")
    documents = SimpleDirectoryReader(input_files=[pdf_path]).load_data()
    
    # Use LlamaIndex's native HuggingFace embedding
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    print("PDF загружен и проиндексирован.")
    return index