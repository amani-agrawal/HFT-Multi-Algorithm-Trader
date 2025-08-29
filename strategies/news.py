from config_globals import NEWS_THRESHOLD
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
from stream.finnub_news_streamer import get_general_news, get_specific_news
from engine.matcher import simulate_order
from collections import defaultdict

#to extract sentiment from news
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")   
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone") 
news_circulated = defaultdict(bool)

def run_news_trend():
    news= get_general_news("general")
    for i in news:
        result = get_sentiment(i)
        if result[0]!="HOLD":
            simulate_order(result[1], result[0])

def get_sentiment(news):
    if not news['related']:
        print("No company name specified.")
        return ('HOLD', None)
    if news_circulated[news['headline']]:
        print("News already processed.")
        return ('HOLD', None)
    news_circulated[news['headline']]= True
    text = news['headline'] + " " + news['summary']
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    probs = softmax(outputs.logits, dim=1)[0]
    labels = ['positive', 'neutral', 'negative']
    sentiment = {label: float(prob) for label, prob in zip(labels, probs)}
    if sentiment['positive'] > NEWS_THRESHOLD:
        return ('BUY', news['related'])
    elif sentiment['negative'] > NEWS_THRESHOLD:
        return ('SELL', news['related'])
    else:
        return ('HOLD', news['related'])
