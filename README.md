# Bike_challenge
This repository is meant to give an analysis of bike traffic in Montpellier in two different ways.
## Prediction 
On the one hand, using data from 
https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv, 
we had to predict the number of bicycles passing between 00:01 AM and 09:00 AM on Friday, April 2nd, by Albert 1er street in Montpellier. That part contains data sorting, and prediction method.
A pdf file is given in Prediction folder describing the method used for this prediction.


## Vizualisation
On the other hand, using data from https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-eco-compteurs, we had to visualize the bike traffic in Montpellier. 
From this site, I used 8 archive.json files, each containing information on one single Montpellier eco meter. The chosen data goes from 17th December 2020 to 29th March 2021.
The vizualisation I propose is a gif, composed of 105 images in png format, and created with imageio module. 

You can open the gif with the following url: 
