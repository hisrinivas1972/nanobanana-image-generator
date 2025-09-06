import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="🎨 Gemini 2.5 Nano Banana Image Editor", layout="centered")
st.title("🎨 Gemini 2.5 Flash (Nano Banana) Image Editor")

api_key = st.text_input("🔑 Enter your Google API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash-image-preview")

    prompt = st.text_area("📝 Enter your image prompt (e.g. 'Restore and colorize this image from 1932')", height=150)
    uploaded_image = st.file_uploader("📤 Upload an image (optional, for editing/enhancement)", type=["png", "jpg", "jpeg"])

    img_format = st.selectbox("🖼️ Choose Download Format", ["PNG", "JPEG"])

    if st.button("🚀 Generate"):
        if not prompt.strip():
            st.warning("⚠️ Please enter a prompt.")
        else:
            with st.spinner("✨ Generating image..."):
                try:
                    contents = [prompt.strip()]
                    if uploaded_image:
                        image_bytes = uploaded_image.read()
                        contents.append(Image.open(BytesIO(image_bytes)))

                    response = model.generate_content(contents, stream=False)

                    found_image = False
                    for part in response.parts:
                        if hasattr(part, "text") and part.text:
                            st.markdown("### 📝 Text Output")
                            st.write(part.text)
                        elif hasattr(part, "inline_data") and part.inline_data:
                            img = Image.open(BytesIO(part.inline_data.data))
                            st.image(img, caption="🖼️ Generated Image", use_container_width=True)

                            img_bytes = BytesIO()
                            fmt = img_format.upper()
                            if fmt == "JPG":
                                fmt = "JPEG"
                            img.save(img_bytes, format=fmt)
                            img_bytes.seek(0)

                            st.download_button(
                                label="⬇️ Download Image",
                                data=img_bytes,
                                file_name=f"gemini_image.{img_format.lower()}",
                                mime=f"image/{img_format.lower()}",
                            )
                            found_image = True

                    if not found_image:
                        st.error("❌ No image output found. Try another prompt or image.")

                except Exception as e:
                    st.error(f"🚨 An error occurred: {e}")
else:
    st.info("🔑 Please enter your Google API key to start.")

st.markdown("---")
st.markdown("""
### 💡 Prompt Writing Tips

- Describe what you want clearly
- Specify style, mood, lighting if you want
- Use examples like:
  - "Restore and colorize this image from 1932"
  - "A cyberpunk cityscape at night with neon lights"
""")
