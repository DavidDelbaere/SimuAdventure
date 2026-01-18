from google import genai
from pydantic import BaseModel, Field
from keyRequest import keyRequest
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Response(BaseModel):
    story: str = Field(description="The text of the story")
    type: int = Field(description="The number corresponding with the response type")

def _get_key_index() -> int:
    with open(os.path.join(BASE_DIR, "keyRequestCount.txt"), "r") as f:
        return int(f.readline().strip() or "0")

def _bump_key_index(n: int) -> None:
    # Optional: only if you actually want the counter to advance.
    with open(os.path.join(BASE_DIR, "keyRequestCount.txt"), "w") as f:
        f.write(str(n + 1))

def _split_into_chunks(text: str):
    # Split into "sentences" while keeping punctuation
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]

INTRO_PROMPT = (
    "I want to participate in a text-based adventure story. "
    "Do not be too dramatic with the story; make it realistic. "
    "Generate an introduction to my story. Do not include any preambulatory text; "
    "I want your response to begin with the story. "
    "Based on how the story begins, ask me to (1) press a button, (2) turn the lights on, "
    "or (3) heat something up. "
    "Be clear which of these 3 things you are asking me to do, but do not explicitly say it. "
    "Your story will be a total of 5 text blocks long."
)

def generate_intro_story_chunks():
    n = _get_key_index()
    client = genai.Client(api_key=keyRequest(n))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=INTRO_PROMPT,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Response.model_json_schema(),
        },
    )

    parsed = json.loads(response.text)
    story = parsed["story"].strip()

    chunks = _split_into_chunks(story)

    # Optional: advance your key counter if that's your intent
    # _bump_key_index(n)

    return chunks, story

def generate_next_story_chunks(story_so_far, user_input, turn):
    n = _get_key_index()
    client = genai.Client(api_key=keyRequest(n))

    prompt = (
        f"Story so far:\n{story_so_far}\n\n"
        f"User input: {user_input}\n\n"
        f"This is turn number {turn + 1} out of 5 total story blocks (block 1 was the introduction).\n\n"
        "Continue the story naturally in a realistic tone. "
        "Then ask the user to do ONE of these actions next: "
        "(1) press a button, (2) turn the lights on, or (3) heat something up. "
        "Be clear which action you want, but do not explicitly list the numbers."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Response.model_json_schema(),
        },
    )

    parsed = json.loads(response.text)
    new_story = parsed["story"].strip()

    full_story = (story_so_far + " " + new_story).strip()
    chunks = _split_into_chunks(new_story)

    return chunks, full_story

def generate_conclusion_chunks(story_so_far):
    n = _get_key_index()
    client = genai.Client(api_key=keyRequest(n))

    prompt = (
        "Generate the conclusion to this text-based adventure story. "
        "Make it realistic, coherent, and fitting given the events so far. "
        "Do not ask the user to take another action. Do not offer choices. "
        "End definitively.\n\n"
        f"Story so far:\n{story_so_far}"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Response.model_json_schema(),
        },
    )

    parsed = json.loads(response.text)
    conclusion = parsed["story"].strip()

    chunks = _split_into_chunks(conclusion)
    return chunks, conclusion
