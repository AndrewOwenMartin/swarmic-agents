import requests
from swarmic_agents.chat.type import ChatError, ChatRequest, ChatResponse, ChatInput

url = "http://localhost:1234/api/v1/chat"
model_name = "qwen/qwen3.6-27b"


def make_payload(texts: list[str]) -> ChatRequest:
    """Create a chat request payload from a list of text strings."""
    return ChatRequest(
        model=model_name,
        input=[ChatInput(type="text", content=text) for text in texts],
    )


def simple_chat(query: str) -> ChatResponse:
    """Send a simple text query to the chat API."""
    payload = make_payload(texts=[query])
    response = send_payload(payload)
    return response


def file_chat(file_paths: list[str], query: list[str]):
    """Send file contents along with queries to the chat API."""
    texts: list[str] = []
    for file_path in file_paths:
        with open(file_path) as f:
            texts.append(f.read())

    texts.extend(query)
    payload = make_payload(texts=texts)
    data = send_payload(payload)
    return data


def send_payload(payload: ChatRequest) -> ChatResponse:
    """Send a chat request payload to the API endpoint."""
    response = requests.post(url, json=payload.model_dump())
    response_json = response.json()
    if "error" in response_json:
        raise ChatError(response_json["error"])
    chat_response = ChatResponse.model_validate(response.json())
    return chat_response


def main():
    chat_response = simple_chat(query="Hi.")
    print("Response:", chat_response)


if __name__ == "__main__":
    main()
