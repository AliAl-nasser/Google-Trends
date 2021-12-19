import pandas as pd
import geopandas as gpd
from pytrends.request import TrendReq
import random
import os
import sys

pytrends = TrendReq(hl='en-US', tz=360)
list_of_years = []


def get_dataframe(geo_code, start_year, end_year):
    frames = []
    for i in range(start_year, end_year+1):
        list_of_years.append(str(i))
        colors = []
        for j in range(0, 10):
            hexadecimal = "#" + ''.join([random.choice('ABCDEF0123456789') for k in range(6)])
            colors.append(hexadecimal)
        year = i
        i = pytrends.top_charts(i, hl='en-US', tz=300, geo=geo_code)
        i.rename(columns={'exploreQuery': 'year'}, inplace=True)
        i["year"].replace({"": str(year)}, inplace=True)
        i['color'] = colors
        frames.append(i)

    result = pd.concat(frames)
    return result


def main(country, geo_code, start_year, end_year):
    tmp = country.strip('" "')
    output_path = 'maps'
    final_directory = os.path.join(output_path, str(tmp))
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)
    result = get_dataframe(geo_code, start_year, end_year)
    for year in list_of_years:
        df = result.loc[result['year'] == year]
        title = df['title'].tolist()
        color = df['color'].tolist()
        for string, color in zip(title, color):
            world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
            se = world.query('name ==' + country)
            fig = se.plot(figsize=(10, 10), color=color)
            fig.set_title('Top Google searches ' + str(start_year) + '-' + str(end_year) + ' in ' + str(tmp),
                          fontdict={'fontsize': '25',
                                    'fontweight': '3'})
            fig.axis('off')
            fig.annotate(year,
                         xy=(0.3, .7), xycoords='figure fraction',
                         horizontalalignment='left', verticalalignment='top',
                         fontsize=35)
            fig.annotate(string,
                         xy=(0.1, .65), xycoords='figure fraction',
                         horizontalalignment='left', verticalalignment='top',
                         fontsize=20)
            filepath = os.path.join(final_directory, str(year) + str(string) + '.png')
            top_search = fig.get_figure()
            top_search.savefig(filepath, dpi=300)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
