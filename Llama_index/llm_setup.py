from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import PromptTemplate, Settings
import torch

llm = None
MODEL_NAME = "C:/Users/NeliOdei/Documents/Alt/Mistral-7B-Instruct-v0.2"

def load_llm():
    global llm
    if llm is None:
        print("Загрузка модели...")

        prompt_template = """
        Используя предоставленный контекст, ответьте на вопрос в конце на русском языке.
        Если вы не знаете ответа, просто скажите, что не знаете. Не придумывайте ответ.
        ==========
        {context_str}
        ==========
        Вопрос: {query_str}
        """
        prompt = PromptTemplate(prompt_template)

        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        llm = HuggingFaceLLM(
            context_window=4096,
            max_new_tokens=256,
            generate_kwargs={"temperature": 0.2, "do_sample": False},
            query_wrapper_prompt=prompt,
            tokenizer_name=MODEL_NAME,
            model_name=MODEL_NAME,
            device_map=device,
            model_kwargs={"torch_dtype": torch.float16, "load_in_8bit": True}
        )
        print("Модель загружена.")
        Settings.llm = llm
    return llm