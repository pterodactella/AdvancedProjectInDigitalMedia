import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from keybert import KeyBERT
from api import get_keywords, setup_api


app = FastAPI()

class textInput(BaseModel):
    keyword: str

class maxTuples(BaseModel):
    listLists: list[list]


# set allowed access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Server": "running"}



@app.post("/parseKeywords")
def parseKeywords(text : textInput):
    try:
        doc = text.keyword
        # print('doc', doc)
        # kw_model = KeyBERT()
        # keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 3), stop_words='english',
        #                         use_mmr=True, diversity=0.7, top_n = int(0.3 *len(doc.split())), highlight = True)
        # keyword_list = sorted([i[0] for i in keywords], key=len, reverse=True)
        # print('doc:', keyword_list)
        keyword_list = get_keywords(doc)
        return keyword_list

    except Exception as e:
        print("Some error occured while performing post request for parsing keywords:", e)



@app.post("/getGraphs")
def getGraphs(text : textInput):
    return setup_api(text.keyword)

@app.post("/max5")
def max5(kwrList : maxTuples):
    kwr = kwrList.listLists
    print('kwr', kwr)
    max5 = []
    for i in range(5):
        val = max(kwr,key=lambda item:item[1])
        max5.append(val)
        kwr.remove(val)
    print('max5', max5)
    return max5






if __name__ == "__main__":
    uvicorn.run(app='main:app', host="localhost",
                    port=8080, reload=True, debug=True)



                    

# doc = ""
# def keybert(doc):
#     kw_model = KeyBERT()

#     keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 3), stop_words='english',
#                               use_mmr=True, diversity=0.7, top_n = int(0.3 *len(doc.split())), highlight = True)
#     keyword_list = sorted([i[0] for i in keywords], key=len, reverse=True)
#     return keyword_list

# keyword_list = keybert(doc)
# keyword_list