Using Proactive Audio

bookmark_border
Preview

This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

To see an example of Live API, run the "Getting Started with the Live API Native Audio" notebook in one of the following environments:

Open in Colab | Open in Colab Enterprise | Open in Vertex AI Workbench | View on GitHub

Proactive Audio helps Gemini have more authentic conversations by letting you control when it responds and in what contexts with fewer interruptions. For example, you can ask Gemini to only respond when prompted or when certain specific topics are discussed. To see Proactive Audio in action, check out a demonstration of the features.

This guide covers how Proactive Audio works, how to integrate it into your application, and what tokens you are billed for. This guide doesn't cover the price list for Proactive Audio. For full pricing details, see Vertex AI pricing. This guide assumes you are working either in Vertex AI Studio or are using the Google Gen AI SDK for Python.

Supported models
You can use Proactive Audio with the following models:

Model version	Availability level
gemini-live-2.5-flash-preview-native-audio-09-2025	Public preview
gemini-live-2.5-flash-preview-native-audio	Public preview; Discontinuation date: October 17, 2025
Use Proactive Audio
Proactive Audio is not enabled by default in gemini-live-2.5-flash-preview-native-audio-09-2025.

To use Proactive Audio, configure the proactivity field in the setup message and set proactive_audio to true:

Python


config = LiveConnectConfig(
    response_modalities=["AUDIO"],
    proactivity=ProactivityConfig(proactive_audio=True),
)
  
Have a conversation using Proactive Audio
You can initiate a conversation with Gemini using Proactive Audio and define when Gemini can respond, limiting its responses to relevant topics.

For example, the following is a sample of what a conversation with Gemini about cooking might look like:



Prompt: "You are an AI assistant in Italian cooking; only chime in when the topic is about Italian cooking."

Speaker A: "I really love cooking!" (No response from Gemini.)

Speaker B: "Oh yes, me too! My favorite is French cuisine." (No response from
Gemini.)

Speaker A: "I really like Italian food; do you know how to make a pizza?"

(Italian cooking topic will trigger response from Gemini.)
Live API: "I'd be happy to help! Here's a recipe for a pizza."
Features
Note: For Proactive Audio, function calling is available as an experimental feature.
When using Proactive Audio, Gemini will respond with minimal latency after the user is done speaking. This reduces interruptions and helps Gemini not lose context if an interruption happens.

Proactive Audio also helps Gemini avoid interruptions from background noise or external chatter, and prevents Gemini from responding if external chatter is introduced during a conversation.

If the user needs to interrupt during a response from Gemini, Proactive Audio makes it easier for Gemini to appropriately back-channel (meaning appropriate interruptions are handled), rather than if a user uses filler words such as umm or uhh.

Gemini can co-listen to an audio file that's not the speaker's voice and subsequently answer questions about that audio file later in the conversation.