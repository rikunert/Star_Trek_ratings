#Please use Python version 2.7

#This script uses the IMDb API in order to get Star Trek episode ratings

#author: Richard Kunert rikunert@gmail.com

#import modules
import imdb as imdb #to access imdb API
import pandas as pd #for data array handling
import datetime as dt#for date handling

imdb_http = imdb.IMDb()#create imdb API object
StarTrek = imdb_http.search_movie('Star Trek')#general search for Star Trek among movie and series titles

#access all Star Trek series (prune to avoid smaller series which I have never heard of)
STS = [i#extract data object of this series
       for i in StarTrek #for each imdb entry with the word star trek in it
       if i.data['kind'] == 'tv series' and#only return if it is a series
       i.data['title'] in ('Star Trek', 'Star Trek: The Next Generation', 'Star Trek: Deep Space Nine', 'Star Trek: Voyager', 'Star Trek: Enterprise')]#only return if series title is part of this tuple

df = pd.DataFrame(columns = ['date', 'rating', 'title', 'episode'])#initialise an empty data frame which will hold episode information

for series in STS:#for each series

    print 'Series: ' + series['title']#just to give the user a feeling for how far we are
    imdb_http.update(series, 'episodes')#augment series info with episode info

    for season in series.data['episodes']:#for each season

        print '    Season: ' + str(season)

        for episode in series.data['episodes'][season].keys():#for each episode

            imdb_http.update(series.data['episodes'][season][episode])#access rating of this episode

            #add data to pandas data frame
            df = df.append(pd.DataFrame(data={'date': dt.datetime.strptime(series.data['episodes'][season][episode].data['original air date'], '%d %B %Y'),
                                              'rating': [series.data['episodes'][season][episode]['rating']],
                                              'title': series['title'],
                                              'episode': series.data['episodes'][season][episode]}))

            #optional:
            #get voting details for this episode
            #imdb_http.update(series.data['episodes'][season][episode], ['main', 'vote details'])#augment episode info for more detailed voting info
            #series.data['episodes'][season][episode].data['number of votes']  # the voting distribution of this episode
            #series.data['episodes'][season][episode].data['votes']  # the number of votes
            #series.data['episodes'][season][episode].data['arithmetic mean']  # the mean rating
            #series.data['episodes'][season][episode].data['median']  # the median rating

df.to_csv('Star_Trek_data.csv')#save data to disc