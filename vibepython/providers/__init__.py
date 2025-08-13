import os

PROVIDER = os.getenv("PROVIDER", "gpt4free")
if PROVIDER == "gpt4free":
    from .handler_gpt4free.generate import generate
elif PROVIDER == "openai":
    from .handler_openai.generate import generate
elif PROVIDER == "ollama":
    from .handler_ollama.generate import generate
else:
    print(f"Unknown provider: {PROVIDER}")
    exit(1)
