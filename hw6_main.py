# Jon Formantes
# 4/5/2023

import pandas as pd
import geopandas as gpd
import math
import matplotlib.pyplot as plt

def load_in_data(shape_file, csv_file):
    gdf = gpd.read_file(shape_file)
    pf = pd.read_csv(csv_file)
    df = gdf.merge(pf, left_on='CTIDFP00', right_on='CensusTract', how='outer')
    return df

def percentage_food_data(data):
    df = data[data['State'] == 'WA']
    NaNFrames = data[data['State'] == 'WA'].dropna()
    return 100 * (len(NaNFrames)/len(df))

def plot_map(data):
    df = data[data['State'] == 'WA'].dropna()
    df.plot()
    plt.savefig('washington_map.png')
    plt.show()

def plot_population_map(data):
    df = data[data['State'] == 'WA']
    df.plot(column='POP2010', legend=True)
    plt.savefig('washington_population_map.png')
    plt.show()

def plot_population_county_map(data):
    df = data[data['State'] == 'WA']
    df = data[['County', 'POP2010', 'geometry']]
    # print(type(df))
    pop_by_county = df.dissolve(by='County', aggfunc='sum')
    pop_by_county.plot(column='POP2010', legend = True, figsize=(10, 5))
    plt.savefig('washington_county_population_map.png')
    plt.show()


def plot_food_access_by_county(data):
    df = data[data['State'] == 'WA']
    df = data[['County', 'geometry', 'POP2010', 'lapophalf', 'lapop10', 'lalowihalf', 'lalowi10']]
    pop_by_county = df.dissolve(by='County', aggfunc='sum')
    pop_by_county['lapophalf_ratio'] = [pophalf/pop for pop, pophalf in zip(pop_by_county['POP2010'], pop_by_county['lapophalf'])]
    pop_by_county['lapop10_ratio'] = [pop10/pop for pop, pop10 in zip(pop_by_county['POP2010'], pop_by_county['lapop10'])]
    pop_by_county['lalowihalf_ratio'] = [poplowi/pop for pop, poplowi in zip(pop_by_county['POP2010'], pop_by_county['lalowihalf'])]
    pop_by_county['lalowi10_ratio'] = [poplowi10/pop for pop, poplowi10 in zip(pop_by_county['POP2010'], pop_by_county['lalowi10'])]
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=(20, 10))
    pop_by_county.plot(ax=ax1, column='lapophalf_ratio', legend=True, figsize=(10, 5), vmin=0, vmax=1)
    ax1.set_title('Low Access: Half')
    pop_by_county.plot(ax=ax2, column='lapop10_ratio', legend=True, figsize=(10, 5), vmin=0, vmax=1)
    ax2.set_title('Low Access: 10')
    pop_by_county.plot(ax=ax3, column='lalowihalf_ratio', legend=True, figsize=(10, 5), vmin=0, vmax=1)
    ax3.set_title('Low Access + Low Income: Half')
    pop_by_county.plot(ax=ax4, column='lalowi10_ratio',
                       legend=True, figsize=(10, 5), vmin=0, vmax=1)
    ax4.set_title('Low Access + Low Income: 10')
    fig.savefig('washington_county_food_access.png')
    plt.show()

def plot_low_access_tracts(data):
    df = data[data['State'] == 'WA']
    NaNframe = df.dropna()
    df = df[df['POP2010'] != 0]
    frame = df
    frame['lapophalf_ratio'] = [col_a/col_b for col_b, col_a in zip(frame['POP2010'], frame['lapophalf'])]
    frame['lapop10_ratio'] = [col_a/col_b for col_b, col_a in zip(frame['POP2010'], frame['lapop10'])]
    frame['low_access_tracts'] = frame.apply(low_access_tracts, axis=1)
    frame = frame[frame['low_access_tracts'] == 1]
    # print(frame.head())
    fig, ax = plt.subplots(1)
    frame.plot(ax=ax, color='#EEEEEE')
    NaNframe.plot(ax=ax, color='#AAAAAA')
    frame.plot(ax=ax, color='#1f77b4', column='low_access_tracts')
    plt.show()
    plt.savefig('washington_low_access.png')
    # NaNframe.plot(ax=ax, color='#AAAAAA')
    
def low_access_tracts(data):
    if data['Urban'] == 1:
        if (data['lapophalf'] > 500) or (data['lapophalf_ratio'] > .33):
            val = 1
        else:
            val = 0
    if data['Rural'] == 1:
        if (data['lapop10'] > 500) or (data['lapop10_ratio'] > .33):
            val = 1
        else:
            val = 0
    return val 

def main():
    data = load_in_data('tl_2010_53_tract00/tl_2010_53_tract00.shp', 'food_access.csv')
    # plot_map(data)
    # print(data)
    # percentage_food_data(data)
    # plot_population_map(data)
    # plot_population_county_map(data)
    # plot_food_access_by_county(data)
    plot_low_access_tracts(data)



if __name__ == '__main__':
    main()