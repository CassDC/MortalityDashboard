import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime


def create_graph_data(g):
    return list(map(lambda data_row: {"x": g.x, "y": data_row.values, "type": g.type, 'name': data_row.name}, g.y))


def create_graph_pane(g):
    layout_properties = {"title": g.title, "xaxis": {"title": g.xtitle, "tickangle": g.tick_angle},
                         "yaxis": {"title": g.ytitle}}
    return place_in_card(None, dcc.Graph(id=g.id, figure={"data": create_graph_data(g), "layout": layout_properties}))


def create_table_pane(t):
    heading = [html.Thead(html.Tr([html.Th(t.col1), html.Th(t.col2)]), className="text-center")]
    rows = map(lambda row: html.Tr([html.Td(row[1][0]), html.Td(row[1][1])]), t.values.iterrows())
    body = [html.Tbody(list(rows), className="text-center")]
    return place_in_card(t.title, dbc.Table(heading + body, bordered=False))


def create_iframe_pane(m):
    return place_in_card(m.title, html.Iframe(id=m.id, srcDoc=open(m.name, 'r').read(), width='100%', height=500))


def create_info_box(b):
    color = 'text-success' if b.value.startswith('-') else 'text-danger'
    return place_in_card(b.title, html.H3(b.value, className=f"text-center {color}"))


def place_in_card(title, elements):
    title_component = [] if title == None else [dbc.CardHeader(html.Header(title, className="text-center"))]
    return dbc.Card(title_component + [dbc.CardBody([elements])], outline=True)


def create_each(fnc, items):
    return list(map(lambda x: fnc(x), items))


def start_server(graphs, folium_maps, tables, info_boxes):
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Panthera Demo")
    graph_panes = create_each(create_graph_pane, graphs)
    info_panes = [dbc.CardGroup(create_each(create_info_box, info_boxes))]
    iframe_panes = create_each(create_iframe_pane, folium_maps)
    table_panes = create_each(create_table_pane, tables)

    jumbotron = dbc.Jumbotron(
        [
            html.H3("South African Mortality Trends Between 2011 - 2017"),
            html.Hr(),
            html.P("A basic dashboard showing a decrease in deaths to tuberculosis and an increase in deaths to lifestyle diseases across all provinces.")
        ], className="mt-3")

    navbar = dbc.NavbarSimple(brand="Panthera Project Demo", brand_href="#", color="info", dark=True,
                              children=[dbc.NavItem(html.Header("Cassandra da Cruz", className="text-light"))])

    section_A = list(map(lambda frame: dbc.Row(dbc.Col(html.Div(frame)), className="mt-3"), info_panes + graph_panes))
    section_B = [
        dbc.Row([dbc.Col(iframe_panes, className="col-8"), dbc.Col(table_panes, className="col-4")], className="mt-3")]
    container = dbc.Container([jumbotron] + section_A + section_B, className="col-8")

    now = datetime.now()  # current date and time
    footer = html.Div(className="footer text-center mt-3 text-dark",
                      children=[html.Hr(), html.P(f"Latest update provided on {now.strftime('%d %B %Y at %H:%M:%S')}"),
                                html.P("◕‿◕"), html.P("By Cassandra da Cruz")])

    app.layout = html.Div([navbar, container, footer])

    app.run_server(debug=False, host="0.0.0.0", port=80)
