import pandas as pd
import plotly.express as px
import json

clusters = [["Maine", "New Hampshire", "Vermont"],
            ["Alaska", "Hawaii"],
            ["Delaware", "Maryland", "New Jersey", "Pennsylvania", "Virginia", "West Virginia"],
            ["Alabama", "Florida", "Georgia", "North Carolina", "South Carolina", "Tennessee"],
            ["Illinois", "Indiana", "Kentucky", "Michigan", "Ohio", "South Dakota"],
            ["Arizona", "California", "Colorado", "Idaho", "Montana", "Nevada", "New Mexico", "Oregon", "Utah", "Washington", "Wyoming"],
            ["Connecticut", "Massachusetts", "Rhode Island"],
            ["New York"],
            ["Arkansas", "Kansas", "Louisiana", "Mississippi", "Missouri", "Oklahoma", "Texas"],
            ["Iowa", "Minnesota", "Nebraska", "North Dakota", "South Dakota"]]


#Import State geo-json data:
counties = json.load(open("states.json", encoding="ISO-8859-1")) #This is a map of other maps or something
df = pd.read_csv("state_scores.csv")

#Initialize Score Map
score_map = {}
for i, row in df.iterrows():
    score_map[row[0]] = row[1]

#Use State ID of the Dataframe as the State
for county in counties['features']:
    county['id'] = county['properties']['NAME']

#Create alternative Dataframe for cluster model
correctional = []
for cluster in clusters:
    total = 0
    for state in cluster:
        total += score_map[state]
    avg = total/len(cluster)
    correctional.append(avg)
matrix = []
for i, row in df.iterrows():
    for ind in range(len(clusters)):
        if row[0] in clusters[ind]:
            #row[1] = correctional[ind]
            matrix.append([row[0], correctional[ind]])
df2 = pd.DataFrame(matrix, columns = ["State Name", "Score"])

#Create Chloropleth
fig = px.choropleth(df, geojson=counties, color="Score", locations="State Name", projection="mercator") 
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()




