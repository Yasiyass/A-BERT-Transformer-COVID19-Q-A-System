from fastapi import FastAPI
from pydantic import BaseModel

from haystack.document_stores import ElasticsearchDocumentStore
import os
from haystack.pipelines import ExtractiveQAPipeline
from haystack.nodes import FARMReader
from haystack.nodes import BM25Retriever



ELASTIC_SEARCH_HOST =  os.environ.get('es_ip', 'localhost')
ELASTIC_SEARCH_PORT =  os.environ.get('es_port', 9200)

app = FastAPI()

document_store = ElasticsearchDocumentStore(host=ELASTIC_SEARCH_HOST,
                                            port=ELASTIC_SEARCH_PORT,
                                            username="",
                                            password="",
                                            index="document")

retriever = BM25Retriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2-covid", use_gpu=False)
pipe = ExtractiveQAPipeline(reader, retriever)



class Queobj(BaseModel):
    question: str
    num_answers: int
    num_docs: int


@app.post('/query')
async def query(que_obj: Queobj):
    question = que_obj.question
    k_retriver = que_obj.num_docs
    k_reader = que_obj.num_answers
    prediction = pipe.run(query=question,
     params={"Retriever": {"top_k": k_retriver},
     "Reader": {"top_k": k_reader}})

    return {'answer': prediction}

#params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}
#uvicorn main:app  --port 8080 #http://127.0.0.1:8080/docs
