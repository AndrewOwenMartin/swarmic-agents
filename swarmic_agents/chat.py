import json
import requests

url = "http://localhost:1234/api/v1/chat"
model_name = "qwen/qwen3.6-27b"
tmp_out_file_name = "/tmp/out.json"
staff_page_input = "/Users/amartin/casting-portal/scratch/staff-page.md"


def make_payload(texts: list[str]):
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


# def query_model():
#     payload = {
#             "model": model_name,
#             "input":  [
#                 {
#                     "type": "text",
#                     "content": open(staff_page_input).read(),
#                 },
#                 {
#                     "type": "text",
#                     "content": "Write each of these four options into separate markdown files. These will be used by further agents so be concise and technical rather than explanatory.",
#                 }
#             ],
#             # "input": "Write a python hello world in less than 100 words and less than 10 lines",
#             # "input":  "This is great, can you do the equivalent in c?",
#             "reasoning": "off",
#             "store": False,
#             # "previous_response_id": "resp_eee65e8d2806d56598f9abcb5202beb0325a0cf614ec13bc"
#     }
#
#     response = requests.post(url, json=payload)
#
#     data = response.json()
#
#     print("dumping")
#     with open("/tmp/out.json",'w') as f:
#         json.dump(data, f)
#
#     return data


def query_file():
    with open("/tmp/out.json", "r") as f:
        data = json.load(f)
    return data


def print_data(data):
    for output_chunk in data["output"]:
        print("---", output_chunk["type"], "---")
        print(output_chunk["content"])


def main(is_live):
    if is_live:
        # data = query_model()
        payload = file_chat(
            file_paths=[staff_page_input],
            query=[
                "Write each of these four options into separate markdown files. These will be used by further agents so be concise and technical rather than explanatory."
            ],
        )
        data = send_payload(payload)
    else:
        data = query_file()

    print_data(data)


if __name__ == "__main__":
    main(is_live=True)
