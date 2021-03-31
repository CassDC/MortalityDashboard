import pandas as pd
import numpy as np
import geojson
import folium
from data_components import *


def read_data():
    # Reading in raw data as dataframe
    df = pd.read_excel(r'./MortalityData.xlsx', nrows=1)
    columns = df.columns.tolist()
    cols_to_use = columns[:len(columns) - 2]
    return pd.read_excel(r'./MortalityData.xlsx', usecols=cols_to_use)


def graph_disease_all_provinces(df, disease_indicator, years, start_year, end_year, title, xtitle, ytitle):
    first_year = df.columns.get_loc(str(start_year))
    last_year = df.columns.get_loc(str(end_year))

    list_of_provinces = df[df.Indicator == disease_indicator]["Location Name"]
    total = df[df["Indicator Name"] == "Total deaths"].iloc[:, first_year:last_year + 1]
    g = df[df.Indicator == disease_indicator].iloc[:, first_year:last_year + 1]
    y = pd.DataFrame(round(np.divide(g, np.asarray(total)) * 100, 1)).reset_index(drop=True)
    y = y.swapaxes(0, 1, copy=True)

    series_data = list(map(lambda year, prov: LabeledTimeSeries(y[year].values, prov), y, list_of_provinces))

    return Graph(title, xtitle, ytitle, "lines", years, series_data)


def graph_diseases_by_province_per_year(df, province, title, xtitle, ytitle, year):
    year = str(year)
    disease_list = ["Tuberculosis", "Cerebrovascular disease", "HIV", "Other heart diseases", "Hypertension",
                    "Other natural causes", "Non-natural causes", "Diabetes"]
    y = list(df[df["Location Name"] == province].iloc[0:-2, df.columns.get_loc(year)])
    series_data = [LabeledTimeSeries(y, None)]
    return Graph(title, None, ytitle, "bar", disease_list, series_data)


def graph_disease_categories(df, title, xtitle, ytitle, years):
    total = pd.DataFrame(df[df["Indicator Name"] == "Total deaths"].iloc[:, 3:].sum())
    y = pd.concat([df.query('Indicator == "KN.H2" or Indicator == "KN.H6"').iloc[:, 3:].sum(),
                   df.query(
                       'Indicator == "KN.H5" or Indicator == "KN.H9" or Indicator == "KN.H11" or Indicator == "KN.H4"').iloc[
                   :, 3:].sum()], axis=1)
    y.columns = ['Communicable diseases', 'Non-communicable diseases']
    labels = y.columns
    y = round(np.divide(y, np.asarray(total)) * 100, 1)
    series_data = list(map(lambda year, case: LabeledTimeSeries(y[year].values, case), y, labels))
    return Graph(title, xtitle, ytitle, "lines", years, series_data)


def change_in_disease_share(df, disease, start_year, end_year, title):
    start_year = str(start_year)
    end_year = str(end_year)
    total = df[df["Indicator Name"] == "Total deaths"].iloc[:,
            df.columns.get_loc(start_year):df.columns.get_loc(end_year) + 1].sum()
    y = df[df["Indicator"] == disease].iloc[:, df.columns.get_loc(start_year):df.columns.get_loc(end_year) + 1].sum()
    y = round(np.divide(y, total) * 100, 1)
    diff = round(100 * (y[0] - y[-1]) / y[0], 1)
    symbol = '+' if diff <= 0 else '-'
    return InfoBox(title, f"{symbol} {abs(diff)} %")


def proportion_multiple_diseases(df, year, diseases):
    year = str(year)
    list_of_provinces = df[df.Indicator == "KN.H2"]["Location Name"]
    year_column = df.columns.get_loc(year)
    total = pd.DataFrame(df.query('`Indicator Name` == "Total deaths"').iloc[:, [0, year_column]])
    total.reset_index(drop=True, inplace=True)

    disease_results = [np.array(df[df["Indicator"] == disease].iloc[:, year_column]) for disease in diseases]

    province_total = np.sum(disease_results, axis=0)
    province_total = pd.DataFrame(province_total)
    province_total.insert(0, "Province", list(list_of_provinces))
    province_total.rename(columns={0: year}, inplace=True)

    province_proportions = pd.DataFrame(round(np.divide(province_total[year], total[year]) * 100, 1))
    province_proportions.insert(0, "Province", list(list_of_provinces))

    return province_proportions


def read_geojson():
    with open('map.geojson') as f:
        gj = geojson.load(f)
    return gj


def make_base_map(latitude, longitude, zoom):
    return folium.Map(location=[latitude, longitude], zoom_start=zoom)


def make_pretty_legend(y, nr_values):
    data = y.iloc[:, -1]
    new_data = data.replace([min(data), max(data)], [np.floor(min(data)), np.ceil(max(data))])
    bins = []
    for i in range(nr_values):
        range_bin = (max(new_data) - min(new_data)) / (nr_values - 1)
        bins.append(min(new_data) + i * range_bin)
    return bins


def make_folium_map(base_map, geo_data, map_data, columns, key_on, fill_colour, bins, legend_name):
    return folium.Choropleth(
        geo_data=geo_data,
        name="choropleth",
        data=map_data,
        columns=columns,
        key_on=key_on,
        fill_color=fill_colour,
        fill_opacity=0.7,
        line_opacity=0.2,
        bins=bins,
        highlight=True,
        legend_name=legend_name, ).add_to(base_map)
