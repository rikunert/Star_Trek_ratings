# Please use Python version 2.7

# This script uses the IMDb API and web scraping in order to get Star Trek movie ratings and produce a scatter plot

# author: Richard Kunert (rikunert@gmail.com) May 2017

import imdb as imdb  # to access imdb API
import pandas as pd  # for data array handling
from BeautifulSoup import BeautifulSoup  # for website parsing and scraping (rotten tomatoes)
import requests  # for http access
import re  # for regular expressions
from ggplot import *  # for plotting
import urllib2  # for accessing url object (movie covers)
import matplotlib.pyplot as plt  # for plotting
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)

# global variables
work_dir = 'C:\Users\Richard\Desktop\python\IMDb_analyses\Star Trek'

imdb_http = imdb.IMDb()  # create imdb API object
StarTrek = imdb_http.search_movie('Star Trek')  # general search for Star Trek among movie and series titles
STF = [i for i in StarTrek if i.data['kind'] == 'movie']

# for some reason this approach misses 5 movies, add them
StarTrekIII = imdb_http.search_movie('Star Trek III the Search for Spock')
StarTrekIV = imdb_http.search_movie('Star Trek IV the voyage home')
StarTrekV = imdb_http.search_movie('Star Trek V the Final Frontier')
StarTrekVI = imdb_http.search_movie('Star Trek VI the Undiscovered Country')
StarTrekFC = imdb_http.search_movie('Star Trek First Contact')
STF.extend([StarTrekIII[0], StarTrekIV[0], StarTrekV[0], StarTrekVI[0], StarTrekFC[0]])

df = pd.DataFrame(columns=['date', 'IMDb_rating', 'Metacritic_rating', 'title', 'image_url'])  # initialise data frame

for i in range(len(STF)):  # for each Star Trek movie

    imdb_http.update(STF[i])  # IMDb: augment movie info
    x = imdb_http.get_movie_critic_reviews(STF[i].movieID)  # Meta critic

    # rotten tomato: prepare website parsing
    tomato_base_url = 'https://www.rottentomatoes.com/m/'
    tomato_url = tomato_base_url + re.sub(':', '', re.sub(' ', '_', str(STF[i]['title'])))
    if 'Star Trek' not in STF[i]['title']:  # fix first contact problem
        tomato_url = tomato_base_url + re.sub(':', '', re.sub(' ', '_', 'Star Trek ' + str(STF[i]['title'])))
    elif 'Khan' in STF[i]['title']:  # fix wrath of khan problem
        tomato_url = tomato_base_url + re.sub(':', '_II', re.sub(' ', '_', str(STF[i]['title'])))
    soup = BeautifulSoup(requests.get(tomato_url).text)  # rotten tomatoes: website parse tree

    # add data to pandas data frame
    if 'year' in STF[i].data.keys() and bool(x['data']):  # filter out movies in production and those without MC data
        df = df.append(pd.DataFrame(data={
            'date': STF[i].data['year'],
            'IMDb_rating': [((STF[i].data['rating'] - 1) / 9.0) * 5],  # normalised to 5 star system
            'Metacritic_rating': [int(x['data']['metascore']) / 20.0],  # normalised to 5 star system
            'Tomatometer': [
                int(min(soup.find('span', {'class': 'meter-value superPageFontColor'}).contents[0])) / 20.0],
        # rotten tomatoe score (normalised to 5 star system)
            'Tomato_user': [
                int(filter(str.isdigit, str(soup.find('span', {'class': 'superPageFontColor'}).contents[0]))) / 20.0],
        # tomato audience score (normalised to 5 star system)
            'title': STF[i].data['title'],
            'image_url': STF[i]['cover url']}))

df.to_csv(work_dir + '\Star_Trek_movie_data.csv', sep=';')  # save data to disc

########################################################################################################################
# Plotting

df = pd.read_csv(work_dir + '\Star_Trek_movie_data.csv', sep=';')

# start plotting using ggplot
p = ggplot(aes(x='date', y='IMDb_rating'), data=df) + geom_point() + \
    geom_line(size=5, color='orange') + theme_bw()  # basic plot
p = p + geom_line(aes(x='date', y='Metacritic_rating'), data=df, size=5, color='purple')
p = p + geom_line(aes(x='date', y='Tomatometer'), data=df, size=5, color='grey')
p = p + geom_line(aes(x='date', y='Tomato_user'), data=df, size=5, color='blue')
p = p + ylim(0, 5) + xlim(1975, 2016) + xlab(' ') + ylab(' ') + ggtitle('Star Trek movie ratings')  # make axes pretty

p.make()  # exporting the figure to use it in matplotlib
plt.text(2017.5, 0, '@rikunert', color='black')  # keep figure open for this to work
plt.text(2017.5, 4.25, 'Rotten\nTomatoes', color='grey')  # keep figure open for this to work
plt.text(2017.5, 3.75, 'Rotten\nTomatoes\nusers', color='blue')  # keep figure open for this to work
plt.text(2017.5, 3.4, 'IMDb users', color='orange')  # keep figure open for this to work
plt.text(2017.5, 3.2, 'Metacritic', color='purple')  # keep figure open for this to work

ax = plt.gca()  # get current axes (axes is like the drawing area apparently)


# add movie cover art
def add_image(ax_, url, xy, imzoom):
    if 'http' in url:  # image on internet
        f = urllib2.urlopen(url)
    else:  # image in working directory
        f = url
    arr_img = plt.imread(f, format='jpg')
    imagebox = OffsetImage(arr_img, zoom=imzoom)
    imagebox.image.axes = ax_
    ab = AnnotationBbox(imagebox, xy, xybox=(0., 0.), boxcoords="offset points", pad=-0.5)  # hide box behind image
    ax_.add_artist(ab)
    return ax_


for i in range(len(df)):  # for each Star Trek movie
    add_image(ax, df['image_url'][i], [df['date'][i], sum(df.iloc[i, 1:5]) / 4.0], 0.3)

ax.xaxis.set_ticks(range(1980, 2020, 10))  # minimal x-axis style
ax.yaxis.set_visible(False)  # no numerical y-axis at all
add_image(ax, work_dir + '\grey_star.jpg', [1975, 0], 0.05)  # zero stars on sort of y-axis
for i in range(1, 6):  # for each star rating from 1 onwards
    for j in range(i):  # for each individual star
        add_image(ax, work_dir + '\gold_star.jpg', [1975 + j * 0.7, i], 0.05)

ax.annotate('The absolute worst movie:\n' + df[df['IMDb_rating'] == min(df['IMDb_rating'])]['title'].iloc[0],
            xy=(1988, 1.5), xytext=(1978, 1), arrowprops=dict(facecolor='black', shrink=0.05))

fig = plt.gcf()  # get current figure to show it
fig.set_size_inches(1024 / 70, 512 / 70)  # reset the figure size to twitter standard
fig.savefig(work_dir + '\Star Trek movie ratings_dates.png', dpi=96, bbox_inches='tight')  # save figure
