from config_globals import NEWS_THRESHOLD
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax

#to extract sentiment from news
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")   
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone") 

def get_sentiment(news):
    if not news['related']:
        print("No company name specified.")
        return ('HOLD', None)
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
