import pandas as pd
import plotly.express as px
import json
counties = json.load(open("counties.json", encoding="ISO-8859-1")) #This is a map of other maps or something
score_map = {}
for county in counties['features']:
    county['id'] = county['properties']['GEO_ID']
    score_map[county['properties']['GEO_ID']] = county['properties']['NAME']
print(score_map) # Generates a map 
print(counties['features'][0]['properties'])
px.choropleth() # DATAFRAME of DATA, score map? 
#print(gj)
#df = pd.read_csv("beginner.csv") #df is a "Dataframe" that was read in by the read_csv.
#cleaned = df[["City","State","Zip Code"]] #This returns a new Dataframe f.
#updated = cleaned.dropna()
#print(updated)


