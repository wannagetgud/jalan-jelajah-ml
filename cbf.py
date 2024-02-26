import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("dataset/tourism_with_id.csv")

# processing dataframe
data_content_based_filtering = df.copy()
data_content_based_filtering['Tags'] = data_content_based_filtering['Category'] + ' ' + data_content_based_filtering['Description']
data_content_based_filtering = data_content_based_filtering[['Place_Id', 'Place_Name', 'Tags', 'Category', 'City','Description', 'Lat', 'Long','Rating','Price']]

tv = TfidfVectorizer(max_features=5000)
vectors = tv.fit_transform(data_content_based_filtering.Tags).toarray()
similarity = cosine_similarity(vectors)


def recommend_by_content_based_filtering(place_key, place_city, place_number):
    data_preferred = data_content_based_filtering[data_content_based_filtering['Category']==place_key].sample(1).values[0][1]
    place_key_index = data_content_based_filtering[data_content_based_filtering['Place_Name']==data_preferred].index[0]
    distancess = similarity[place_key_index]
    place_key_list = sorted(list(enumerate(distancess)), key=lambda x: x[1], reverse=True)[1:100]
    index = 0
    recommended_places = []
    for i in place_key_list:
        if data_content_based_filtering.iloc[i[0]].City == place_city:
          place = {
              "id": index,
              "place_name": data_content_based_filtering.iloc[i[0]]["Place_Name"],
              "description": data_content_based_filtering.iloc[i[0]]["Description"],
              "city": data_content_based_filtering.iloc[i[0]]["City"],
              "category": data_content_based_filtering.iloc[i[0]]["Category"],
              "lat": data_content_based_filtering.iloc[i[0]]["Lat"],
              "long": data_content_based_filtering.iloc[i[0]]["Long"],
              "price": data_content_based_filtering.iloc[i[0]]["Price"]
              }
          recommended_places.append(place)
          index+=1

        if len(recommended_places) >= int(place_number):
            break
    
    return recommended_places