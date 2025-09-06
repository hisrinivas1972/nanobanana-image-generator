import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO

# --- Page config ---
st.set_page_config(page_title="🎨🍌 Gemini 2.5 Dual Image Editor", layout="centered")
st.title("🎨🍌 Gemini 2.5 Flash Dual Image Editor")

# --- API Key input ---
api_key = st.text_input("🔑 Enter your Google API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash-image-preview")
    except Exception as e:
        st.error("❌ Invalid API key or model error.")
        st.stop()

    # --- Prompt input ---
    prompt = st.text_area("📝 Enter your image prompt (e.g. 'Merge these two images into a cinematic scene')", height=150)

    # --- Image uploader (exactly two images required) ---
    uploaded_images = st.file_uploader(
        "📤 Upload exactly two images to edit/combine",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    # --- Format selector ---
    img_format = st.selectbox("🖼️ Choose Download Format", ["PNG", "JPEG"])

    # --- Check image count ---
    if uploaded_images and len(uploaded_images) != 2:
        st.warning("⚠️ Please upload exactly 2 images.")

    # --- Generate button ---
    if st.button("🚀 Generate"):
        if not prompt.strip():
            st.warning("⚠️ Please enter a prompt.")
        elif len(uploaded_images) != 2:
            st.warning("⚠️ You must upload exactly 2 images.")
        else:
            with st.spinner("✨ Generating image..."):
                try:
                    contents = [prompt.strip()]

                    # Read and display the two images
                    for img_file in uploaded_images:
                        try:
                            image_bytes = img_file.read()
                            pil_img = Image.open(BytesIO(image_bytes))
                            st.image(pil_img, caption=f"📷 Uploaded: {img_file.name}", use_container_width=True)
                            contents.append(pil_img)
                        except Exception as e:
                            st.warning(f"⚠️ Could not read image {img_file.name}: {e}")
                            st.stop()

                    # Generate using Gemini
                    response = model.generate_content(contents, stream=False)

                    # Parse result
                    found_image = False
                    for part in response.parts:
                        if hasattr(part, "text") and part.text:
                            st.markdown("### 📝 Text Output")
                            st.write(part.text)

                        elif hasattr(part, "inline_data") and part.inline_data:
                            try:
                                img = Image.open(BytesIO(part.inline_data.data))
                                st.image(img, caption="🖼️ Generated Image", use_container_width=True)

                                # Prepare for download
                                img_bytes = BytesIO()
                                fmt = img_format.upper()
                                img.save(img_bytes, format=fmt)
                                img_bytes.seek(0)

                                st.download_button(
                                    label="⬇️ Download Image",
                                    data=img_bytes,
                                    file_name=f"gemini_image.{img_format.lower()}",
                                    mime=f"image/{img_format.lower()}",
                                )
                                found_image = True
                            except Exception as img_error:
                                st.warning(f"⚠️ Could not load generated image: {img_error}")

                    if not found_image:
                        st.error("❌ No image output found. Try another prompt or different images.")

                except Exception as e:
                    st.error(f"🚨 An error occurred: {e}")
else:
    st.info("🔑 Please enter your Google API key to start.")

# --- Prompt Tips ---
st.markdown("---")
st.markdown("""
### 💡 Prompt Writing Tips

- 🧠 Describe your intent clearly
- 🎨 Specify style, tone, or purpose
- 🖼️ Useful examples:
  - ""Give me long blond hair, slicked back. Put me like a cowboy riding a horse, hunting thieves through the forest with energy and intensity. Close up on my face."
(Use this prompt together with your own photo as input to generate a dramatic cowboy-themed image.)"
  - "Create a before-and-after restoration"
  - "Combine these into a futuristic landscape"
  - "Turn these faces into a single stylized portrait"
""")
