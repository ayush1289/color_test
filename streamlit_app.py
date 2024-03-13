import streamlit as st
import re
import uuid
from chat_llm.chat_handler import ChatHandler
from faceRecModule.faceFeature import FaceFeatures
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def file_upload(filepath:str):
    try:
        faceFeature = FaceFeatures(filepath)
        points = faceFeature.find_face_features()
        faceFeature.get_features_colour(points)
        facefeature = {
            "left_eye_colour": faceFeature.left_eye_colour,
            "right_eye_colour": faceFeature.right_eye_colour,
            "nose_colour": faceFeature.nose_colour,
            "jaw_colour": faceFeature.jaw_colour,
            "lips_colour": faceFeature.lips_colour
        }
        llm_reply = ChatHandler(api_key,[faceFeature.left_eye_colour, faceFeature.right_eye_colour, faceFeature.nose_colour, faceFeature.jaw_colour, faceFeature.lips_colour])
        good_palette = llm_reply.get_good_palette()
        bad_palette = llm_reply.get_bad_palette()
        blush_palette = llm_reply.get_blush()
        os.remove(f"uploads/image.jpg")    
        return {
            "face_feature": facefeature,
            "good_palette": good_palette,
            "bad_palette": bad_palette,
            "blush_palette": blush_palette,
        }
    except Exception as e:
        return {"error": "Face feature extraction failed."}

def hexcode_from_text(text):
    """
    Extracts hexcodes from a given text.

    Parameters:
        text (str): A string containing hexcodes.

    Returns:
        list: A list of hexcodes corresponding to the colors mentioned in the text.
    """
    hexcode_color_pairs = re.findall(r"#([a-fA-F\d]+)\s*\(([^)]+)\)", text)
    colors = {pair[0]: pair[1] for pair in hexcode_color_pairs}
    return hexcode_color_pairs

def hexcode_remover_from_text(text):
    """
    Removes hexcodes from a given text.

    Parameters:
        text (str): A string containing hexcodes.

    Returns:
        str: A string with hexcodes removed.
    """
    return re.sub(r"#([a-fA-F\d]+)\s*\(([^)]+)\)", "", text)




st.title("FaceHue Harmony")
st.subheader("A virtual assistant to help you find the perfect colors to match your skin tone.")
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.features = None
    st.session_state.response_code = 0
    st.session_state.prompt = [
        "Tell me which colours will look good on me on a sunny day?",
        "What colours will not complement my skin tone?",
        "What are the best blush colours for me?",
    ]


with st.sidebar.title("Upload an image"):
    with st.form(key="my_form"):
        uploaded_file = st.file_uploader("Choose an image...",type=["jpg","jpeg","png"])
        submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        with open("uploads/image.jpg","wb") as f:
            f.write(uploaded_file.read())
        st.session_state.features = file_upload("uploads/image.jpg")
        st.session_state.response_code = 200
        


if st.session_state.response_code == 200:
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            color_hexcode = hexcode_from_text(message["content"])
            response = hexcode_remover_from_text(message["content"])
            response = response[4:]
            with st.chat_message("assistant"):
                for i in range(5):
                    col1, col2 = st.columns([4,1])
                    with col1:
                        new_line_index = response.find("\n")
                        if new_line_index != -1:
                            st.write(f"{i+1}."+response[:new_line_index])
                            response = response[new_line_index+6:]
                        else:
                            st.write(f"{i+1}."+response)
                    with col2:
                        st.color_picker( color_hexcode[i][1],f"#{color_hexcode[i][0]}",key=f"{uuid.uuid4()}")



    prompt = st.selectbox("Ask a question", st.session_state.prompt,index = None, placeholder="Choose a prompt")
    if prompt:
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        if prompt == st.session_state.prompt[0]:
            response = st.session_state.features.get("good_palette")
        elif prompt == st.session_state.prompt[1]:
            response = st.session_state.features.get("bad_palette")
        elif prompt == st.session_state.prompt[2]:
            response = st.session_state.features.get("blush_palette")
        st.session_state.messages.append({"role":"assistant","content":response})
        color_hexcode = hexcode_from_text(response)
        response = hexcode_remover_from_text(response)
        response = response[4:]
        with st.chat_message("assistant"):
            for i in range(5):
                col1, col2 = st.columns([4,1])
                with col1:
                    new_line_index = response.find("\n")
                    if new_line_index != -1:
                        st.write(f"{i+1}."+response[:new_line_index])
                        response = response[new_line_index+6:]
                    else:
                        st.write(f"{i+1}."+response)
                with col2:
                    st.color_picker( color_hexcode[i][1],f"#{color_hexcode[i][0]}",key=f"{uuid.uuid4()}")
else:
    st.warning("Please upload an image to get started.")