from flask import Flask, request
 
import openai
import os
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import PyPDF2




openai.api_key = ""
openai.api_base = "https://api.openai.com/v1/completions"

app = Flask(_name_)
def doc_text(file_path,from_page,to_page):
    print("file for read")
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        extracted_text = ""
        page_num = min(to_page,len(reader.pages))
        for i in range(from_page,page_num):
            extracted_text += reader.pages[i].extract_text()
            extracted_text += " "
        # global store_text
        # store_text = extracted_text
    return extracted_text

def medical_summery(doc,plaintiff,docType):

    text1 = doc_text(doc,0,8)
    
    
    print(text1)
    

    documentPrompt = "find key points from given input. Input :{text_input}"
    
    prompt_in = documentPrompt.format(text_input=text1[0:12000])
    # print(prompt_in)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_in,
        stop=None)
    print(response)
    result = response['choices']
    # result = bracket_finder(result)
    print("final result : ",result)
    
    return result

@app.route('/upload', methods=['POST'])
def querygpt():
        file = request.files['file']
        
        if file and file.filename.lower().endswith('.pdf'):
            file.save('uploaded_file.pdf')
            key_val_pair = medical_summery('uploaded_file.pdf',plaintiff,docType)
            return key_val_pair, 200
        else:
            return 'Invalid file format. Please upload a PDF file.'
        

if name == '_main_': 
   app.run(port=5000)
