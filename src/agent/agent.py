from __future__ import annotations
from config import load_settings
from llm import make_client

def main():
    settings = load_settings()
    client = make_client(settings)

    response = client.chat.completions.create(
        model=settings.model,
        messages=[{"role": "user", "content": "Hello, world!"}],
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()