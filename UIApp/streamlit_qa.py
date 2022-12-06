import streamlit as st
import requests, json
#from annotated_text import annotated_text

st.set_page_config(
    page_title="Covid Q&A",
    page_icon=":shark:",
    layout="wide",
    initial_sidebar_state="expanded"
    )

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)
def icon(icon_name):
    st.markdown(f'<i class="fa fa-external-link" aria-hidden="true"></i>', unsafe_allow_html=True)

remote_css("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css")

st.markdown('<h1 style="text-align: center">Artificial Intelligence Covid Q&A</h1>', unsafe_allow_html=True)

st.sidebar.header("Options")
top_k_reader = st.sidebar.slider("Max. number of answers", min_value=1, max_value=10, value=3, step=1)
top_k_retriever = st.sidebar.slider("Max. number of documents from retriever", min_value=1, max_value=10, value=3, step=1)


st.markdown('<h3>Question</h3>', unsafe_allow_html=True)
question = st.text_input("Put your query", value="What are the symptoms of COVID?")
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
        token2 =[]
        tokens.append(each['answer'])
        token2.append(each['context'])

        col1, col2 = st.columns([7,1])
        col1.markdown(f'<span style="font-size:22; font-weight:bold;">Title: {title}</span><a href={url} target="_blank"><i class="fa fa-external-link" aria-hidden="true"></i></a>', unsafe_allow_html=True)
        col2.markdown(f'<input type="button" value="Confidence: {int(each["score"]*100)}%">', unsafe_allow_html=True)
        st.text("")
        col1, col2 = st.columns([2,4])
        col1.markdown(f'<span style="font-size: 16; font-weight:bold;">Publish time: {each["meta"]["publish_time"]}\
                    <br>Authors: {each["meta"]["authors"]}</span>', unsafe_allow_html=True)
        #annotated_text(*tokens)
        #st.write(tokens)
        st.write(f'<span style="font-size:16; font-weight:bold; color:#c00;">Answer : {tokens[0]}</span>', unsafe_allow_html=True)
        st.write(f'<span style="font-size:14;">Context : {token2[0]}</span>', unsafe_allow_html=True)




#sudo chmod 777 streamlit_qa.py
########./streamlit_qa.py
#before runing the following line main.py was executed. (uvicorn main:app  --port 8080)
#streamlit run streamlit_qa.py --server.port 80
