# ElectionForecast
N votes received, V votes to go, what's the chance of each candidate winning?

I approached this problem three different ways

electionprediction.py - Pure simulation - can handle as many number of candidates as your heart desires, runs fairly quickly
electionprediction2.py - Half-simulation, half-(pointless?)computation - can handle 2 or three candidates, runs farily quickly
electionprediction3.py - Pure Bayesian Computation - can handle 2 or 3 candidates, runs a loop for each possible distribution of remaining votes which is V+k-1 C k-1 if k is the number of candidates, so it's pretty fast for 2 candidates, unreasonably slow for 3 candidates with V>300
