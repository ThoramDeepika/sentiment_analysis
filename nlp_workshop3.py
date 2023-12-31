import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('/content/threads_reviews.csv')

df

df.head()

df.tail()

df.shape

df.columns

df.isnull().sum()

df.duplicated().sum()

df.drop_duplicates

df.describe()

df.info()

df.nunique()

df['source'].unique()

df['source'].value_counts()

plt.figure(figsize=(5,5))
counts = df['source'].value_counts()
plt.pie(counts,labels = counts.index,autopct='%1.1f%%', colors = sns.color_palette('hls'))
plt.title("Source of reviews")
plt.show()

fig = go.Figure(data=[go.Bar(x=df['source'].value_counts().index, y=df['source'].value_counts())])
fig.update_layout(title='Source of Reviews',xaxis_title="Source",yaxis_title="Count")
fig.show()

counts = df['source'].value_counts()
fig = go.Figure(data=[go.Pie(labels=counts.index, values=counts)])
fig.update_layout(title='Source of Reviews')
fig.show()

df['rating'].unique()

df['rating'].value_counts()

plt.figure(figsize=(15,6))
sns.countplot(x = df['rating'], data = df, palette = 'hls')
plt.show()

plt.figure(figsize=(10, 10))
counts = df['rating'].value_counts()
plt.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=sns.color_palette('hls'))
plt.title('Rating')
plt.show()

fig = go.Figure(data=[go.Bar(x=df['rating'].value_counts().index, y=df['rating'].value_counts())])
fig.update_layout(title='Rating',xaxis_title="Rating",yaxis_title="Count")
fig.show()

counts = df['rating'].value_counts()
fig = go.Figure(data=[go.Pie(labels=counts.index, values=counts)])
fig.update_layout(title='Rating')
fig.show()

df['review_date'] = pd.to_datetime(df['review_date'])

df1 = df.copy()

df1.set_index('review_date', inplace=True)

start_date = df1.index.min()
end_date = df1.index.max()

print("Start Date of Reviews:", start_date)
print("End Date of Reviews:", end_date)

week_delta = pd.Timedelta(days=7)
current_date = start_date

while current_date <= end_date:
    start_week = current_date
    end_week = current_date + week_delta
    current_week_data = df1[(df1.index >= start_week) & (df1.index < end_week)]
    print(current_week_data)
    weekly_counts = current_week_data.resample('D').size()
    print(weekly_counts)
    fig = px.bar(weekly_counts, x=weekly_counts.index, y=weekly_counts.values,
                 labels={'x': 'Date', 'y': 'Number of Reviews'},
                 title=f'Reviews for Week {start_week.strftime("%Y-%m-%d")} to {end_week.strftime("%Y-%m-%d")}')
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()
    current_date += week_delta

daily_counts = df1.resample('D').size()

fig = go.Figure()
fig.add_trace(go.Bar(x=daily_counts.index, y=daily_counts.values,
                     marker_color='skyblue'))
fig.update_layout(title='Number of Reviews Day-wise',
                  xaxis_title='Date',
                  yaxis_title='Number of Reviews',
                  xaxis_tickangle=-45)
fig.show()

fig = go.Figure()
for source_name, source_data in df1.groupby('source'):
    fig.add_trace(go.Scatter(x=source_data.resample('D').size().index, y=source_data.resample('D').size().values,
                            mode='lines', name=source_name))
fig.update_layout(title='Number of Reviews Day-wise',
                  xaxis_title='Date',
                  yaxis_title='Number of Reviews',
                  xaxis_tickangle=-45)
fig.show()

fig = go.Figure()
for source_name, source_data in df1.groupby('source'):
    fig.add_trace(go.Scatter(x=source_data.resample('D').size().index, y=source_data.resample('D').size().values,
                            mode='lines+markers', name=source_name))
fig.update_layout(title='Number of Reviews Day-wise',
                  xaxis_title='Date',
                  yaxis_title='Number of Reviews',
                  xaxis_tickangle=-45)
