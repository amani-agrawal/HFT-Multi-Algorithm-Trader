import finnhub
from datetime import datetime, timedelta
from config_globals import FINNUB_API_KEY, NEWS_THRESHOLD
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from torch.nn.functional import softmax

#to get news
finnhub_client = finnhub.Client(api_key=FINNUB_API_KEY) 

#to extract sentiment from news
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")   
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone") 

#to extract company name from news header
ner = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)   

today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)

#The companyName should be its stock name like AAPL for APPLE
def get_specific_news(companyName):
    return finnhub_client.company_news(companyName, _from=yesterday.isoformat(), to=today.isoformat())

# Category can be: 'general', 'forex', 'crypto', or 'merger'
def get_general_news(category="general"):
    yesterday_start = datetime.combine(yesterday, datetime.min.time())
    yesterday_unix = int(yesterday_start.timestamp())
    news = finnhub_client.general_news(category)
    recent_news = [item for item in news if item['datetime'] >= yesterday_unix]
    for idx, i in enumerate(recent_news):
        if not i['related']:
            companies = [e['word'] for e in ner(i['headline']) if e['entity_group'] == 'ORG']
            for j in companies:
                if len(j)>=20:
                    continue
                results = finnhub_client.symbol_lookup(j)['result']
                if results and results[0]["symbol"]:
                    recent_news[idx]["related"] = results[0]["symbol"]
                    break
    return recent_news
