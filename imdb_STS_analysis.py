# Python version: 2.7

# This script plots IMDb Star Trek episode rating data

# author: Richard Kunert rikunert@gmail.com

# import modules
import matplotlib.pyplot as plt  # for plotting
from matplotlib.cbook import get_sample_data  # for adding image to plot
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
from ggplot import *  # for plotting
import pandas as pd  # for plotting with ggplot
import datetime as dt  # for date handling
from scipy import stats #for regression analysis
import numpy as np

# load data
df = pd.read_csv('C:\Users\Richard\Desktop\python\IMDb_analyses\Star Trek\Star_Trek_data.csv')
df['date'] = pd.to_datetime(df['date'])

########################################################################################################################
# Scatter Plot of Ratings versus Airing Date

# start plotting using ggplot
p = ggplot(aes(x='date', y='rating', colour='title'), data=df) + geom_point() + theme_bw()  # basic plot
p = p + ylim(1, 10) + scale_x_date(labels='%Y') + xlab('Date') + ylab('Mean IMDb rating')  # make axes pretty
p = p + ggtitle('Star Trek episode ratings')  # add title


# print p  # in case you want to see what has been made in ggplot

# continue with matplotlib for annotations and adding images


def add_starship(ax_, ship, xy, imzoom):
    fn = get_sample_data("C:\Users\Richard\Desktop\python\IMDb_analyses\Star Trek\\" + ship + ".jpg", asfileobj=False)
    arr_img = plt.imread(fn, format='jpg')
    imagebox = OffsetImage(arr_img, zoom=imzoom)
    imagebox.image.axes = ax_
    ab = AnnotationBbox(imagebox, xy,
                        xybox=(0., 0.),
                        boxcoords="offset points",
                        pad=-0.5)  # hide enclosing box behind image
    ax_.add_artist(ab)
    return ax_


p.make()  # exporting the figure to use it in matplotlib
plt.text(dt.datetime(2003, 1, 1), 1.2, '@rikunert')  # keep figure open for this to work

ax = plt.gca()  # get current axes (axes is like the drawing area apparently)
ax.legend_.remove()  # remove legend

# add images of star ships
add_starship(ax, 'TOS', [dt.datetime(1972, 1, 1), 2], 0.1)
add_starship(ax, 'TNG', [dt.datetime(1989, 1, 1), 2.5], 0.1)
add_starship(ax, 'DS9', [dt.datetime(1994, 1, 1), 2], 0.15)
add_starship(ax, 'VOY', [dt.datetime(1999, 6, 1), 2.6], 0.1)
add_starship(ax, 'ENT', [dt.datetime(2002, 1, 1), 2], 0.1)

# annotate: most delayed episode
max_TOS_date = max(df[df['title'] == 'Star Trek']['date'])
ax.annotate('That TOS episode \nwhich was not aired', xy=(max_TOS_date, df[df['date'] == max_TOS_date]['rating']),
            xytext=(dt.datetime(1975, 1, 1), 8),
            arrowprops=dict(facecolor='black', shrink=0.05))

# annotate: worst episode
min_rating = min(df['rating'])
episode_date = min(df[df['rating'] == min_rating]['date'])  # extract time stamp with min function
episode_name = df[df['rating'] == min_rating]['episode']
ax.annotate('The worst episode:\n' + episode_name.iloc[0], xy=(episode_date, min_rating),
            xytext=(dt.datetime(1980, 1, 1), 4),
            arrowprops=dict(facecolor='black', shrink=0.05))

# annotate: best episode
max_rating = max(df['rating'])
episode_date = min(df[df['rating'] == max_rating]['date'])  # extract time stamp with min function
episode_name = df[df['rating'] == max_rating]['episode']
ax.annotate('The best episode:\n' + episode_name.iloc[0], xy=(episode_date, max_rating),
            xytext=(dt.datetime(1975, 1, 1), 9.7),
            arrowprops=dict(facecolor='black', shrink=0.05))

# show and save plot
# plt.show()
fig = plt.gcf()  # get current figure
fig.set_size_inches(1024 / 70, 512 / 70)  # reset the figure size to twitter standard
fig.savefig('C:\Users\Richard\Desktop\python\IMDb_analyses\Star Trek\Star Trek ratings_dates.png', dpi=96,
            bbox_inches='tight')

########################################################################################################################
#  Density Plot of Ratings

#  start plotting using ggplot
p = ggplot(aes(x='rating', colour='title'), data=df) + geom_density() + theme_bw()  # basic plot
p = p + xlim(1, 10) + xlab('IMDb rating') + ylab('Density')  # make axes pretty
p = p + ggtitle('Star Trek episode ratings')  # add title
print p  # in case you want to see what has been made in ggplot

# continue with matplotlib for annotations and adding images
p.make()  # exporting the figure to use it in matplotlib
plt.text(9.5, 0, '@rikunert')  # keep figure open for this to work

ax = plt.gca()  # get current axes (axes is like the drawing area apparently)
ax.legend_.remove()  # remove legend

# add images of star ships
add_starship(ax, 'TOS', [6.85, 0.52], 0.05)
add_starship(ax, 'TNG', [5.38, 0.2], 0.08)
add_starship(ax, 'DS9', [8.305, 0.52], 0.15)
add_starship(ax, 'VOY', [7, 0.58], 0.1)
add_starship(ax, 'ENT', [9.05, 0.4], 0.05)

fig = plt.gcf()  # get current figure
fig.set_size_inches(1024 / 70, 512 / 70)  # reset the figure size to twitter standard
fig.savefig('C:\Users\Richard\Desktop\python\IMDb_analyses\Star Trek\Star Trek ratings_density.png', dpi=96,
            bbox_inches='tight')

########################################################################################################################
#  Scatter Plot of modern Star Trek series

# df1 = df[df['title'] != 'Star Trek'] #  remove TOS from file
# p = ggplot(aes(x='date', y='rating', colour='title'), data=df) + geom_point() + theme_bw()  # basic plot
#
# df1['date_delta'] = (df1['date'] - df1['date'].min())  / np.timedelta64(1,'D')
# slope, intercept, r_value, p_value, std_err = stats.linregress(df1['date_delta'].astype(np.int32), df1['rating'])