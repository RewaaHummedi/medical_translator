import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import pandas as pd
import os

# Load the Faseeh model
model_c = 'nadsoft/Faseeh-v0.1-beta'
tokenizer = AutoTokenizer.from_pretrained(model_c)
model = AutoModelForSeq2SeqLM.from_pretrained(model_c)

# Create a translation pipeline
translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang='ajp_Arab', tgt_lang='eng_Latn', max_length=400)

# Streamlit interface
st.title("Medical Symptoms Translator")

# Input fields
name = st.text_input("Name")
medical_file_number = st.text_input("Medical File Number")
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
age = st.number_input("Age", min_value=0)
symptoms = st.text_area("Symptoms (in Arabic)")

# Translate button
if st.button("Translate"):
    if symptoms:
        # Translate the symptoms
        output = translator(symptoms)
        translated_text = output[0]['translation_text']
        
        # Display the translated text
        st.write("### Translated Symptoms (in English)")
        st.write(translated_text)
        
        # Save to Excel
        data = {
            "Name": [name],
            "Medical File Number": [medical_file_number],
            "Gender": [gender],
            "Age": [age],
            "Symptoms (Arabic)": [symptoms],
            "Translated Symptoms (English)": [translated_text]
        }
        
        df = pd.DataFrame(data)
        
        # Define the file name and check if it exists
        file_name = "medical_translations.xlsx"
        if os.path.exists(file_name):
            # If the file exists, load the existing data
            existing_df = pd.read_excel(file_name)
            df = pd.concat([existing_df, df], ignore_index=True)
        
        # Save the DataFrame to Excel
        df.to_excel(file_name, index=False)
        
        st.success("Data has been saved to medical_translations.xlsx")
    else:
        st.error("Please enter the symptoms to translate.")
