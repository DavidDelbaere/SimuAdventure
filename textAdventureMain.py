from google import genai
from pydantic import BaseModel, Field # type: ignore
from keyRequest import keyRequest
from geminiPrompt import geminiPrompt
import time

i = 0

#select first available key in keys.txt
n = (int)(open('keyRequestCount.txt', 'r').readline())
client = genai.Client(api_key=keyRequest(n))

#structure response as JSON with 'text' and 'type' fields
class Response(BaseModel):
    story: str = Field(description="The text of the story")
    type: int = Field(description="The number corresponding with the response type you are asking me for")

#introductory prompt
preamble = client.models.generate_content_stream(
    model="gemini-2.5-flash", 
    contents="I want to participate in a text-based adventure story. Do not be too dramatic with the story; make it realistic. " \
    "Generate an introduction to my story. Do not include any preambulatory text; I want your response to begin with the story. " \
    "Based on how the story begins, ask me to (1) move, (2) heat something up, (3) cool something down, or (4) press a button. " \
    "Be clear which of these 4 things you are asking me to do, but do not explicitly say it. "
    "Your story will be a total of 5 text blocks long, with a response from me between each. Plan an ending accordingly.",
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Response.model_json_schema(),
    },
)

#print the text portion of the response
full_text = ""
story_started = False
marker = '"story": '

print("(1) ", end="")
for chunk in preamble:
    full_text += chunk.text
    
    # Check if we have reached the 'story' section yet
    if not story_started:
        if marker in full_text:
            story_started = True
            # Print any part of the 'story' that was in the same chunk as the marker
            start_index = full_text.find(marker) + len(marker)
            print(full_text[start_index:], end="", flush=True)
    else:
        # We are currently inside the 'story'
        # Check if the story has ended
        if "]" in chunk.text:
            content_before_end = chunk.text.split(',".')[0]
            print(content_before_end, end="", flush=True)
            story_started = False # Stop printing live
        else:
            print(chunk.text, end="", flush=True)

#write the story up to the current point as a reminder for Gemini
with open('story.txt', 'w') as file:
    file.write(full_text)

i += 1
n += 1

"""
#while still space on current key
while (i < 4):

    currentStory = open('story.txt', 'r').readline()

    promptContent = geminiPrompt(response.type) + " Generate the next part of the story based on this," \
    "ensuring that there is variation between each of the text blocks you generate and that the story will be a total of " \
    "5 text blocks long. Again, ask me to (1) move, (2) heat something up, (3) cool something down, or (4) press a button." \
    "Be clear which of these 4 things you are asking me to do, but do not explicitly say it." \
    "As a reminder, the story so far is: " + currentStory,

    print("\n" + (str)(promptContent) + "\n")

    geminiResponse = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=promptContent,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Response.model_json_schema(),
        },
    )

    response = Response.model_validate_json(geminiResponse.text)
    
    #write the story up to the current point as a reminder for Gemini
    with open('story.txt', 'a') as file:
        file.write(response.text)

    #print the text portion of the response
    print("(" + (str)(i+1) + ") " + response.text)
    
    if(n%20 == 19):
        i += 1
        n += 1
        break

    i += 1
    n += 1

currentStory = open('story.txt', 'r').readline()

conclusion = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Generate the conclusion to my story, using all of the previous text blocks in my adventure story to craft a fitting end." \
    "As a reminder, the story so far is: " + currentStory,
)

print("(" + (str)(i+1) + ") " + conclusion.text)

i += 1
n += 1

#update total number of key requests
with open('keyRequestCount.txt', 'w') as file:
    file.write((str)(n))
"""