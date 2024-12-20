import requests
import streamlit as st
import json
import base64

def get_lang_code(lang_string):
    if lang_string == "Hindi":
        code = "hi-IN"
    elif lang_string == "Bengali":
        code = "bn-IN"
    elif lang_string == "Kannada":
        code = "kn-IN"
    elif lang_string == "Malayalam":
        code = "ml-IN"
    elif lang_string == "Marathi":
        code = "mr-IN"
    elif lang_string == "Odiya":
        code = "od-IN"
    elif lang_string == "Punjabi":
        code = "pa-IN"
    elif lang_string == "Tamil":
        code = "ta-IN"
    elif lang_string == "Telugu":
        code = "te-IN"
    elif lang_string == "Gujarati":
        code = "gu-IN"

    return code

def get_translation(input_text, lang):

    url = "https://api.sarvam.ai/translate"

    payload = {
        "input": input_text,
        "source_language_code": "en-IN",
        "target_language_code": get_lang_code(lang),
        "speaker_gender": "Male",
        "mode": "formal",
        "model": "mayura:v1",
        "enable_preprocessing": True
    }
    headers = {
        "api-subscription-key": st.secrets["SARVAM_API_KEY"],
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)

    return response.text

def get_speech(text, lang):

    url = "https://api.sarvam.ai/text-to-speech"

    payload = {
        "inputs": [text],
        "target_language_code": get_lang_code(lang),
        "speaker": "meera",
        "pitch": 0,
        "pace": 1.2,
        "loudness": 1.5,
        "speech_sample_rate": 8000,
        "enable_preprocessing": True,
        "model": "bulbul:v1"
    }

    headers = {
        "api-subscription-key": st.secrets["SARVAM_API_KEY"],
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.text

def main():

    st.title("Multilingual Translater")

    text = st.text_area("Enter your message")
    lang = st.selectbox("Select Language to translate to: ", ["Hindi","Bengali","Kannada","Malayalam","Marathi","Odiya","Punjabi","Tamil","Telegu","Gujarati"])

    if st.button("Submit"):
        if text:
            res = get_translation(text, lang)
            res_json = json.loads(res)
            new_text = res_json["translated_text"]
            st.header("Translation")
            st.success(new_text)

            speech_res = get_speech(new_text, lang)
            speech = json.loads(speech_res)
            if "audios" in speech and speech["audios"]:
                audio_base64 = speech["audios"][0]
                audio_bytes = base64.b64decode(audio_base64)
                
                st.audio(audio_bytes, format="audio/wav")

if __name__ == "__main__":
    main()
