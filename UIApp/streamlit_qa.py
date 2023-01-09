import streamlit as st
import requests, json
from PIL import Image
import re
import string
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from collections import Counter

from transformers import pipeline
import pandas as pd




st.set_page_config(
    page_title="Covid Q&A",
    page_icon="shark",
    layout="wide",
    initial_sidebar_state="auto"
    )

def remove_special_char_and_punctuations(text):
    pattern = r'[^a-zA-Z0-9\'\s]'
    my_stop_words = ["the","abstract","and","patients", "patient","has","have","been","about","covid19", "use","using","due","based","one","among", "method","used", "result","conclusion","including","methods","results","will","conclusions","via","sarscov2"]
    txt = re.sub(pattern, '', text)
    for i in range(len(my_stop_words)):
        txt = txt.lower().replace(my_stop_words[i], ' ')
    txt = ''.join([c for c in txt if c not in string.punctuation])
    return txt

def concat_all_sentences(sents):
    all_tokens = ''
    for text in sents:
        tx = str(text).lower()#.strip()
        #tx = " ".join(tx.split())
        all_tokens += tx + ''
    return all_tokens

def plot_wordcloud(docx):
    #mywordcloud = WordCloud().generate(docx)
    fig = plt.figure(figsize=(20,10))
    plt.imshow(docx, interpolation = "bilinear")
    plt.axis('off')
    st.pyplot(fig)

def plot_word_freq(docx,num=10):
    word_freq = Counter (docx.split())
    most_common_tokens = word_freq.most_common(num)
    x,y = zip(*most_common_tokens)
    fig = plt.figure(figsize =(20,15))
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.show()
    st.pyplot(fig)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)
def icon(icon_name):
    st.markdown(f'<i class="fa fa-external-link" aria-hidden="true"></i>', unsafe_allow_html=True)

remote_css("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css")

st.markdown('<h1 style="text-align: center">Covid Question-Answering AI System 🦠</h1>', unsafe_allow_html=True)


st.sidebar.header("Options")
top_k_reader = st.sidebar.slider("Max. number of answers", min_value=1, max_value=10, value=3, step=1)
top_k_retriever = st.sidebar.slider("Max. number of documents from retriever", min_value=1, max_value=10, value=3, step=1)


st.markdown('<h3>Question</h3>', unsafe_allow_html=True)
question = st.text_area("Put your query", value="e.g. What are the symptoms of COVID?",key='query')
button = st.button('Get Answer')
st.text("")
st.text("")

if button:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = {
         'question': question, 'num_answers': top_k_reader, 'num_docs': top_k_retriever
    }
    response = requests.post('http://127.0.0.1:8080/query',
    headers=headers,
     data=json.dumps(data))
    result = response.json()
    for each in result['answer']['answers']:
        title = each['meta']['title']
        url = each['meta']['url'].split(';')[0]
        tokens = []
        #token2 =[]
        token3 =[]
        tokens.append(each['answer'])
        #token2.append(each['context'])
        token3.append(each["meta"]['abstract'])

        col1, col2 = st.columns([14,1])
        col1.info('')
        col1.markdown(f'<span style="font-size:22; font-weight:bold;">Title: {title}</span><a href={url} target="_blank"><i class="fa fa-external-link" aria-hidden="true"></i></a>', unsafe_allow_html=True)
        col2.markdown(f'<input type="button" value="Score: {int(each["score"]*100)}%">', unsafe_allow_html=True)
        #st.text("")
        col1, col2 = st.columns([14,1])
        col1.markdown(f'<span style="font-size: 16; font-weight:bold;">Publish time: {each["meta"]["publish_time"]}\
                    <br>Authors: {each["meta"]["authors"]}</span>', unsafe_allow_html=True)

        st.write(f'<span style="font-size:16; font-weight:bold; color:#c00;">Answer : {tokens[0]}</span>', unsafe_allow_html=True)
        #st.write(f'<span style="font-size:14;">Context : {token2[0]}</span>', unsafe_allow_html=True)
        with st.expander("Abstract"):
            st.write(f'<span style="font-size:14;">{token3[0]}</span>', unsafe_allow_html=True)

st.image("https://images.unsplash.com/photo-1584118624012-df056829fbd0?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=3432&q=80")

# Text analysis app
st.markdown('<h1 style="text-align: center">Text Analysis App </h1>', unsafe_allow_html=True)

raw_text = st.text_area("Enter Text Here", key = 'analyzer', value = 'please insert a text here to analyze')
if st.button('Submit'):
    if len(raw_text) >2:
        st.success(raw_text)
    elif len(raw_text) == 1:
        st.warning('Insufficient Text, minimum word required is 2 words')
    else:
        st.write('Enter Text')

#layout
col1,col2 = st.columns(2)
clean_text = remove_special_char_and_punctuations(raw_text)
processed_text = concat_all_sentences(clean_text)

with col1:
    with st.expander('Original Text'):
        st.write(raw_text)
    with st.expander('Plot Word Frequency'):
        plot_word_freq(processed_text)

with col2:
    with st.expander('Processed Text'):
        st.write(processed_text)
    with st.expander('plot Wordcloud'):
        st.success('Wordcloud')
        text_wordcloud = WordCloud(width = 500, height = 500, random_state = 10).generate(processed_text)
        my_cloud = plot_wordcloud(text_wordcloud)
        #st.write(my_cloud)


# A Transformer Summarization NLP App
st.markdown('<h1 style="text-align: center">Bart Transformer Summarizer</h1>', unsafe_allow_html=True)

raw_text = st.text_area('A summarization pipeline with a HuggingFace Transformer library🤗',key = 'summarizer')

# Initialize the HuggingFace summarization pipeline
summarizer = pipeline("summarization")

if st.button("Summarize"):
    if len(raw_text) >2:
        st.success(raw_text)
    elif len(raw_text) == 1:
        st.warning('Insufficient Text, minimum is 2')
    else:
        st.write('Enter Text')

col1,col2 = st.columns(2)
with col1:
    with st.expander("Original Text"):
        st.write(raw_text)
    # Layout
with col2:
    with st.expander("BART Summarization Model"):
        my_summary = summarizer(raw_text.split("\n", 1))
        st.markdown(my_summary[0]['summary_text'])




#sudo chmod 777 streamlit_qa.py
########./streamlit_qa.py
#before runing the following line main.py was executed. (uvicorn main:app  --port 8080)
#streamlit run streamlit_qa.py --server.port 80
