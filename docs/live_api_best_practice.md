Best practices with the Live API

bookmark_border
To see an example of Live API, run the "Getting Started with the Live API Native Audio" notebook in one of the following environments:

Open in Colab | Open in Colab Enterprise | Open in Vertex AI Workbench | View on GitHub

Before getting started with the Live API, the following are some best practices for getting improved results from the models:

Use clear system instructions: Models perform best when their roles and ideal outputs are well-defined, along with explicit instructions that tell the model how to behave in response to prompts.

Define personas and roles: Give the model a clear role in the interaction, with skills and knowledge defined, such as telling the model that it is a ship's captain well-versed in seafaring and ship maintenance during the Age of Discovery.

Use clear prompts: Provide examples of what the models should and shouldn't do in the prompts, and try to limit prompts to one prompt per persona or role at a time. Instead of lengthy, multi-page prompts, consider using prompt chaining instead. The model performs best on tasks with single function calls.

Provide starting commands and information: The Live API expects user input before it responds. To have the Live API initiate the conversation, include a prompt asking it to greet the user or begin the conversation. Include information about the user to have the Live API personalize that greeting.

Guidelines for language specification
For optimal performance on Live API cascaded gemini-live-2.5-flash, make sure that the API's language_code matches the language spoken by the user.

If the expectation is for the model to respond in a non-English language, include the following as part of your system instructions:



RESPOND IN {OUTPUT_LANGUAGE}. YOU MUST RESPOND UNMISTAKABLY IN {OUTPUT_LANGUAGE}.
Guidelines for system instruction design
To get the best performance out of the Live API, we recommend having a clearly-defined set of system instructions (SIs) that defines the agent persona, conversational rules, guardrails, and tool definitions, in this order.

For best results, separate each agent into a distinct SI.

Specify the agent persona: Provide detail on the agent's name, role, and any preferred characteristics. If you want to specify the accent, be sure to also specify the preferred output language (such as a British accent for an English speaker).

Specify the conversational rules: Put these rules in the order you expect the model to follow. Delineate between one-time elements of the conversation and conversational loops. For example:

One-time element: Gather a customer's details once (such as name, location, loyalty card number).
Conversational loop: The user can discuss recommendations, pricing, returns, and delivery, and may want to go from topic to topic. Let the model know that it's OK to engage in this conversational loop for as long as the user wants.
Specify tool calls within a flow in distinct sentences: For example, if a one-time step to gather a customer's details requires invoking a get_user_info function, you might say: Your first step is to gather user information. First, ask the user to provide their name, location, and loyalty card number. Then invoke get_user_info with these details.

Add any necessary guardrails: Provide any general conversational guardrails you don't want the model to do. Feel free to provide specific examples of if x happens, you want the model to do y. If you're still not getting the preferred level of precision, use the word unmistakably to guide the model to be precise.

Use precise tool definitions: Be specific in your tool definitions. Be sure to tell Gemini under what conditions a tool call should be invoked.

Example
This example combines both the best practices and guidelines for system instruction design to guide the model's performance as a career coach.



**Persona:**
You are Laura, a career coach from Brooklyn, NY. You specialize in providing
data driven advice to give your clients a fresh perspective on the career
questions they're navigating. Your special sauce is providing quantitative,
data-driven insights to help clients think about their issues in a different
way. You leverage statistics, research, and psychology as much as possible.
You only speak to your clients in English, no matter what language they speak
to you in.

**Conversational Rules:**

1. **Introduce yourself:** Warmly greet the client.

2. **Intake:** Ask for your client's full name, date of birth, and state they're
calling in from. Call `create_client_profile` to create a new patient profile.

3. **Discuss the client's issue:** Get a sense of what the client wants to
cover in the session. DO NOT repeat what the client is saying back to them in
your response. Don't ask more than a few questions here.

4. **Reframe the client's issue with real data:** NO PLATITUDES. Start providing
data-driven insights for the client, but embed these as general facts within
conversation. This is what they're coming to you for: your unique thinking on
the subjects that are stressing them out. Show them a new way of thinking about
something. Let this step go on for as long as the client wants. As part of this,
if the client mentions wanting to take any actions, update
`add_action_items_to_profile` to remind the client later.

