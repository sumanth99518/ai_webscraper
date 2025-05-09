import requests
import json
from key import API
template_prase = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    "5. **structure format:**simple clean format."
    "   Use the following format:\n\n"
    "   header:result1\n"
    "   header:result2\n"
)
template = (
    "You are tasked with extracting atleast 10 the specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string (''). "
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text. "
    "5. **Numbers and Symbols:** In numbers dont use ','(commas) ,Ignore symbols."
    "6. **CSV Format:** Present the extracted information in a structured CSV format. Use headers to clearly label the data columns. "
    "   Use the following format:\n\n"
    "   Header1,Header2,Header3\n"
    "   Value1,Value2,Value3\n"
    "   Value4,Value5,Value6\n\n"
)
def call_with_openrouter(chunks, parse_description):
    headers = {
        "Authorization": f"Bearer {API}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com",
        "X-Title": "Your App Name"
    }

    parsed_results = []
    total = len(chunks)
    print("----------------------started OpenRouter")

    for idx, chunk in enumerate(chunks, 1):
        print(f"{idx} in {total}")
        
        # Fill in the prompt template
        prompt = template_prase.format(dom_content=chunk, parse_description=parse_description)

        data = {
            "model": "meta-llama/llama-4-maverick:free",
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ]
        }

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            parsed_results.append(reply)
        else:
            print("Error:", response.status_code, response.text)
            parsed_results.append("")

    print("----------------------end OpenRouter")
    return "\n".join(parsed_results)
def parse_with_gemini(chunks, parse_description):
    headers = {
        "Authorization": f"Bearer {API}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com",
        "X-Title": "Your App Name"
    }

    parsed_results = []
    total = len(chunks)
    print("----------------------started OpenRouter")


        
        # Fill in the prompt template
    prompt = template.format(dom_content=chunks, parse_description=parse_description)

    data = {
            "model": "meta-llama/llama-4-maverick:free",
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ]
        }

    response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        parsed_results.append(reply)
        
    else:
        print("Error:", response.status_code, response.text)
        parsed_results.append("")

    print("----------------------end OpenRouter")
    return "\n".join(parsed_results)