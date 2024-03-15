import streamlit as st
import re
import uuid
from chat_llm.chat_handler import hexcode_from_text, hexcode_remover_from_text, ChatHandler
from faceRecModule.faceFeature import FaceFeatures
from dotenv import load_dotenv
import os
load_dotenv("setup/.env")
api_key = os.getenv("OPENAI_API_KEY")
  
def get_hexcodes(filepath:str):
    try:
        faceFeature = FaceFeatures(filepath)
        points = faceFeature.find_face_features()
        faceFeature.get_features_colour(points)
        hexcode_face = {
            "left_eye_colour": faceFeature.left_eye_colour,
            "right_eye_colour": faceFeature.right_eye_colour,
            "nose_colour": faceFeature.nose_colour,
            "jaw_colour": faceFeature.jaw_colour,
            "lips_colour": faceFeature.lips_colour
        }
        os.remove(f"uploads/image.jpg")
        return hexcode_face
    
    except Exception as e:
        return {"error": "Face feature extraction failed."}
col1,col2,col3 = st.columns([1,1,1]) 
with col2:   
    st.image("logoNew.png",width=200)
st.title("Personal Color Assistant")
st.subheader("A virtual assistant to help you find the perfect colors to match your skin tone.")
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.features = None
    st.session_state.good_palette = None
    st.session_state.bad_palette = None
    st.session_state.blush_palette = None
    st.session_state.response_code = 0
    st.session_state.prompt = [
        "Tell me which colours will look good on me on a sunny day?",
        "What colours will not complement my skin tone?",
        "What are the best blush colours for me?",    
    ]
    st.session_state.file_container = True


if st.session_state.file_container:
    with st.subheader("Upload an image"):
        with st.form(key="my_form"):
            uploaded_file = st.file_uploader("Choose an image...",type=["jpg","jpeg","png"])
            submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            with open("uploads/image.jpg","wb") as f:
                f.write(uploaded_file.read())
                with st.spinner("Processing..."):
                    st.session_state.features = get_hexcodes("uploads/image.jpg")
                    print(st.session_state.features)
                    st.session_state.response_code = 200
                    st.session_state.file_container = False
                st.success("Image uploaded successfully.")
        


if st.session_state.response_code == 200 and not st.session_state.file_container:

    llm_reply = ChatHandler(
        api_key=api_key,
        hexcodes=(
            st.session_state.features["left_eye_colour"],
            st.session_state.features["right_eye_colour"],
            st.session_state.features["nose_colour"],
            st.session_state.features["jaw_colour"],
            st.session_state.features["lips_colour"],
        ),
    )

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



    col1, col2 = st.columns([5,1])
    with col2:
        if st.button("Upload another image"):
            st.session_state.file_container = True
            st.session_state.messages = [] 
    with col1:
        prompt = st.selectbox("Ask a question", st.session_state.prompt,index = None, placeholder="Choose a prompt")
    if prompt:
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.spinner("lets see what the AI has to say..."):

            response = ""
            if prompt == st.session_state.prompt[0]:
                if not st.session_state.good_palette:
                    st.session_state.good_palette = llm_reply.get_good_palette()
                response = st.session_state.good_palette
            elif prompt == st.session_state.prompt[1]:
                if not st.session_state.bad_palette:
                    st.session_state.bad_palette = llm_reply.get_bad_palette()
                response = st.session_state.bad_palette
            elif prompt == st.session_state.prompt[2]:
                if not st.session_state.blush_palette:
                    st.session_state.blush_palette = llm_reply.get_blush()
                response = st.session_state.blush_palette
        
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