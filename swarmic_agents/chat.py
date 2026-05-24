import json
from typing import TypedDict, Literal
import requests

url = "http://localhost:1234/api/v1/chat"
model_name = "qwen/qwen3.6-27b"
tmp_out_file_name = "/tmp/out.json"
staff_page_input = "/Users/amartin/casting-portal/scratch/staff-page.md"

class ChatInput(TypedDict):
    type: str
    content: str

class ChatRequest(TypedDict):
    model: str
    input: list[ChatInput]
    reasoning: Literal["off", "on"] # = 'off'
    store: bool # = False
    

def make_payload(texts: list[str]) -> ChatRequest:
    return {
        "model": model_name,
        "input": [{"type": "text", "content": text} for text in texts],
        "reasoning": "off",
        "store": False,
    }


def file_chat(file_paths: list[str], query: list[str]):
    texts: list[str] = []
    for file_path in file_paths:
        with open(file_path) as f:
            texts.append(f.read())

    texts.extend(query)

    return make_payload(texts=texts)


def send_payload(payload):
    response = requests.post(url, json=payload)
    return response.json()



def print_data(data):
    for output_chunk in data["output"]:
        print("---", output_chunk["type"], "---")
        print(output_chunk["content"])


def main():
    payload = file_chat(
        file_paths=[staff_page_input],
        query=[
            "Write each of these four options into separate markdown files. These will be used by further agents so be concise and technical rather than explanatory."
        ],
    )
    data = send_payload(payload)

    print_data(data)


if __name__ == "__main__":
    main()
