from data_capture import *
from server import *

if __name__ == '__main__':
    df = read_data()
    gj = read_geojson()

    years = df.columns[3:]  # List of years for time series

    map_southafrica = make_base_map(-30.5595, 22.9375, 5)
    map_data = proportion_multiple_diseases(df, 2017, ["KN.H5", "KN.H9", "KN.H11", "KN.H4"])
    bins = make_pretty_legend(map_data, 5)
    folium_map = make_folium_map(map_southafrica, gj, map_data, ["Province", "2017"], 'properties.PROVINCE', 'YlOrRd', bins, "Percentage of deaths from reportable non-communicable diseases per province in 2017 (%)")
    folium_map.save('folium_map.html')

    t1 = Table(map_data, "Non-communicable disease deaths in 2017 [percentage of total deaths]", "Province", "Percent")

    graphs = [graph_disease_all_provinces(df, "KN.H2", years, 2011, 2017, "Tuberculosis deaths as a proportion of total deaths for 2011-2017","Years", "Proportion to total deaths [%]"),
              graph_disease_all_provinces(df, "KN.H4", years, 2011, 2017, "Diabetes deaths as a proportion of total deaths for 2011-2017", "Years", "Proportion to total deaths [%]"),
              graph_diseases_by_province_per_year(df, "Western Cape", "Causes of death in the Western Cape in 2017", "Cause of death", "Number of deaths", 2017),
              graph_disease_categories(df, "Communicable and non-communicable diseases as a proportion of South African deaths for 2011-2017", "Years", "Proportion to total deaths [%]", years)]

    info_boxes = [change_in_disease_share(df, "KN.H2", 2011, 2017, "Change in share of tuberculosis 2011 - 2017"),
                  change_in_disease_share(df, "KN.H6", 2011, 2017, "Change in share of deaths to HIV 2011 - 2017"),
                  change_in_disease_share(df, "KN.H4", 2011, 2017, "Change in share of deaths to diabetes 2011 - 2017"),
                  change_in_disease_share(df, "KN.H11", 2011, 2017, "Change in share of deaths to hypertension 2011 - 2017")]

    sa_map = FoliumMap('folium_map.html', "Non-communicable disease deaths in 2017 [percentage of total deaths]")

    start_server(graphs, [sa_map], [t1], info_boxes)

