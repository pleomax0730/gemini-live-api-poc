Title: Gemini Live API: A Developer’s Practical Guide

URL Source: https://ai.plainenglish.io/gemini-live-api-a-developers-practical-guide-0fe7b83552b3

Published Time: 2025-08-10T20:37:22Z

Markdown Content:
Gemini Live API: A Developer’s Practical Guide | by Aswin Chandrasekaran | Artificial Intelligence in Plain English

===============

[Sitemap](https://ai.plainenglish.io/sitemap/sitemap.xml)

[Open in app](https://rsci.app.link/?%24canonical_url=https%3A%2F%2Fmedium.com%2Fp%2F0fe7b83552b3&%7Efeature=LoOpenInAppButton&%7Echannel=ShowPostUnderCollection&%7Estage=mobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fai.plainenglish.io%2Fgemini-live-api-a-developers-practical-guide-0fe7b83552b3&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fai.plainenglish.io%2Fgemini-live-api-a-developers-practical-guide-0fe7b83552b3&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![Image 3](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

[Artificial Intelligence in Plain English ----------------------------------------](https://ai.plainenglish.io/?source=post_page---publication_nav-78d064101951-0fe7b83552b3---------------------------------------)

·
Follow publication

[![Image 4: Artificial Intelligence in Plain English](https://miro.medium.com/v2/resize:fill:76:76/1*9zAmnK08gUCmZX7q0McVKw@2x.png)](https://ai.plainenglish.io/?source=post_page---post_publication_sidebar-78d064101951-0fe7b83552b3---------------------------------------)
New AI, ML and Data Science articles every day. Follow to join our 3.5M+ monthly readers.

Follow publication

Gemini Live API: A Developer’s Practical Guide
==============================================

[![Image 5: Aswin Chandrasekaran](https://miro.medium.com/v2/resize:fill:64:64/1*dfzjRyMxNX9ycwmzLY0GjA.png)](https://aswincsekar.medium.com/?source=post_page---byline--0fe7b83552b3---------------------------------------)

[Aswin Chandrasekaran](https://aswincsekar.medium.com/?source=post_page---byline--0fe7b83552b3---------------------------------------)

Follow

5 min read

·

Aug 10, 2025

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fai-in-plain-english%2F0fe7b83552b3&operation=register&redirect=https%3A%2F%2Fai.plainenglish.io%2Fgemini-live-api-a-developers-practical-guide-0fe7b83552b3&user=Aswin+Chandrasekaran&userId=d2e40d76143d&source=---header_actions--0fe7b83552b3---------------------clap_footer------------------)

3

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F0fe7b83552b3&operation=register&redirect=https%3A%2F%2Fai.plainenglish.io%2Fgemini-live-api-a-developers-practical-guide-0fe7b83552b3&source=---header_actions--0fe7b83552b3---------------------bookmark_footer------------------)

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D0fe7b83552b3&operation=register&redirect=https%3A%2F%2Fai.plainenglish.io%2Fgemini-live-api-a-developers-practical-guide-0fe7b83552b3&source=---header_actions--0fe7b83552b3---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![Image 6](https://miro.medium.com/v2/resize:fit:700/1*7kXJGBZwkUdj_f5-PW68nA.png)

Alright, let’s talk about the Gemini Live API. If you’re reading this, you’re ready to move beyond simple request-response models and build something truly interactive. This guide is for you — the developer at the keyboard. We’ll skip the marketing fluff and get straight into the patterns, pitfalls, and pro-tips that will make your life easier.

Part 1: The Two Modes of Conversation
-------------------------------------

The most fundamental concept to grasp is that the Live API has two distinct ways of communicating. Choosing the wrong one is like using a screwdriver to hammer a nail — it might work, but it’s messy and inefficient.

### `send_client_content`: The Turn-Based Chat

This is your go-to for structured, ordered communication. Think of it as a classic command-line interface or a chat app. The user types a message, presses enter, and waits for a response.

**When to use it:**

*   To kick off a session with an initial prompt or system instruction.
*   For user input from a text field.
*   Anytime the order of messages is critical and you have clear “turns.”

You signal the end of a turn with `turn_complete=True`. This is the "enter" key of the API.

#

# Use Case: Starting a conversation with a clear, single prompt.

#

import google.genai as genai

from google.genai import types

# ... (client initialization)

async with client.aio.live.connect(model=MODEL_NAME) as session:

 # We're sending one complete "turn" to the model.

 print("Sending initial prompt...")

 await session.send_client_content(

 turns=[

 types.Content(role='user', parts=[types.Part(text="Give me a step-by-step guide to making sourdough bread.")])

 ],

 # This tells Gemini: "I'm done with my thought, it's your turn."

 turn_complete=True

 )

 async for response in session.receive():

 if response.text:

 print(f"Gemini: {response.text}")
### `send_realtime_input`: The Open Phone Line

This is for the fast, fluid, and sometimes chaotic world of live media streaming. Think voice assistants or live video analysis. The goal here is low latency, not perfect order.

Get Aswin Chandrasekaran’s stories in your inbox
------------------------------------------------

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

**When to use it:**

*   Streaming audio chunks from a microphone.
*   Sending video frames from a camera.
*   When responsiveness is more important than sequential purity.

#

# Use Case: Streaming live audio from a file or microphone.

#

from pathlib import Path

# Let's pretend this is a chunk of audio from a live stream.

audio_bytes = Path("audio_chunk_01.pcm").read_bytes()

# Note: We use the dedicated 'audio' parameter. This is important!

# More on this in the Pro-Tips section.

# the audio should be raw pcm_16bit little endian and 16k sample rate

await session.send_realtime_input(

 audio=types.Blob(data=audio_bytes, mime_type="audio/pcm;rate=16000")

)
> **_Critical Rule: Don’t Cross the Streams_**
> 
> 
> _Seriously. Avoid mixing_`send_client_content`_and_`send_realtime_input`_within the same active conversation. Their underlying designs are fundamentally different. Trying to inject an ordered_`client_content`_message into a low-latency_`realtime_input`_stream will lead to unpredictable behavior and race conditions. Set your context first, then start your stream._

Part 2: Giving Your AI Superpowers with Tools
---------------------------------------------

This is where the magic happens. You can teach Gemini to use external functions, turning it from a conversationalist into an agent that can act.

### Step 1: Declare Your Toolkit on Connection

You can’t just ask Gemini to do something it doesn’t know exists. You must declare your available “tools” (functions) when you first connect using the `config`.

#

# Let's tell Gemini it has a tool to get the current weather.

#

tools = [{

 'function_declarations': [{

 'name': 'get_current_weather',

 'description': 'Returns the weather for a given city.',

 'parameters': {

 'type': 'object',

 'properties': { 'city': {'type': 'string'} }

 }

 }]

}]

config = {

 "tools": tools,

 "response_modalities": ['TEXT']

}

# Now, when we connect, Gemini knows it has this capability.

async with client.aio.live.connect(model=MODEL_NAME, config=config) as session:

 # ...

 pass
### Step 2: Listen for the `tool_call` and Respond

When a user’s request triggers a tool, Gemini won’t run it. Instead, it will send you a `tool_call` message. This is a request for you to run your code and report back.

> **_The Golden Rule of Tools: Always Return the_**`id`
> 
> 
> _When Gemini sends a_`tool_call`_, it includes a unique_`id`_. Think of this as a tracking number for a package. When you send your_`send_tool_response`_, you_**_must_**_include this exact_`id`_. This is how Gemini matches your result to its original request in an asynchronous world. Forgetting it will leave Gemini waiting for a response that never comes._

#

# The complete loop: listening, executing, and responding to a tool call.

#

async for chunk in session.receive():

 if chunk.tool_call:

 # 1. Gemini is asking us to run a function.

 print(f"Received tool call: {chunk.tool_call}")

 function_call = chunk.tool_call.function_calls[0]

 

 # 2. Extract the details and the all-important 'id'.

 function_name = function_call.name

 function_args = function_call.args

 call_id = function_call.id # <-- The tracking number!

 

 # 3. Execute your actual code.

 if function_name == 'get_current_weather':

 # This is where you'd call your weather API.

 # result = your_weather_api(city=function_args['city'])

 result = {'temperature': '72F', 'condition': 'Sunny'}

 

 # 4. Respond with the result and the original 'id'.

 function_response = types.FunctionResponse(

 name=function_name,

 response=result,

 id=call_id,

 )

 await session.send_tool_response(function_responses=function_response)

Part 3: Pro-Tips for a Smoother Dev Experience
----------------------------------------------

A few final habits that will keep your code clean and save you from future headaches.

*   **Tip 1: Use the Right Parameter for the Job.** When using `send_realtime_input`, use the specific parameters like `audio` or `video` instead of the generic `media`. The specific parameters ensure your data is routed through the API's internal optimizations for that media type.
*   **Tip 2: The “One Argument” Rule.** A `send_realtime_input` call should do one thing. Send audio, or send text, or send a video frame. Don't try to bundle them. The API will raise a `ValueError` to stop you.

# DO THIS: 

await session.send_realtime_input(audio=audio_chunk) 

# DON'T DO THIS (it will fail):

await session.send_realtime_input(audio=audio_chunk, text="is this thing on?")
*   **Tip 3: Modernize Your Methods.** You might see an old `session.send()` method in older examples. **This is deprecated.** Using the modern, specific methods makes your code's intent crystal clear.

await session.send_client_content(...)

await session.send_realtime_input(...)

await session.send_tool_response(...)
Happy coding. Go build something amazing.

Sources: [https://github.com/googleapis/python-genai/tree/main/google/genai](https://github.com/googleapis/python-genai/tree/main/google/genai)

A message from our Founder
--------------------------

**Hey,**[**Sunil**](https://linkedin.com/in/sunilsandhu)**here.** I wanted to take a moment to thank you for reading until the end and for being a part of this community.

Did you know that our team run these publications as a volunteer effort to over 200k supporters? **We do not get paid by Medium**!

If you want to show some love, please take a moment to **follow me on**[**LinkedIn**](https://linkedin.com/in/sunilsandhu)**,**[**TikTok**](https://tiktok.com/@messyfounder)**and**[**Instagram**](https://instagram.com/sunilsandhu). And before you go, don’t forget to **clap** and **follow** the writer️!

[Gemini](https://medium.com/tag/gemini?source=post_page-----0fe7b83552b3---------------------------------------)

[Voice Assistant](https://medium.com/tag/voice-assistant?source=post_page-----0fe7b83552b3---------------------------------------)

[AI](https://medium.com/tag/ai?source=post_page-----0fe7b83552b3---------------------------------------)

[Artificial Intelligence](https://medium.com/tag/artificial-intelligence?source=post_page-----0fe7b83552b3---------------------------------------)

[Live](https://medium.com/tag/live?source=post_page-----0fe7b83552b3---------------------------------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fai-in-plain-english%2F0fe7b83552b3&operation=register&redirect=https%3A%2F%2Fai.plainenglish.io%2Fgemini-live-api-a-developers-practical-guide-0fe7b83552b3&user=Aswin+Chandrasekaran&userId=d2e40d76143d&source=---footer_actions--0fe7b83552b3---------------------clap_footer------------------)

3

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fai-in-plain-english%2F0fe7b83552b3&operation=register&redirect=https%3A%2F%2Fai.plainenglish.io%2Fgemini-live-api-a-developers-practical-guide-0fe7b83552b3&user=Aswin+Chandrasekaran&userId=d2e40d76143d&source=---footer_actions--0fe7b83552b3---------------------clap_footer------------------)

3

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F0fe7b83552b3&operation=register&redirect=https%3A%2F%2Fai.plainenglish.io%2Fgemini-live-api-a-developers-practical-guide-0fe7b83552b3&source=---footer_actions--0fe7b83552b3---------------------bookmark_footer------------------)

[![Image 7: Artificial Intelligence in Plain English](https://miro.medium.com/v2/resize:fill:96:96/1*9zAmnK08gUCmZX7q0McVKw@2x.png)](https://ai.plainenglish.io/?source=post_page---post_publication_info--0fe7b83552b3---------------------------------------)

[![Image 8: Artificial Intelligence in Plain English](https://miro.medium.com/v2/resize:fill:128:128/1*9zAmnK08gUCmZX7q0McVKw@2x.png)](https://ai.plainenglish.io/?source=post_page---post_publication_info--0fe7b83552b3---------------------------------------)

Follow

[Published in Artificial Intelligence in Plain English -----------------------------------------------------](https://ai.plainenglish.io/?source=post_page---post_publication_info--0fe7b83552b3---------------------------------------)

[32K followers](https://ai.plainenglish.io/followers?source=post_page---post_publication_info--0fe7b83552b3---------------------------------------)

·[Last published 1 hour ago](https://ai.plainenglish.io/you-can-always-tell-when-its-chatgpt-no-matter-how-hard-they-try-58847befc776?source=post_page---post_publication_info--0fe7b83552b3---------------------------------------)

New AI, ML and Data Science articles every day. Follow to join our 3.5M+ monthly readers.

Follow

[![Image 9: Aswin Chandrasekaran](https://miro.medium.com/v2/resize:fill:96:96/1*dfzjRyMxNX9ycwmzLY0GjA.png)](https://aswincsekar.medium.com/?source=post_page---post_author_info--0fe7b83552b3---------------------------------------)

[![Image 10: Aswin Chandrasekaran](https://miro.medium.com/v2/resize:fill:128:128/1*dfzjRyMxNX9ycwmzLY0GjA.png)](https://aswincsekar.medium.com/?source=post_page---post_author_info--0fe7b83552b3---------------------------------------)

Follow

[Written by Aswin Chandrasekaran -------------------------------](https://aswincsekar.medium.com/?source=post_page---post_author_info--0fe7b83552b3---------------------------------------)

[62 followers](https://aswincsekar.medium.com/followers?source=post_page---post_author_info--0fe7b83552b3---------------------------------------)

·[57 following](https://medium.com/@aswincsekar/following?source=post_page---post_author_info--0fe7b83552b3---------------------------------------)

Co-Founder and CTO at Bubba AI

Follow

No responses yet
----------------

[](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page---post_responses--0fe7b83552b3---------------------------------------)

![Image 11](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fai.plainenglish.io%2Fgemini-live-api-a-developers-practical-guide-0fe7b83552b3&source=---post_responses--0fe7b83552b3---------------------respond_sidebar------------------)

Cancel

Respond

More from Aswin Chandrasekaran and Artificial Intelligence in Plain English
---------------------------------------------------------------------------

![Image 12: How I Built a Recipe Parser That Actually Works Using Google’s LangExtract](https://miro.medium.com/v2/resize:fit:679/format:webp/1*ymXuU_7JseAPshtmaoPg-w.png)

[![Image 13: Artificial Intelligence in Plain English](https://miro.medium.com/v2/resize:fill:20:20/1*9zAmnK08gUCmZX7q0McVKw@2x.png)](https://ai.plainenglish.io/?source=post_page---author_recirc--0fe7b83552b3----0---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

In

[Artificial Intelligence in Plain English](https://ai.plainenglish.io/?source=post_page---author_recirc--0fe7b83552b3----0---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

by

[Aswin Chandrasekaran](https://aswincsekar.medium.com/?source=post_page---author_recirc--0fe7b83552b3----0---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

[How I Built a Recipe Parser That Actually Works Using Google’s LangExtract -------------------------------------------------------------------------- ### So here’s the thing — I love cooking, but I absolutely hate how recipes are formatted online. You know what I mean right? You’re looking…](https://ai.plainenglish.io/how-i-built-a-recipe-parser-that-actually-works-using-googles-langextract-6252ef808635?source=post_page---author_recirc--0fe7b83552b3----0---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

Aug 25

[](https://ai.plainenglish.io/how-i-built-a-recipe-parser-that-actually-works-using-googles-langextract-6252ef808635?source=post_page---author_recirc--0fe7b83552b3----0---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F6252ef808635&operation=register&redirect=https%3A%2F%2Fai.plainenglish.io%2Fhow-i-built-a-recipe-parser-that-actually-works-using-googles-langextract-6252ef808635&source=---author_recirc--0fe7b83552b3----0-----------------bookmark_preview----0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

![Image 14: 5 Essential MCP Servers That Give Claude & Cursor Real Superpowers (2025)](https://miro.medium.com/v2/resize:fit:679/format:webp/1*hHkPaadPKucy3RLtlkaP0A.png)

[![Image 15: Artificial Intelligence in Plain English](https://miro.medium.com/v2/resize:fill:20:20/1*9zAmnK08gUCmZX7q0McVKw@2x.png)](https://ai.plainenglish.io/?source=post_page---author_recirc--0fe7b83552b3----1---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

In

[Artificial Intelligence in Plain English](https://ai.plainenglish.io/?source=post_page---author_recirc--0fe7b83552b3----1---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

by

[Prithwish Nath](https://medium.com/@prithwish.nath?source=post_page---author_recirc--0fe7b83552b3----1---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

[5 Essential MCP Servers That Give Claude & Cursor Real Superpowers (2025) ------------------------------------------------------------------------- ### Transform Claude & Cursor into web scraping, browser-controlling automation engines. 5 essential Model Context Protocol servers with…](https://ai.plainenglish.io/5-essential-mcp-servers-that-give-claude-cursor-real-superpowers-2025-509a822dd4fd?source=post_page---author_recirc--0fe7b83552b3----1---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

Sep 27

[16](https://ai.plainenglish.io/5-essential-mcp-servers-that-give-claude-cursor-real-superpowers-2025-509a822dd4fd?source=post_page---author_recirc--0fe7b83552b3----1---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F509a822dd4fd&operation=register&redirect=https%3A%2F%2Fai.plainenglish.io%2F5-essential-mcp-servers-that-give-claude-cursor-real-superpowers-2025-509a822dd4fd&source=---author_recirc--0fe7b83552b3----1-----------------bookmark_preview----0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

![Image 16: RAG is Hard Until I Know these 12 Techniques → RAG Pipeline to 99% Accuracy](https://miro.medium.com/v2/resize:fit:679/format:webp/1*iSVnzJgRj9taXgmQ6AJIbQ.png)

[![Image 17: Artificial Intelligence in Plain English](https://miro.medium.com/v2/resize:fill:20:20/1*9zAmnK08gUCmZX7q0McVKw@2x.png)](https://ai.plainenglish.io/?source=post_page---author_recirc--0fe7b83552b3----2---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

In

[Artificial Intelligence in Plain English](https://ai.plainenglish.io/?source=post_page---author_recirc--0fe7b83552b3----2---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

by

[Simranjeet Singh](https://medium.com/@simranjeetsingh1497?source=post_page---author_recirc--0fe7b83552b3----2---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

[RAG is Hard Until I Know these 12 Techniques → RAG Pipeline to 99% Accuracy --------------------------------------------------------------------------- ### RAG is Hard Until I Know these 12 Techniques → RAG Pipeline to 99% Accuracy. Best Blog to Scale or increase RAG Pipelines Accuracy.](https://ai.plainenglish.io/rag-is-hard-until-i-know-these-12-techniques-rag-pipeline-to-99-accuracy-0100d9cb969b?source=post_page---author_recirc--0fe7b83552b3----2---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

Sep 27

[8](https://ai.plainenglish.io/rag-is-hard-until-i-know-these-12-techniques-rag-pipeline-to-99-accuracy-0100d9cb969b?source=post_page---author_recirc--0fe7b83552b3----2---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F0100d9cb969b&operation=register&redirect=https%3A%2F%2Fai.plainenglish.io%2Frag-is-hard-until-i-know-these-12-techniques-rag-pipeline-to-99-accuracy-0100d9cb969b&source=---author_recirc--0fe7b83552b3----2-----------------bookmark_preview----0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

![Image 18: Building a Multi-Provider Voice AI Agent: Architecture Deep Dive](https://miro.medium.com/v2/resize:fit:679/format:webp/1*05yP4SXmklTd5EFuFKfQJg.jpeg)

[![Image 19: Artificial Intelligence in Plain English](https://miro.medium.com/v2/resize:fill:20:20/1*9zAmnK08gUCmZX7q0McVKw@2x.png)](https://ai.plainenglish.io/?source=post_page---author_recirc--0fe7b83552b3----3---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

In

[Artificial Intelligence in Plain English](https://ai.plainenglish.io/?source=post_page---author_recirc--0fe7b83552b3----3---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

by

[Aswin Chandrasekaran](https://aswincsekar.medium.com/?source=post_page---author_recirc--0fe7b83552b3----3---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

[Building a Multi-Provider Voice AI Agent: Architecture Deep Dive ---------------------------------------------------------------- ### Modern voice AI agents need to handle real-time conversations while executing business functions seamlessly. This post explores the…](https://ai.plainenglish.io/building-a-multi-provider-voice-ai-agent-architecture-deep-dive-73fdb84c7d14?source=post_page---author_recirc--0fe7b83552b3----3---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

Jul 16

[](https://ai.plainenglish.io/building-a-multi-provider-voice-ai-agent-architecture-deep-dive-73fdb84c7d14?source=post_page---author_recirc--0fe7b83552b3----3---------------------0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F73fdb84c7d14&operation=register&redirect=https%3A%2F%2Fai.plainenglish.io%2Fbuilding-a-multi-provider-voice-ai-agent-architecture-deep-dive-73fdb84c7d14&source=---author_recirc--0fe7b83552b3----3-----------------bookmark_preview----0c6c05de_629c_4534_98f4_ac7815b0f72c--------------)

[See all from Aswin Chandrasekaran](https://aswincsekar.medium.com/?source=post_page---author_recirc--0fe7b83552b3---------------------------------------)

[See all from Artificial Intelligence in Plain English](https://ai.plainenglish.io/?source=post_page---author_recirc--0fe7b83552b3---------------------------------------)

Recommended from Medium
-----------------------

![Image 20: The Google ADK Playbook: Part 7 — The Capstone Project](https://miro.medium.com/v2/resize:fit:679/format:webp/1*BEEjY7BnxoCQF8Z1Qo_ivQ.png)

[![Image 21: AI Unboxed](https://miro.medium.com/v2/resize:fill:20:20/1*mvXuZ063OxNQiFpBSkr5Pw.png)](https://medium.com/ai-unboxed?source=post_page---read_next_recirc--0fe7b83552b3----0---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

In

[AI Unboxed](https://medium.com/ai-unboxed?source=post_page---read_next_recirc--0fe7b83552b3----0---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

by

[Gopi Donthireddy](https://medium.com/@gopi.don?source=post_page---read_next_recirc--0fe7b83552b3----0---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[The Google ADK Playbook: Part 7 — The Capstone Project ------------------------------------------------------ ### Welcome to the grand finale of the Google ADK Playbook! Over the last six articles, we’ve journeyed from a single agent to orchestrating…](https://medium.com/ai-unboxed/the-google-adk-playbook-part-7-the-capstone-project-8ee28769d688?source=post_page---read_next_recirc--0fe7b83552b3----0---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

Aug 7

[](https://medium.com/ai-unboxed/the-google-adk-playbook-part-7-the-capstone-project-8ee28769d688?source=post_page---read_next_recirc--0fe7b83552b3----0---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F8ee28769d688&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fai-unboxed%2Fthe-google-adk-playbook-part-7-the-capstone-project-8ee28769d688&source=---read_next_recirc--0fe7b83552b3----0-----------------bookmark_preview----e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

![Image 22: A Weekend Project: Build Your Own TTS Automation with Colab and n8n](https://miro.medium.com/v2/resize:fit:679/format:webp/1*PUXGoarH5cXgs4CGC6VtiQ.png)

[![Image 23: Mustafa BİÇER](https://miro.medium.com/v2/resize:fill:20:20/1*rqOg0krVRdtklApOIzM1tw.jpeg)](https://mstfbiccer.medium.com/?source=post_page---read_next_recirc--0fe7b83552b3----1---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[Mustafa BİÇER](https://mstfbiccer.medium.com/?source=post_page---read_next_recirc--0fe7b83552b3----1---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[A Weekend Project: Build Your Own TTS Automation with Colab and n8n ------------------------------------------------------------------- ### Here’s a quick write-up on a “weekend project” that takes Telegram messages and replies with Turkish MP3 voice notes — using only open…](https://mstfbiccer.medium.com/a-weekend-project-build-your-own-tts-automation-with-colab-and-n8n-3c1da86876f6?source=post_page---read_next_recirc--0fe7b83552b3----1---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

Jun 21

[](https://mstfbiccer.medium.com/a-weekend-project-build-your-own-tts-automation-with-colab-and-n8n-3c1da86876f6?source=post_page---read_next_recirc--0fe7b83552b3----1---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F3c1da86876f6&operation=register&redirect=https%3A%2F%2Fmstfbiccer.medium.com%2Fa-weekend-project-build-your-own-tts-automation-with-colab-and-n8n-3c1da86876f6&source=---read_next_recirc--0fe7b83552b3----1-----------------bookmark_preview----e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

![Image 24: The Claude Skills Cookbook: Anthropic’s New Context Engine Outperforms MCP??](https://miro.medium.com/v2/resize:fit:679/format:webp/1*DQH6ushHsV8W0Dv_fz1u9Q.png)

[![Image 25: Coding Nexus](https://miro.medium.com/v2/resize:fill:20:20/1*KCZtO6-wFqmTaMmbTMicbw.png)](https://medium.com/coding-nexus?source=post_page---read_next_recirc--0fe7b83552b3----0---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

In

[Coding Nexus](https://medium.com/coding-nexus?source=post_page---read_next_recirc--0fe7b83552b3----0---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

by

[Code Coup](https://medium.com/@CodeCoup?source=post_page---read_next_recirc--0fe7b83552b3----0---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[The Claude Skills Cookbook: Anthropic’s New Context Engine Outperforms MCP?? ---------------------------------------------------------------------------- ### Anthropic quietly released the Claude Skills Cookbook on GitHub. Initially, I assumed it was just another dull API document. But after…](https://medium.com/coding-nexus/the-claude-skills-cookbook-anthropics-new-context-engine-outperforms-mcp-92249dae37d3?source=post_page---read_next_recirc--0fe7b83552b3----0---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

5d ago

[](https://medium.com/coding-nexus/the-claude-skills-cookbook-anthropics-new-context-engine-outperforms-mcp-92249dae37d3?source=post_page---read_next_recirc--0fe7b83552b3----0---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F92249dae37d3&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fcoding-nexus%2Fthe-claude-skills-cookbook-anthropics-new-context-engine-outperforms-mcp-92249dae37d3&source=---read_next_recirc--0fe7b83552b3----0-----------------bookmark_preview----e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

![Image 26: Is user onboarding better now that we have AI?](https://miro.medium.com/v2/resize:fit:679/format:webp/1*41bmt3d6GawWWUVBHrJ50g.png)

[![Image 27: Roman from Onboarding.Pro](https://miro.medium.com/v2/resize:fill:20:20/1*EIsynkKzqL5QH3L-41Q_QA.png)](https://medium.com/@romanzadyrako?source=post_page---read_next_recirc--0fe7b83552b3----1---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[Roman from Onboarding.Pro](https://medium.com/@romanzadyrako?source=post_page---read_next_recirc--0fe7b83552b3----1---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[Is user onboarding better now that we have AI? ---------------------------------------------- ### Back in 2020, I wrote a post titled Why user onboarding still sucks in 2020, which was actually an update from a similar post from 2018. I…](https://medium.com/@romanzadyrako/is-user-onboarding-better-now-that-we-have-ai-796d2e9be72b?source=post_page---read_next_recirc--0fe7b83552b3----1---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

Sep 13

[](https://medium.com/@romanzadyrako/is-user-onboarding-better-now-that-we-have-ai-796d2e9be72b?source=post_page---read_next_recirc--0fe7b83552b3----1---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F796d2e9be72b&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40romanzadyrako%2Fis-user-onboarding-better-now-that-we-have-ai-796d2e9be72b&source=---read_next_recirc--0fe7b83552b3----1-----------------bookmark_preview----e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

![Image 28: How DeepSeek OCR Quietly Solved a Billion-Dollar Problem in AI Scaling](https://miro.medium.com/v2/resize:fit:679/format:webp/0*OgEctMcohHmdcCSv)

[![Image 29: Data And Beyond](https://miro.medium.com/v2/resize:fill:20:20/1*k72U7hHLb9EFXD5CLsbzFQ.png)](https://medium.com/data-and-beyond?source=post_page---read_next_recirc--0fe7b83552b3----2---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

In

[Data And Beyond](https://medium.com/data-and-beyond?source=post_page---read_next_recirc--0fe7b83552b3----2---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

by

[TONI RAMCHANDANI](https://toniramchandani.medium.com/?source=post_page---read_next_recirc--0fe7b83552b3----2---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[How DeepSeek OCR Quietly Solved a Billion-Dollar Problem in AI Scaling ---------------------------------------------------------------------- ### A technical marvel using SAM, CLIP, and a sparse MoE decoder — at open-source scale.](https://medium.com/data-and-beyond/how-deepseek-ocr-quietly-solved-a-billion-dollar-problem-in-ai-scaling-7b4502613af9?source=post_page---read_next_recirc--0fe7b83552b3----2---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

6d ago

[8](https://medium.com/data-and-beyond/how-deepseek-ocr-quietly-solved-a-billion-dollar-problem-in-ai-scaling-7b4502613af9?source=post_page---read_next_recirc--0fe7b83552b3----2---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F7b4502613af9&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fdata-and-beyond%2Fhow-deepseek-ocr-quietly-solved-a-billion-dollar-problem-in-ai-scaling-7b4502613af9&source=---read_next_recirc--0fe7b83552b3----2-----------------bookmark_preview----e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

![Image 30: Building a Text-to-SQL Chatbot with RAG, LangChain, FastAPI And Streamlit](https://miro.medium.com/v2/resize:fit:679/format:webp/1*s1ggrmDLA-VfEppGMDPKNA.png)

[![Image 31: Dharmendra Pratap Singh](https://miro.medium.com/v2/resize:fill:20:20/1*jG8dJP2cc8WgTXQSJY9f0g.png)](https://medium.com/@dharamai2024?source=post_page---read_next_recirc--0fe7b83552b3----3---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[Dharmendra Pratap Singh](https://medium.com/@dharamai2024?source=post_page---read_next_recirc--0fe7b83552b3----3---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[Building a Text-to-SQL Chatbot with RAG, LangChain, FastAPI And Streamlit ------------------------------------------------------------------------- ### In this project, I built an AI-powered chatbot that converts natural language questions into SQL queries and retrieves answers directly…](https://medium.com/@dharamai2024/building-a-text-to-sql-chatbot-with-rag-langchain-fastapi-and-streamlit-0a8f43488a08?source=post_page---read_next_recirc--0fe7b83552b3----3---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

6d ago

[5](https://medium.com/@dharamai2024/building-a-text-to-sql-chatbot-with-rag-langchain-fastapi-and-streamlit-0a8f43488a08?source=post_page---read_next_recirc--0fe7b83552b3----3---------------------e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F0a8f43488a08&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40dharamai2024%2Fbuilding-a-text-to-sql-chatbot-with-rag-langchain-fastapi-and-streamlit-0a8f43488a08&source=---read_next_recirc--0fe7b83552b3----3-----------------bookmark_preview----e6cf7bbf_136c_4e2d_a800_6d3001b72f8c--------------)

[See more recommendations](https://medium.com/?source=post_page---read_next_recirc--0fe7b83552b3---------------------------------------)

[Help](https://help.medium.com/hc/en-us?source=post_page-----0fe7b83552b3---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----0fe7b83552b3---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----0fe7b83552b3---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----0fe7b83552b3---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----0fe7b83552b3---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----0fe7b83552b3---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----0fe7b83552b3---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----0fe7b83552b3---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----0fe7b83552b3---------------------------------------)

