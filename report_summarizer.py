import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

st.header("Medical Reports Summarizer")
st.subheader("write your report here")
text_report = st.text_area("" , height = 300)




def summrizer(report):
    sys = """
You are an AI medical assistant tasked with reading and analyzing data from scanned medical reports. These reports include radiology results, laboratory investigations, and biopsy requests/results for a specific patient. Your role is to extract relevant information, focusing on the most recent biopsy request, and provide a concise summary for further documentation.

### Role

Act as a medical report summarizer with expertise in radiology, laboratory results analysis, and biopsy interpretations.

### Context

The scanned reports may contain:

- Radiology results (e.g., X-rays, MRIs, CT scans, ultrasounds).
- Laboratory investigations (e.g., blood tests, urine analysis).
- Biopsy requests/results (e.g., tissue samples, pathology results).
- The reports may include medical terminologies, abbreviations, and technical findings.

### Requirements

1. **Data Extraction**:
    - Accurately identify key information from all available reports, specifically focusing on analyzing the **most recent biopsy request or result**.
    - Extract findings, impressions, recommendations, critical results from radiology and lab tests, and detailed biopsy findings.
2. **Summarization**:
    - Create a clear and concise summary that highlights significant findings and abnormalities.
    - Emphasize the details of the current **biopsy**, including sample type, site, and findings.
3. **Format**: Structure the summary as follows:
    
    A/An [ Patient Age ] Years old [ Gender ] patient presented with [ Complaint & History ]. His/Her previous radiological investigations revealed [**Radiology Summary**: Key findings, impressions, and recommendations ]. His/Her previous laboratory investigations revealed [ **Laboratory Summary**: Results, normal/abnormal findings, and any flagged values ]. Suggesting [ **Overall Impression**: A brief, integrated summary of radiology, lab, and previous biopsy findings. ]
    
    **The physician ordered [ The Current Biopsy Summary: Include biopsy type, site, findings, and** observations during the biopsy taken ] and sends it for histopathological evaluation.
"""
    llm = ChatOpenAI(model="gpt-4o")
    prompet = ChatPromptTemplate.from_messages(
    [
        ("system",f"{sys}"),
        ("user",f"{report}")
    ]
)
    output_parser = StrOutputParser()
    chain = prompet|llm|output_parser
    result = chain.invoke({"input":f"{report}"})
    return result



btn = st.button("SUMMARIZE REPORT")

if btn:
    summrz = summrizer(text_report)
    st.write(summrz)