fig.show()

fig = go.Figure()
for source_name, source_data in df1.groupby('source'):
    fig.add_trace(go.Scatter(x=source_data.resample('D').size().index, y=source_data.resample('D').size().values,
                            mode='markers', name=source_name))
fig.update_layout(title='Number of Reviews Day-wise',
                  xaxis_title='Date',
                  yaxis_title='Number of Reviews',
                  xaxis_tickangle=-45)
fig.show()

fig = go.Figure()
for rating_val, rating_data in df1.groupby('rating'):
    fig.add_trace(go.Scatter(x=rating_data.resample('D').size().index, y=rating_data.resample('D').size().values,
                             mode='lines+markers', name=f'Rating {rating_val}'))
fig.update_layout(title='Number of Reviews Day-wise by Rating',
                  xaxis_title='Date',
                  yaxis_title='Number of Reviews',
                  xaxis_tickangle=-45)
fig.show()

fig = go.Figure()
for rating_val, rating_data in df1.groupby('rating'):
    fig.add_trace(go.Scatter(x=rating_data.resample('D').size().index, y=rating_data.resample('D').size().values,
                             mode='markers', name=f'Rating {rating_val}'))
fig.update_layout(title='Number of Reviews Day-wise by Rating',
                  xaxis_title='Date',
                  yaxis_title='Number of Reviews',
                  xaxis_tickangle=-45)
fig.show()

df['rating']=df['rating'].map({1:-1,2:-1,3:0,4:1,5:1})

df

df_new = df[['review_description', 'rating']]

df_new



df_new['rating'].unique()

df_new['rating'].value_counts()

fig = go.Figure(data=[go.Bar(x=df_new['rating'].value_counts().index, y=df_new['rating'].value_counts())])
fig.update_layout(title='Rating',xaxis_title="Rating",yaxis_title="Count")
fig.show()

counts = df_new['rating'].value_counts()
fig = go.Figure(data=[go.Pie(labels=counts.index, values=counts)])
fig.update_layout(title='Rating')
fig.show()

"""data preprocessing

"""

def clean_text(text):
    text = text.lower()
    return text.strip()

df_new.review_description = df_new.review_description.apply(lambda x: clean_text(x))

df_new.review_description

import string
string.punctuation

def remove_punctuation(text):
    punctuationfree="".join([i for i in text if i not in string.punctuation])
    return punctuationfree

df_new.review_description = df_new.review_description.apply(lambda x:remove_punctuation(x))

df_new.review_description

df_new.review_description = df_new.review_description.apply(lambda x: x.lower())

df_new.review_description

import re

def tokenization(text):
    tokens = re.split(' ',text)
    return tokens

df_new.review_description = df_new.review_description.apply(lambda x: tokenization(x))

df_new.review_description

import nltk
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
stopwords[0:10]
['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're"]

def remove_stopwords(text):
    output= " ".join(i for i in text if i not in stopwords)
    return output

df_new.review_description = df_new.review_description.apply(lambda x:remove_stopwords(x))

df_new.review_description

def clean_text(text):
    text = re.sub('\[.*\]','', text).strip()
    text = re.sub('\S*\d\S*\s*','', text).strip()
    return text.strip()

df_new.review_description = df_new.review_description.apply(lambda x: clean_text(x))

df_new.review_description

import spacy
nlp = spacy.load('en_core_web_sm')

stopwords = nlp.Defaults.stop_words
def lemmatizer(text):
    doc = nlp(text)
    sent = [token.lemma_ for token in doc if not token.text in set(stopwords)]
    return ' '.join(sent)

df_new.review_description =  df_new.review_description.apply(lambda x: lemmatizer(x))

def remove_urls(vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT)

df_new.review_description = df_new.review_description.apply(lambda x: remove_urls(x))

def remove_urls(vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT)

def remove_digits(text):
    clean_text = re.sub(r"\b[0-9]+\b\s*", "", text)
    return(text)

df_new.review_description = df_new.review_description.apply(lambda x: remove_digits(x))

def remove_digits1(sample_text):
    clean_text = " ".join([w for w in sample_text.split() if not w.isdigit()])
    return(clean_text)

df_new.review_description = df_new.review_description.apply(lambda x: remove_digits1(x))

def remove_emojis(data):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               "]+", flags=re.UNICODE)
    return re.sub(emoji_pattern, '', data)

