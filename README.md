# Gemini 2.5 Nano Banana Image Editor

A Streamlit app using Google's Gemini 2.5 generative AI model to generate or enhance images based on prompts.

Prompts for Nano Banana (Gemini 2.5 Flash Image):

Create an image from text only:
"Create a photorealistic image of an orange cat with green eyes, sitting on a couch."

Edit an existing image with text prompt:
"Using the image of the cat, create a photorealistic, street-level view of the cat walking along a sidewalk in a New York City neighborhood, with the blurred legs of pedestrians and yellow cabs passing by in the background."
(Use this prompt together with your cat image as input.)

Restore and colorize an old photo:
"Restore and colorize this image from 1932"
(Use this prompt together with a black-and-white old photo.)

Edit multiple input images together:
"Make the girl wear this t-shirt. Leave the background unchanged."
(Use this prompt with two images: the girl photo and the t-shirt image.)

Conversational image edits:

"Change the cat to a bengal cat, leave everything else the same"

"The cat should wear a funny party hat"
(Use these prompts sequentially in a chat session with the cat image to iteratively edit.)

Custom image editing with your photo:
"Give me long blond hair, slicked back. Put me like a cowboy riding a horse, hunting thieves through the forest with energy and intensity. Close up on my face."
(Use this prompt together with your own photo as input to generate a dramatic cowboy-themed image.)

## How to run locally

1. Clone this repo:

```bash
git clone https://github.com/hisrinivas1972/nanobanana-image-editor.git
cd gemini-image-editor
