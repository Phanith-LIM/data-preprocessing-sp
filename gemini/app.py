import json
import google.generativeai as genai
from helper import extract_words_from_files




page_number = 4
genai.configure(api_key="")
path = f'/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/processing/WMC-Internation/clean/{page_number}'

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[
        
    ]
)


words = extract_words_from_files(path)
text = f'''
Convert the following English words into their phonetic equivalents in Khmer: {words}. Return the result as a JSON object where each English word is the key and its Khmer phonetic equivalent is the value.
Use this format:
{{
    "3": {{
        "xinjiang": "ស៊ីនជាំង",
        "fcc": "អេហ្វស៊ីស៊ី"
    }}
}}
'''
response = chat_session.send_message(text)
print(response)
json_response = json.loads(response.candidates[0].content.parts[0].text)

output_path = f"output/{page_number}.json"
with open(output_path, 'w') as f:
    json.dump(json_response, f, ensure_ascii=False)

print(f"JSON response saved to {output_path}")