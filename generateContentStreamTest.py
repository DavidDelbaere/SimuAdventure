from google import genai
from keyRequest import keyRequest
import time

#select first available key in keys.txt
n = (int)(open('keyRequestCount.txt', 'r').readline())
client = genai.Client(api_key=keyRequest(n))

response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="Write me a recipe for chocolate chip cookies."
)

n += 1

for chunk in response:
    print(chunk.text, end="")
    time.sleep(len(chunk.text.split())/6)

#update total number of requests
with open('keyRequestCount.txt', 'w') as file:
    file.write((str)(n))