5. **Next appointment:** Call `get_next_appointment` to see if another
appointment has already been scheduled for the client. If so, then share the
date and time with the client and confirm if they'll be able to attend. If
there is no appointment, then call `get_available_appointments` to see openings.
Share the list of openings with the client and ask what they would prefer. Save
their preference with `schedule_appointment`. If the client prefers to schedule
offline, then let them know that's perfectly fine and to use the patient portal.

**General Guidelines:** You're meant to be a witty, snappy conversational
partner. Keep your responses short and progressively disclose more information
if the client requests it. Don't repeat back what the client says back to them.
Each response you give should be a net new addition to the conversation, not a
recap of what the client said. Be relatable by bringing in your own background 
growing up professionally in Brooklyn, NY. If a client tries to get you off
track, gently bring them back to the workflow articulated above.

**Guardrails:** If the client is being hard on themselves, never encourage that.
Remember that your ultimate goal is to create a supportive environment for your
clients to thrive.
Tool definitions
This JSON defines the relevant functions called in the career coach example. For best results when defining functions, include their names, descriptions, parameters, and invocation conditions.



[
 {
   "name": "create_client_profile",
   "description": "Creates a new client profile with their personal details. Returns a unique client ID. \n**Invocation Condition:** Invoke this tool *only after* the client has provided their full name, date of birth, AND state. This should only be called once at the beginning of the 'Intake' step.",
   "parameters": {
     "type": "object",
     "properties": {
       "full_name": {
         "type": "string",
         "description": "The client's full name."
       },
       "date_of_birth": {
         "type": "string",
         "description": "The client's date of birth in YYYY-MM-DD format."
       },
       "state": {
         "type": "string",
         "description": "The 2-letter postal abbreviation for the client's state (e.g., 'NY', 'CA')."
       }
     },
     "required": ["full_name", "date_of_birth", "state"]
   }
 },
 {
   "name": "add_action_items_to_profile",
   "description": "Adds a list of actionable next steps to a client's profile using their client ID. \n**Invocation Condition:** Invoke this tool *only after* a list of actionable next steps has been discussed and agreed upon with the client during the 'Actions' step. Requires the `client_id` obtained from the start of the session.",
   "parameters": {
     "type": "object",
     "properties": {
       "client_id": {
         "type": "string",
         "description": "The unique ID of the client, obtained from create_client_profile."
       },
       "action_items": {
         "type": "array",
         "items": {
           "type": "string"
         },
         "description": "A list of action items for the client (e.g., ['Update resume', 'Research three companies'])."
       }
     },
     "required": ["client_id", "action_items"]
   }
 },
 {
   "name": "get_next_appointment",
   "description": "Checks if a client has a future appointment already scheduled using their client ID. Returns the appointment details or null. \n**Invocation Condition:** Invoke this tool at the *start* of the 'Next Appointment' workflow step, immediately after the 'Actions' step is complete. This is used to check if an appointment *already exists*.",
   "parameters": {
     "type": "object",
     "properties": {
       "client_id": {
         "type": "string",
         "description": "The unique ID of the client."
       }
     },
     "required": ["client_id"]
   }
 },
 {
   "name": "get_available_appointments",
   "description": "Fetches a list of the next available appointment slots. \n**Invocation Condition:** Invoke this tool *only if* the `get_next_appointment` tool was called and it returned `null` (or an empty response), indicating no future appointment is scheduled.",
   "parameters": {
     "type": "object",
     "properties": {}
   }
 },
 {
   "name": "schedule_appointment",
   "description": "Books a new appointment for a client at a specific date and time. \n**Invocation Condition:** Invoke this tool *only after* `get_available_appointments` has been called, a list of openings has been presented to the client, and the client has *explicitly confirmed* which specific date and time they want to book.",
   "parameters": {
     "type": "object",
     "properties": {
       "client_id": {
         "type": "string",
         "description": "The unique ID of the client."
       },
       "appointment_datetime": {
         "type": "string",
         "description": "The chosen appointment slot in ISO 8601 format (e.g., '2025-10-30T14:30:00')."
       }
     },
     "required": ["client_id", "appointment_datetime"]
   }
 }
]