from config import GOOGLE_API_KEY
import os
import streamlit as st
from pathlib import Path
import google.generativeai as genai
from PIL import Image

#configure genai with api key
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096
}

# apply safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hosptial. Your expertise is crucial in identifying any anomalies diseases, or health issues that may be present in the images.

Your Responsibilities:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or sign of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions. 

Important notes:

1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of images: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions"

Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.
"""

model = genai.GenerativeModel(model_name='gemini-1.5-pro',
                            generation_config=generation_config,
                            safety_settings=safety_settings)

st.set_page_config(page_title="VitalImage Analytics", page_icon=':anatomical_heart:')

# Custom CSS for styling the title
st.markdown(
    """
    <style>
    .file-uploader {
        font-size: 20px;
        font-weight: 600;
        color: #4B0082;  /* Indigo color */
        margin-bottom: 10px;
    }
    .caption {
        font-size: 14px;
        color: #6A5ACD;  /* Light Indigo color */
        text-align: center;
    }
    .title {
        font-size: 48px;
        font-weight: 700;
        color: #4B0082; /* Indigo color */
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    .subtitle {
        font-size: 18px;
        color: #4B0082;
        text-align: center;
        margin-bottom: 20px;
    }
    .center {
        display: flex;
        justify-content: center;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Title with custom CSS
st.markdown("<div class='title'>Vital Image Analytics</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-Powered Diagnostics for Disease Detection</div>", unsafe_allow_html=True)

# Displaying an icon with the upload prompt
st.markdown("<div class='file-uploader'>📤 Upload an Image for AI Diagnosis</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader('', type=["png", "jpg", "jpeg"])

# Display uploaded image preview
if uploaded_file is not None:
    st.markdown('<div class="center">', unsafe_allow_html=True)
    st.image(Image.open(uploaded_file), caption="Uploaded Medical Image", use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)

submit_button = st.button("Generate the Analysis")

if submit_button:
    #process the uploaded image
    image_data = uploaded_file.getvalue()
    #making our image ready
    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        }
    ]
    #making our prompt ready
    prompt_parts = [
        "Describe what the ",
        image_parts[0],
        system_prompt
    ]
    # Generate a response based on prompt and image
    response = model.generate_content(prompt_parts)
    # print(response.text)
    st.write(response.text)