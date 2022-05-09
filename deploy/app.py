import streamlit as st
import pandas as pd 
from matplotlib import pyplot as plt
from plotly import graph_objs as go
from sklearn.linear_model import LinearRegression
import numpy as np 
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

st.title("Nutrition Assistant")
st.text("Let us help you decide what to eat")
st.image("foood.jpg")

st.subheader("Whats your preference?")
vegetarian = st.checkbox("Vegetarian")
gluten_free = st.checkbox("Gluten Free")
kosher = st.checkbox("Kosher")

st.subheader("Select your desired daily percentage for Macros")
protein_val = st.slider("Select protein  value",0,100)
carb_val = st.slider("Select carbohydrate value",0,100)
fat_val = st.slider("Select fat value",0,100)

food = pd.read_csv("../input/food.csv")
ratings = pd.read_csv("../input/ratings.csv")
combined = pd.merge(ratings, food, on='Food_ID')

def tag(combined):
    if vegetarian == 1 and gluten_free == 1 and kosher == 1:
        ans = combined.loc[(combined['Vegetarian'] == vegetarian) & (combined['Gluten-Free'] == gluten_free) & (combined['Kosher'] == kosher) & (combined['Carbs DV%'] >= carb_val) & (combined['Proteins DV%'] >= protein_val) & (combined['Fats DV%'] >= fat_val),['Name','Carbs DV%', 'Fats DV%', 'Proteins DV%', 'Vegetarian', 'Gluten-Free', 'Kosher']]
    elif vegetarian == 1 and gluten_free == 1:
        ans = combined.loc[(combined['Vegetarian'] == vegetarian) & (combined['Gluten-Free'] == gluten_free) & (combined['Carbs DV%'] >= carb_val) & (combined['Proteins DV%'] >= protein_val) & (combined['Fats DV%'] >= fat_val),['Name','Carbs DV%', 'Fats DV%', 'Proteins DV%', 'Vegetarian', 'Gluten-Free', 'Kosher']]
    elif vegetarian == 1 and kosher == 1:
        ans = combined.loc[(combined['Vegetarian'] == vegetarian) & (combined['Kosher'] == kosher) & (combined['Carbs DV%'] >= carb_val) & (combined['Proteins DV%'] >= protein_val) & (combined['Fats DV%'] >= fat_val),['Name','Carbs DV%', 'Fats DV%', 'Proteins DV%', 'Vegetarian', 'Gluten-Free', 'Kosher']]
    elif gluten_free == 1 and kosher == 1:
        ans = combined.loc[(combined['Gluten-Free'] == gluten_free) & (combined['Kosher'] == kosher) & (combined['Carbs DV%'] >= carb_val) & (combined['Proteins DV%'] >= protein_val) & (combined['Fats DV%'] >= fat_val),['Name','Carbs DV%', 'Fats DV%', 'Proteins DV%', 'Vegetarian', 'Gluten-Free', 'Kosher']]
    elif vegetarian == 1:
        ans = combined.loc[(combined['Vegetarian'] == vegetarian) & (combined['Carbs DV%'] >= carb_val) & (combined['Proteins DV%'] >= protein_val) & (combined['Fats DV%'] >= fat_val),['Name','Carbs DV%', 'Fats DV%', 'Proteins DV%', 'Vegetarian', 'Gluten-Free', 'Kosher']]
    elif gluten_free == 1:
        ans = combined.loc[(combined['Gluten-Free'] == gluten_free) & (combined['Carbs DV%'] >= carb_val) & (combined['Proteins DV%'] >= protein_val) & (combined['Fats DV%'] >= fat_val),['Name','Carbs DV%', 'Fats DV%', 'Proteins DV%', 'Vegetarian', 'Gluten-Free', 'Kosher']]
    elif kosher == 1:
        ans = combined.loc[(combined['Kosher'] == kosher) & (combined['Carbs DV%'] >= carb_val) & (combined['Proteins DV%'] >= protein_val) & (combined['Fats DV%'] >= fat_val),['Name','Carbs DV%', 'Fats DV%', 'Proteins DV%', 'Vegetarian', 'Gluten-Free', 'Kosher']]
    else:
        ans = combined.loc[(combined['Carbs DV%'] >= carb_val) & (combined['Proteins DV%'] >= protein_val) & (combined['Fats DV%'] >= fat_val),['Name','Carbs DV%', 'Fats DV%', 'Proteins DV%', 'Vegetarian', 'Gluten-Free', 'Kosher']]
    return ans

ans = tag(combined)
names = ans['Name'].tolist()
x = np.array(names)
ans1 = np.unique(x)

if len(ans1) > 0:
    finallist = ""
    proceedVal = st.checkbox("Proceed ?")
    if proceedVal == True:
        finallist = st.selectbox("Select a dish you like",ans1)
else:
    st.write("No dishes found, please change the parameters")

##### IMPLEMENTING RECOMMENDER ######
dataset = ratings.pivot_table(index='Food_ID',columns='User_ID',values='Rating')
dataset.fillna(0,inplace=True)
csr_dataset = csr_matrix(dataset.values)
dataset.reset_index(inplace=True)

model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
model.fit(csr_dataset)

def food_recommendation(Food_Name):
    n = 10
    FoodList = food[food['Name'].str.contains(Food_Name)]  
    if len(FoodList):        
        Foodi= FoodList.iloc[0]['Food_ID']
        Foodi = dataset[dataset['Food_ID'] == Foodi].index[0]
        distances , indices = model.kneighbors(csr_dataset[Foodi],n_neighbors=n+1)    
        Food_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
        Recommendations = []
        for val in Food_indices:
            Foodi = dataset.iloc[val[0]]['Food_ID']
            i = food[food['Food_ID'] == Foodi].index
            Recommendations.append({'Name':food.iloc[i]['Name'].values[0],'Distance':val[1]})
        df = pd.DataFrame(Recommendations,index=range(1,n+1))
        return df['Name']
    else:
        return "No Similar Foods."
try:
    display = np.array(food_recommendation(finallist))
except NameError:
    st.write("")

combined_final = ans[['Name','Fats DV%', 'Carbs DV%','Proteins DV%']]
combined_final = combined_final.drop_duplicates()

try:
    if proceedVal == True:
        proceedVal1 = st.checkbox("View Recommendations ?")
        if proceedVal1 == True:
            st.write(combined_final.loc[combined_final['Name'].isin(display)])
except NameError:
    st.write("")