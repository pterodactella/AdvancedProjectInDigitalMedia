from keybert import KeyBERT
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import pandas as pd
import plotly.express as px
import spacy
import pytextrank
from collections import Counter
from string import punctuation
import numpy as np
from multi_rake import Rake
import plotly.io as io
from keyphrase_vectorizers import KeyphraseCountVectorizer
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# from flair.models import TextClassifier
# from flair.data import Sentence

io.templates.default = "plotly_white"
load_dotenv()
key =  os.getenv('key')

def keybert(doc):
    '''Pass the scring from the user's input'''
    kw_model = KeyBERT()


    # keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 2), stop_words="english",
    #                           use_maxsum=True, nr_candidates = int(0.08 *len(doc.split())), top_n = int(0.03 *len(doc.split())))

    keywords = kw_model.extract_keywords(doc, vectorizer = KeyphraseCountVectorizer(),
                                use_mmr=True, diversity = 0.8 , top_n = int(0.05 *len(doc.split())))
    keyword_list = sorted([i[0] for i in keywords], key=len, reverse=True)
    return keyword_list



def get_hotwords(text1):
    '''Pass the nlp after you define it in the end point'''
    nlp = spacy.load("en_core_web_trf")
    nlp.add_pipe("textrank")
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN', "VERB"] 
    doc = nlp(text1) 
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.text)
    return result



def get_keywords(doc):
    keyword_list = keybert(doc)
    output = set(get_hotwords(doc))
    most_common_list = Counter(output).most_common(int(0.03*len(doc.split())))
    for i in most_common_list:
        keyword_list.append(i[0])
    return keyword_list
    

def setup_api(doc):
    keyword_list = get_keywords(doc)
    my_data = {
    'country': 'dk',
    'currency': 'dkk',
    'dataSource': 'cli',
    'kw[]': keyword_list
    }
    my_headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+key
    }

    response = requests.post('https://api.keywordseverywhere.com/v1/get_keyword_data', data=my_data, headers=my_headers)
    if response.status_code == 200:
        print('success\n\n')
        keywords_data = response.json()["data"]
    else:
        print("An error occurred\n\n", response.content.decode('utf-8'))

    # Set up the dataframe
    df = pd.json_normalize(keywords_data, 'trend', "keyword")
    # print(df.head)
    df["month"] =  pd.to_datetime(df.month, format='%B').dt.month
    df["Date"] = df.year.astype(str) + "-"+ df.month.astype(str)
    df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m")

    pivoted = pd.pivot_table(index = "Date", columns = ["keyword"], values = "value", data = df)
    bar_plot = plot_barplot(pivoted)
    # remove hardly searched keywords
    for i in pivoted.columns:
        if pivoted[i].sum()<200:
            pivoted = pivoted.drop(columns = [i])

    #  the 2nd graph
    pivoted = pivoted.reset_index()
    graph_overallsv = plot_overallSV(pivoted)

    graph_top5 = plot_top5(pivoted)



   
    return [bar_plot, graph_overallsv, graph_top5]





def plot_barplot(pivoted_table):
    fig = px.bar(np.log10(pivoted_table.iloc[-1]) )

    fig.update_layout(
        # paper_bgcolor='rgba(0,0,0,0)',
        title="Count of search volume over last month",
        xaxis_title="Keyword",
        yaxis_title="Log 10 of Seach Volume",
        showlegend=False,
        title_x=0.5,
        hovermode="x")

    
    # fig.show()
    # print(io.to_html(fig, full_html=False))

    return io.to_html(fig, full_html=False)

def plot_overallSV(pivoted_table):
    fig = px.line(pivoted_table , y= pivoted_table.sum(axis = 1), x = "Date", title='Overall Text Search Volume', markers= True)
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    fig.update_yaxes(tickformat='', title = "Search Volume")
    fig.update_layout(
        # paper_bgcolor='rgba(0,0,0,0)'
        title_x=0.5
        )
    return io.to_html(fig, full_html=False)


# Adauga in html 
def plot_top5(pivoted_table):
    fig = make_subplots(
        rows=1, cols=2, x_title='Keyword',
                        y_title='Search Volume',
        subplot_titles=("5 Most Searched", "5 Least Searched"))

    fig.add_trace(go.Bar(x = list(dict(pivoted_table.sum().nlargest(5))), y = list(dict(pivoted_table.sum().nlargest(5)).values())),row=1, col=1)

    fig.add_trace(go.Bar(x = list(dict(pivoted_table.sum().nsmallest(5))), y = list(dict(pivoted_table.sum().nsmallest(5)).values())),
                row=1, col=2)

    # fig.show()

    return io.to_html(fig, full_html=False)
    


# # Sentiment analysis
# def generate_sentiment_analysis(text : str):
#     sentence = Sentence(text)
#     classifier = TextClassifier.load('en-sentiment')
#     classifier.predict(sentence)
#     print(f'The sentiment of your text is classified as {sentence.labels[0].value} with the score of {sentence.labels[0].score*100:.2f}%')
