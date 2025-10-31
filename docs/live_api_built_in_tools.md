Built-in tools for the Live API

bookmark_border
To see an example of Live API, run the "Getting Started with the Live API Native Audio" notebook in one of the following environments:

Open in Colab | Open in Colab Enterprise | Open in Vertex AI Workbench | View on GitHub

Live API-supported models come with the built-in ability to use the following tools:

Function calling
Code execution
Grounding with Google Search
Grounding with Vertex AI RAG Engine (Preview)
To enable a particular tool for usage in returned responses, include the name of the tool in the tools list when you initialize the model. The following sections provide examples of how to use each of the built-in tools in your code.

Supported models
You can use the Live API with the following models:

Model version	Availability level
gemini-live-2.5-flash	Private GA*
gemini-live-2.5-flash-preview-native-audio	Public preview
gemini-live-2.5-flash-preview-native-audio-09-2025	Public preview
* Reach out to your Google account team representative to request access.

Function calling
Use function calling to create a description of a function, then pass that description to the model in a request. The response from the model includes the name of a function that matches the description and the arguments to call it with.

All functions must be declared at the start of the session by sending tool definitions as part of the LiveConnectConfig message.

To enable function calling, include function_declarations in the tools list:

Python
Python


import asyncio
from google import genai
from google.genai import types

client = genai.Client(
    vertexai=True,
    project=GOOGLE_CLOUD_PROJECT,
    location=GOOGLE_CLOUD_LOCATION,
)
model = "gemini-live-2.5-flash"

# Simple function definitions
turn_on_the_lights = {"name": "turn_on_the_lights"}
turn_off_the_lights = {"name": "turn_off_the_lights"}

tools = [{"function_declarations": [turn_on_the_lights, turn_off_the_lights]}]
config = {"response_modalities": ["TEXT"], "tools": tools}

async def main():
    async with client.aio.live.connect(model=model, config=config) as session:
        prompt = "Turn on the lights please"
        await session.send_client_content(turns={"parts": [{"text": prompt}]})

        async for chunk in session.receive():
            if chunk.server_content:
                if chunk.text is not None:
                    print(chunk.text)
            elif chunk.tool_call:
                function_responses = []
                for fc in tool_call.function_calls:
                    function_response = types.FunctionResponse(
                        name=fc.name,
                        response={ "result": "ok" } # simple, hard-coded function response
                    )
                    function_responses.append(function_response)

                await session.send_tool_response(function_responses=function_responses)


if __name__ == "__main__":
    asyncio.run(main())
  
For examples using function calling in system instructions, see our best practices example.

Code execution
You can use code execution with the Live API to generate and execute Python code directly. To enable code execution for your responses, include code_execution in the tools list:

Python


import asyncio
from google import genai
from google.genai import types


client = genai.Client(
    vertexai=True,
    project=GOOGLE_CLOUD_PROJECT,
    location=GOOGLE_CLOUD_LOCATION,
)
model = "gemini-live-2.5-flash"

tools = [{'code_execution': {}}]
config = {"response_modalities": ["TEXT"], "tools": tools}

async def main():
    async with client.aio.live.connect(model=model, config=config) as session:
        prompt = "Compute the largest prime palindrome under 100000."
        await session.send_client_content(turns={"parts": [{"text": prompt}]})

        async for chunk in session.receive():
            if chunk.server_content:
                if chunk.text is not None:
                    print(chunk.text)
            
                model_turn = chunk.server_content.model_turn
                if model_turn:
                    for part in model_turn.parts:
                      if part.executable_code is not None:
                        print(part.executable_code.code)

                      if part.code_execution_result is not None:
                        print(part.code_execution_result.output)

if __name__ == "__main__":
    asyncio.run(main())
  
Grounding with Google Search
You can use Grounding with Google Search with the Live API by including google_search in the tools list:

Python


import asyncio
from google import genai
from google.genai import types

client = genai.Client(
    vertexai=True,
    project=GOOGLE_CLOUD_PROJECT,
    location=GOOGLE_CLOUD_LOCATION,
)
model = "gemini-live-2.5-flash"


tools = [{'google_search': {}}]
config = {"response_modalities": ["TEXT"], "tools": tools}

async def main():
    async with client.aio.live.connect(model=model, config=config) as session:
        prompt = "When did the last Brazil vs. Argentina soccer match happen?"
        await session.send_client_content(turns={"parts": [{"text": prompt}]})

        async for chunk in session.receive():
            if chunk.server_content:
                if chunk.text is not None:
                    print(chunk.text)

                # The model might generate and execute Python code to use Search
                model_turn = chunk.server_content.model_turn
                if model_turn:
                    for part in model_turn.parts:
                        if part.executable_code is not None:
                        print(part.executable_code.code)

                        if part.code_execution_result is not None:
                        print(part.code_execution_result.output)

if __name__ == "__main__":
    asyncio.run(main())
  
Grounding with Vertex AI RAG Engine (Preview)
You can use Vertex AI RAG Engine with the Live API for grounding, storing, and retrieving contexts:

Python


from google import genai
from google.genai import types
from google.genai.types import (Content, LiveConnectConfig, HttpOptions, Modality, Part)
from IPython import display

PROJECT_ID=YOUR_PROJECT_ID
LOCATION=YOUR_LOCATION
TEXT_INPUT=YOUR_TEXT_INPUT
MODEL_NAME="gemini-live-2.5-flash"

client = genai.Client(
   vertexai=True,
   project=PROJECT_ID,
   location=LOCATION,
)

rag_store=types.VertexRagStore(
   rag_resources=[
       types.VertexRagStoreRagResource(
           rag_corpus=  # Use memory corpus if you want to store context.
       )
   ],
   # Set `store_context` to true to allow Live API sink context into your memory corpus.
   store_context=True
)

async with client.aio.live.connect(
   model=MODEL_NAME,
   config=LiveConnectConfig(response_modalities=[Modality.TEXT],
                            tools=[types.Tool(
                                retrieval=types.Retrieval(
                                    vertex_rag_store=rag_store))]),
) as session:
   text_input=TEXT_INPUT
   print("> ", text_input, "\n")
   await session.send_client_content(
       turns=Content(role="user", parts=[Part(text=text_input)])
   )

   async for message in session.receive():
       if message.text:
           display.display(display.Markdown(message.text))
           continue
For more information, see Use Vertex AI RAG Engine in Gemini Live API.

(Public preview) Native audio
Preview

This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

Gemini 2.5 Flash with Live API introduces native audio capabilities, enhancing the standard Live API features. Native audio provides richer and more natural voice interactions through 30 HD voices in 24 languages. It also includes two new features exclusive to native audio: Proactive Audio and Affective Dialog.

Note: response_modalities=["TEXT"] is not supported for native audio.
Use Affective Dialog
Important: Affective Dialog can produce unexpected results.
Affective Dialog allows models using Live API native audio to better understand and respond appropriately to users' emotional expressions, leading to more nuanced conversations.

To enable Affective Dialog, set enable_affective_dialog to true in the setup message:

Python


config = LiveConnectConfig(
    response_modalities=["AUDIO"],
    enable_affective_dialog=True,
)