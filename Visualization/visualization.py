#%%
import pandas as pd
import folium
import imageio
import os


#%%
#Only once, charge data from urls
#url = 'https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H19070220_archive.json'
#download(url, path='./MMM_EcoCompt_X2H19070220_archive.json')
#url2 = 'https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20042632_archive.json'
#download(url2, path='./MMM_EcoCompt_X2H20042632_archive.json')
#url3 = 'https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20042633_archive.json'
#download(url3, path='./MMM_EcoCompt_X2H20042633_archive.json')
#url4 = 'https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20042635_archive.json'
#download(url4, path='./MMM_EcoCompt_X2H20042635_archive.json')
#url5 = 'https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20063161_archive.json'
#download(url5, path='./MMM_EcoCompt_X2H20063161_archive.json')
#url6 = 'https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20063162_archive.json'
#download(url6, path='./MMM_EcoCompt_X2H20063162_archive.json')
#url7 = 'https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_XTH19101158_archive.json'
#download(url7, path='./MMM_EcoCompt_XTH19101158_archive.json')
#url8 = 'https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20063163_archive.json'
#download(url8, path='./MMM_EcoCompt_X2H20063163_archive.json')


# %%
#Creation of a dictionary containing the 8 json-files we need, one by Eco meter
dict_ = {} #we start with an empty dictionary which will be filled with json_files
dict_[0] = pd.read_json('C:/Users/quenf/Bike_challenge2/Visualization/JSON_Files/MMM_EcoCompt_X2H19070220_archive.json', lines = True)
dict_[1] = pd.read_json('C:/Users/quenf/Bike_challenge2/Visualization/JSON_Files/MMM_EcoCompt_X2H20042632_archive.json', lines = True)
dict_[2] = pd.read_json('C:/Users/quenf/Bike_challenge2/Visualization/JSON_Files/MMM_EcoCompt_X2H20042633_archive.json', lines = True)
dict_[3] = pd.read_json('C:/Users/quenf/Bike_challenge2/Visualization/JSON_Files/MMM_EcoCompt_X2H20042635_archive.json', lines = True)
dict_[4] = pd.read_json('C:/Users/quenf/Bike_challenge2/Visualization/JSON_Files/MMM_EcoCompt_X2H20063161_archive.json', lines = True)
dict_[5] = pd.read_json('C:/Users/quenf/Bike_challenge2/Visualization/JSON_Files/MMM_EcoCompt_X2H20063162_archive.json', lines = True)
dict_[6] = pd.read_json('C:/Users/quenf/Bike_challenge2/Visualization/JSON_Files/MMM_EcoCompt_XTH19101158_archive.json', lines = True)
dict_[7] = pd.read_json('C:/Users/quenf/Bike_challenge2/Visualization/JSON_Files/MMM_EcoCompt_X2H20063163_archive.json', lines = True)


# %%
dict_coord = {} #empty dictionary in which we will put coordinates of each Eco meter

#We fill dict_coord up
# and we only keep variables we're interested in for the visualization

for i in range(8):
    dict_coord[i] = dict_[i]['location'][0]
    dict_[i].drop(columns = ['laneId', 'id', 'type', 'vehicleType','reversedLane'], inplace = True)


#%%
#Latitude and longitude are reversed in first and last dict_coord elements
list_ = []
for i in range(8):
    list_ = list_ + [list(dict_coord[i].values())[0]]
list_[0][0], list_[0][1] = list_[0][1], list_[0][0]
list_[7][0], list_[7][1] = list_[7][1], list_[7][0]


#%%
#Creation of a dictionary in which we will 
#put every single html_file, containing 
#information about the date bound to its name

dict_map = {} 

for i in range(0, dict_[0].shape[0]):
    dict_map[i] = folium.Map(location=[43.610769, 3.876716 ], zoom_start=12) 
    #best zoom to see clearly every piece of information we need
    folium.raster_layers.TileLayer('OpenStreetMap').add_to(dict_map[i])
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(dict_map[i])
    folium.raster_layers.TileLayer('Stamen Toner').add_to(dict_map[i])
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(dict_map[i])
    folium.raster_layers.TileLayer('CartoDB positron').add_to(dict_map[i])
    folium.raster_layers.TileLayer('CartoDB dark_matter').add_to(dict_map[i])
    #add layer control to show different map types
    folium.LayerControl().add_to(dict_map[i])
    for j in range(8):
        folium.CircleMarker(location = list_[j], radius = dict_[j]['intensity'][i]/60, color = 'OrangeRed',  fill_color = 'DarkOrange').add_to(dict_map[i])
    dict_map[i].save(f"Day_{str(dict_[j]['dateObserved'][i])[0:10]}.html")


#%%
#Creation of our gif

png_dir = '../Visualization'
images = []
for file_name in sorted(os.listdir(png_dir)):
    if file_name.endswith('.png'):
        file_path = os.path.join(png_dir, file_name)
        images.append(imageio.imread(file_path))
imageio.mimsave('../Visualization/gif/Vis.gif', images, fps = 2) 
#fps option gives the gif framerate
