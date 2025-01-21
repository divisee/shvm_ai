FROM vllm/vllm-openai:latest

# Установим переменную окружения для указания кеша Hugging Face
ENV HF_HOME=/model_cache

# Запуск модели
CMD ["--model", "divisee/Magic-psy-LoRA-Qwen-Finetuned"]