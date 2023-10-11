import numpy as np
import pandas as pd
import sys

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

kuku = pd.read_csv('main_database.csv', index_col=False)
num_rating_df = kuku.groupby('Hostel_Name').count()['Hostel_Rating_Simple'].reset_index()
num_rating_df.rename(columns={'Hostel_Rating_Simple':'num_ratings'},inplace=True)
avg_rating_df = kuku.groupby('Hostel_Name').mean()['Hostel_Rating_Simple'].reset_index()
avg_rating_df.rename(columns={'Hostel_Rating_Simple':'avg_rating'},inplace=True)
popular_df = kuku.merge(avg_rating_df,on='Hostel_Name')
yoyo=popular_df.merge(num_rating_df,on='Hostel_Name')
yoyo = yoyo[yoyo['num_ratings']>=2].sort_values('avg_rating',ascending=False)
yoyo['tags'] = yoyo['Hostel_Rating'] + yoyo['Hostel_Location'] + yoyo['Gender']
yoyo['tags'].apply(lambda x:[i.replace(" ","")for i in x])
yoyo['tags'] = yoyo['tags'].apply(lambda x:x.lower())
cv = CountVectorizer(max_features=500,stop_words='english')
vector = cv.fit_transform(yoyo['tags']).toarray()
cv.get_feature_names()
similarity = cosine_similarity(vector)
index = sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])

def recommend(Hostel_Name):
    hostel_index = yoyo[yoyo['Hostel_Name'] == Hostel_Name].index[0]
    # print(hostel_index)
    distances = similarity[hostel_index]
    # print(distances)
    hostel_list= sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    name = set()
    loc = list()
    avg = list()
    fee = list()
    for i in hostel_list:
        if yoyo.iloc[i[0]].Hostel_Name != Hostel_Name and yoyo.iloc[i[0]].Gender == yoyo.loc[yoyo[yoyo['Hostel_Name'] == Hostel_Name].index[1]].Gender:
            name.add(yoyo.iloc[i[0]].Hostel_Name)
    name = list(name)
    # print(name)
    for i in name:
        loc.append(yoyo.loc[yoyo[yoyo['Hostel_Name'] == i].index[1]].Hostel_Location)
        avg.append(yoyo.loc[yoyo[yoyo['Hostel_Name'] == i].index[1]].avg_rating)
        fee.append(yoyo.loc[yoyo[yoyo['Hostel_Name'] == i].index[1]].Yearly_Hostel_Fees)

    # print(name)
    # print(loc)
    # print(avg)
    # print(fee)
    # print(len(name))
    # print(len(loc))
    # print(len(avg))
    # print(len(fee))
    for j in range(0, len(name)):
        print(f'{name[j]},{loc[j]},{avg[j]:.2f},{fee[j]}')

# recommend('royal stay')
