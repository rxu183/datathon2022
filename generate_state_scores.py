import pandas as pd
df = pd.read_csv("sc-est2019-agesex-civ.csv")
df.drop(df[df['NAME'] == "United States"].index, inplace = True)
df = df.reset_index(drop=True)
df.drop(df[df['SEX'] == 0].index, inplace = True)
df = df.reset_index(drop=True)
df.drop(df[df['SEX'] == 1].index, inplace = True)
df = df.reset_index(drop=True)
df.to_csv("updated-sc-est2019-agesex-civ.csv", index=False)

from collections import defaultdict
import math
df = pd.read_csv("updated-sc-est2019-agesex-civ.csv")

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
   
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))  

state_pop = defaultdict(int)
state_avg_age = defaultdict(int)
state_annual_pop = defaultdict(lambda: defaultdict(int))

#collection of avg age, population, and annual population for each state
for (i, row) in df.iterrows():
    if row[6] == 999:
        state_pop[row[4]] = row[17]
        for (i, pop) in enumerate(row[8:]):
            state_annual_pop[row[4]][f"{2010+i}"] = pop
    else:
        state_avg_age[row[4]] += row[6]*row[17]
       
for state in state_avg_age:
    state_avg_age[state] /= state_pop[state]
   
#calculation of the avg pop growth for each state

state_pop_growth = defaultdict(float)
for state in state_annual_pop:
    growth = 0
    for i in range(9):
        growth += (state_annual_pop[state][str((2010+i)+1)] - state_annual_pop[state][str(2010+i)])/state_annual_pop[state][str(2010+i)]
    state_pop_growth[state] = growth

#initializing the number of certified facilities in each state

df = pd.read_csv("mammogram per state.csv")

state_cert_faci = defaultdict(int)

for (i, row) in df.iterrows():
    state_cert_faci[abbrev_to_us_state[row[0]]] = row[1]

#initializing the median income in each state
df = pd.read_csv("income by state.csv")
df.drop(index=[0,1], inplace=True)

state_income = defaultdict(int)

for (i, row) in df.iterrows():
    state_income[row[0]] = float(row[1].replace(",", ""))

#normalizing the data

def normalize(data_set, data):
    max_val = max(data_set.values())
    min_val = min(data_set.values())
    norm = (data-min_val)/(max_val-min_val)
    return norm

norm_income = defaultdict(float)
norm_avg_age = defaultdict(float)
norm_pop = defaultdict(float)
norm_pop_growth = defaultdict(float)
norm_cert_faci = defaultdict(float)

for state in state_pop:
    norm_income[state] = normalize(state_income, state_income[state])
    norm_avg_age[state] = normalize(state_avg_age, state_avg_age[state])
    norm_pop[state] = normalize(state_pop, state_pop[state])
    norm_pop_growth[state] = normalize(state_pop_growth, state_pop_growth[state])
    norm_cert_faci[state] = normalize(state_cert_faci, state_cert_faci[state])

#calculating the score for each state

def score(pop_g, pop, inc, num_cert, avg_age):
    return math.log((float(pop_g)+float(pop)+(float(avg_age)))/((float(inc)) + (float(num_cert))))
        #float(pop)*    
state_score = defaultdict(float)

for state in norm_pop:
    state_score[state] = score(norm_pop_growth[state], norm_pop[state], norm_income[state], norm_cert_faci[state], norm_avg_age[state])

#converting scores to csv file
sorted_state_scores = sorted(state_score.items(), key=lambda a: a[0])
df = pd.DataFrame(sorted_state_scores, columns=['State Name', 'Score'])
df.to_csv("state scores.csv", index=False)