df_new.review_description = df_new.review_description.apply(lambda x: remove_emojis(x))

df_new

import wordcloud

from wordcloud import WordCloud
data = df_new.review_description
plt.figure(figsize = (20,20))
wc = WordCloud(max_words = 1000 , width = 1600 , height = 800,
               collocations=False).generate(" ".join(data))
plt.imshow(wc)
plt.axis('off')
plt.show()

from wordcloud import WordCloud
data = df_new[df_new['rating'] == 1]['review_description']
plt.figure(figsize = (20,20))
wc = WordCloud(max_words = 1000 , width = 1600 , height = 800,
               collocations=False).generate(" ".join(data))
plt.imshow(wc)
plt.axis('off')
plt.show()

data = df_new[df_new['rating'] == 0]['review_description']
plt.figure(figsize = (20,20))
wc = WordCloud(max_words = 1000 , width = 1600 , height = 800,
               collocations=False).generate(" ".join(data))
plt.imshow(wc)
plt.axis('off')
plt.show()

data = df_new[df_new['rating'] == -1]['review_description']
plt.figure(figsize = (20,20))
wc = WordCloud(max_words = 1000 , width = 1600 , height = 800,
               collocations=False).generate(" ".join(data))
plt.imshow(wc)
plt.axis('off')
plt.show()

from sklearn.feature_extraction.text import TfidfVectorizer

tf1=TfidfVectorizer()
data_vec=tf1.fit_transform(df_new['review_description'])

data_vec

import pickle
model_filename = 'tfidf_vectorizer.pkl'
with open('mode_filename', 'wb') as model_file:
  pickle.dump(tf1, model_file)



y=df_new['rating'].values

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test=train_test_split(data_vec,y,test_size=0.2,stratify = y, random_state=42)

from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_balanced, y_balanced = smote.fit_resample(X_train, y_train)

X_balanced, y_balanced



from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

sv = SVC()

model_sv = sv.fit(X_balanced, y_balanced)

y_pred_sv = model_sv.predict(X_test)

accuracy = accuracy_score(y_test,y_pred_sv)
print(f'Accuracy: {accuracy:2f}')

model_filename = 'svm_model.pkl'
with open(model_filename, 'wb') as model_file:
  pickle.dump(model_sv, model_file)

dt = DecisionTreeClassifier()

model_dt = dt.fit(X_balanced, y_balanced)

y_pred_dt = model_dt.predict(X_test)

sv = SVC()
dt = DecisionTreeClassifier()
rf = RandomForestClassifier()
ad = AdaBoostClassifier()

models = [sv, dt, rf, ad]

accuracies = []

for model in models:
    print('Results for the model:', model.__class__.__name__)
    model.fit(X_balanced, y_balanced)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print('Accuracy:', accuracy)

    cm = confusion_matrix(y_test, y_pred)
    print('Confusion Matrix:\n', cm)

    report = classification_report(y_test, y_pred)
    print('Classification Report:\n', report)

    print('\n')

    accuracies.append(accuracy)

print('List of Accuracies:', accuracies)

model_names = ['SVC', 'DecisionTree', 'RandomForest', 'AdaBoost']
fig = go.Figure(data=go.Bar(x=model_names, y=accuracies))
fig.update_layout(title='Model Accuracies',
                  xaxis_title='Model',
                  yaxis_title='Accuracy',
                  yaxis_tickformat='.2%',
                  yaxis_range=[0, 1],
                  xaxis_tickangle=0)
fig.show()

import pickle
model_filename = 'svm_model.pkl'
with open(model_filename,'wb') as model_file:
    pickle.dump(sv,model_file)











