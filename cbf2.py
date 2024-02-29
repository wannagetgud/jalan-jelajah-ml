import pandas as pd

df = pd.read_csv("dataset/tourism_with_id.csv")
data = df
data['city_category'] = data[['City','Category']].agg(' '.join,axis=1)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
cv.fit(data['city_category'])

cv_matrix = cv.transform(data['city_category']) 
cv_matrix.todense()
pd.DataFrame(
    cv_matrix.todense(),
    columns=list(cv.vocabulary_.keys()),
    index = data.Place_Name
).sample(5)


from sklearn.metrics.pairwise import cosine_similarity
cosine_sim = cosine_similarity(cv_matrix)
cosine_sim_df = pd.DataFrame(cosine_sim,index=data['Place_Name'],columns=data['Place_Name'])

def recommend_by_content_based_filtering2(place_name,similarity_data=cosine_sim_df,items=data[['Place_Name','Category','Description','City', 'Lat', 'Long', 'Price', 'Rating']],k=10):
    index = similarity_data.loc[:,place_name].to_numpy().argpartition(range(-1,-k,-1))
    closest = similarity_data.columns[index[-1:-(k+2):-1]]
    closest = closest.drop(place_name,errors='ignore')
    result = pd.DataFrame(closest).merge(items).head(k)
    recommended_places = []
    for i in range(len(result)):
        place = {
            "id": i,
            "place_name": result.iloc[i]["Place_Name"],
            "description": result.iloc[i]["Description"],
            "city": result.iloc[i]["City"],
            "category": result.iloc[i]["Category"],
            "lat": result.iloc[i]["Lat"],
            "long": result.iloc[i]["Long"],
            "price": result.iloc[i]["Price"],
            "rating": result.iloc[i]["Rating"]
        }
        recommended_places.append(place)

    return recommended_places
    