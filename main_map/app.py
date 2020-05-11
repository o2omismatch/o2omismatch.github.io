import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import geopandas as gpd

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoidGlhbnl1c3UiLCJhIjoiY2pzcDVjbHN4MGJlODN5cWdxcWhvNmhhNiJ9._-JbYk5jLroDDTxSoEWS3A"

# Dictionary of important locations in New York
# list_of_locations = {
#     "Madison Square Garden": {"lat": 40.7505, "lon": -73.9934},
#     "Yankee Stadium": {"lat": 40.8296, "lon": -73.9262},
#     "Empire State Building": {"lat": 40.7484, "lon": -73.9857},
#     "New York Stock Exchange": {"lat": 40.7069, "lon": -74.0113},
#     "JFK Airport": {"lat": 40.644987, "lon": -73.785607},
#     "Grand Central Station": {"lat": 40.7527, "lon": -73.9772},
#     "Times Square": {"lat": 40.7589, "lon": -73.9851},
#     "Columbia University": {"lat": 40.8075, "lon": -73.9626},
#     "United Nations HQ": {"lat": 40.7489, "lon": -73.9680},
# }

# Initialize data frame
# df1 = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data1.csv",
#     dtype=object,
# )
# df2 = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data2.csv",
#     dtype=object,
# )
# df3 = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data3.csv",
#     dtype=object,
# )
# df = pd.concat([df1, df2, df3], axis=0)
# df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%Y-%m-%d %H:%M")
# df.index = df["Date/Time"]
# df.drop("Date/Time", 1, inplace=True)
# totalList = []
# for month in df.groupby(df.index.month):
#     dailyList = []
#     for day in month[1].groupby(month[1].index.day):
#         dailyList.append(day[1])
#     totalList.append(dailyList)
# totalList = np.array(totalList)

##### Mismatch Data
df_geo = gpd.read_file('assets/street_mismatch_extract.geojson')
# df_geo = df_geo.to_crs("EPSG:4326")
# df_geo = df_geo.dropna()
# df_geo = df_geo.reset_index(drop=True)

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("mismatch_logo.png")
                        ),
                        html.H2("O2O NYC"),
                        dcc.Graph(id="histogram"),
                        html.P(
                            """Select different data source or by selecting
                            different time frames on the histogram."""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id='data-dropdown',
                                    options=[
                                        {'label': 'Offline', 'value':'total_visit'},
                                        {'label': 'Online', 'value':'review_num_tot'},
                                        {'label': 'Mismatch', 'value':'mismatch_log'}
                                    ],
                                    value='mismatch_log'
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        # html.Div(
                        #     className="row",
                        #     children=[
                        #         # html.Div(
                        #         #     className="div-for-dropdown",
                        #         #     children=[
                        #         #         # Dropdown for locations on map
                        #         #         dcc.Dropdown(
                        #         #             id="location-dropdown",
                        #         #             options=[
                        #         #                 {"label": i, "value": i}
                        #         #                 for i in list_of_locations
                        #         #             ],
                        #         #             placeholder="Select a location",
                        #         #         )
                        #         #     ],
                        #         # ),
                        #         # html.Div(
                        #         #     className="div-for-dropdown",
                        #         #     children=[
                        #         #         # Dropdown to select times
                        #         #         dcc.Dropdown(
                        #         #             id="bar-selector",
                        #         #             options=[
                        #         #                 {
                        #         #                     "label": str(n) + ":00",
                        #         #                     "value": str(n),
                        #         #                 }
                        #         #                 for n in range(24)
                        #         #             ],
                        #         #             multi=True,
                        #         #             placeholder="Select certain hours",
                        #         #         )
                        #         #     ],
                        #         # ),
                        #     ],
                        # ),
                        html.P(id="total-rides"),
                        html.P(id="total-rides-selection"),
                        html.P(id="date-value"),
                        # dcc.Markdown(
                        #     children=[
                        #         "Source: [FiveThirtyEight](https://github.com/fivethirtyeight/uber-tlc-foil-response/tree/master/uber-trip-data)"
                        #     ]
                        # ),
                        
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        # dcc.Graph(id="map-graph"),
                        dcc.Graph(id="map_mismatch"),
                        html.Div(
                            className="text-padding",
                            children=[
                                "Select any of the bars on the histogram to section data by time."
                            ],
                        ),
                        # dcc.Graph(id="histogram"),
                    ],
                ),
            ],
        )
    ]
)

# # Gets the amount of days in the specified month
# # Index represents month (0 is April, 1 is May, ... etc.)
# daysInMonth = [30, 31, 30, 31, 31, 30]

# # Get index for the specified month in the dataframe
# monthIndex = pd.Index(["Apr", "May", "June", "July", "Aug", "Sept"])

# Get the amount of rides per hour based on the time selected
# This also higlights the color of the histogram bars based on
# if the hours are selected
def get_selection(datasource):
    xVal = []
    yVal = []
    xSelected = []
    colorVal = [
        "#F4EC15",
        "#DAF017",
        "#BBEC19",
        "#9DE81B",
        "#80E41D",
        "#66E01F",
        "#4CDC20",
        "#34D822",
        "#24D249",
        "#25D042",
        "#26CC58",
        "#28C86D",
        "#29C481",
        "#2AC093",
        "#2BBCA4",
        "#2BB5B8",
        "#2C99B4",
        "#2D7EB0",
        "#2D65AC",
        "#2E4EA4",
        "#2E38A4",
        "#3B2FA0",
        "#4E2F9C",
        "#603099",
    ]

    # Put selected times into a list of numbers xSelected
    xSelected.extend([int(x) for x in selection])

    for i in range(df_geo.shape[0]):
        # If bar is selected then color it white
        # if i in xSelected and len(xSelected) < 24:
        #     colorVal[i] = "#FFFFFF"
        xVal.append(i)
        # Get the number of rides at a particular time
        yVal.append(len(totalList[month][day][totalList[month][day].index.hour == i]))
    return [np.array(xVal), np.array(yVal), np.array(colorVal)]

def map_color(min_val, max_val, val):
    colors = ['#00939c', '#5dbabf', '#bae1e2', '#f8c0aa', '#dd7755', '#c22e01']
    # print(int(np.floor((val - min_val) / (max_val - min_val) * 6)))
    return colors[int(np.floor((val - min_val) / (max_val - min_val) * 6 - 0.01))]


# # Selected Data in the Histogram updates the Values in the DatePicker
# @app.callback(
#     Output("bar-selector", "value"),
#     [Input("histogram", "selectedData"), Input("histogram", "clickData")],
# )
# def update_bar_selector(value, clickData):
#     holder = []
#     if clickData:
#         holder.append(str(int(clickData["points"][0]["x"])))
#     if value:
#         for x in value["points"]:
#             holder.append(str(int(x["x"])))
#     return list(set(holder))


# # Clear Selected Data if Click Data is used
# @app.callback(Output("histogram", "selectedData"), [Input("histogram", "clickData")])
# def update_selected_data(clickData):
#     if clickData:
#         return {"points": []}


# # Update the total number of rides Tag
# @app.callback(Output("total-rides", "children"), [Input("date-picker", "date")])
# def update_total_rides(datePicked):
#     date_picked = dt.strptime(datePicked, "%Y-%m-%d")
#     return "Total Number of rides: {:,d}".format(
#         len(totalList[date_picked.month - 4][date_picked.day - 1])
#     )


# # Update the total number of rides in selected times
# @app.callback(
#     [Output("total-rides-selection", "children"), Output("date-value", "children")],
#     [Input("date-picker", "date"), Input("bar-selector", "value")],
# )
# def update_total_rides_selection(datePicked, selection):
#     firstOutput = ""

#     if selection is not None or len(selection) is not 0:
#         date_picked = dt.strptime(datePicked, "%Y-%m-%d")
#         totalInSelection = 0
#         for x in selection:
#             totalInSelection += len(
#                 totalList[date_picked.month - 4][date_picked.day - 1][
#                     totalList[date_picked.month - 4][date_picked.day - 1].index.hour
#                     == int(x)
#                 ]
#             )
#         firstOutput = "Total rides in selection: {:,d}".format(totalInSelection)

#     if (
#         datePicked is None
#         or selection is None
#         or len(selection) is 24
#         or len(selection) is 0
#     ):
#         return firstOutput, (datePicked, " - showing hour(s): All")

#     holder = sorted([int(x) for x in selection])

#     if holder == list(range(min(holder), max(holder) + 1)):
#         return (
#             firstOutput,
#             (
#                 datePicked,
#                 " - showing hour(s): ",
#                 holder[0],
#                 "-",
#                 holder[len(holder) - 1],
#             ),
#         )

#     holder_to_string = ", ".join(str(x) for x in holder)
#     return firstOutput, (datePicked, " - showing hour(s): ", holder_to_string)


# Update Histogram Figure based on Month, Day and Times Chosen
@app.callback(
    Output("histogram", "figure"),
    [Input("data-dropdown", "value")],
)
def update_histogram(datasource):
    # date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    # monthPicked = date_picked.month - 4
    # dayPicked = date_picked.day - 1

    # [xVal, yVal, colorVal] = get_selection(monthPicked, dayPicked, selection)
    # xVal = list(range(df_geo.shape[0]))
    xVal = df_geo[datasource].to_list()


    layout = go.Layout(
        bargap=0.01,
        bargroupgap=0,
        barmode="group",
        margin=go.layout.Margin(l=10, r=0, t=0, b=50),
        showlegend=False,
        plot_bgcolor="#323130",
        paper_bgcolor="#323130",
        dragmode="select",
        font=dict(color="white"),
        xaxis=dict(
            range=[min(xVal), max(xVal)],
            showgrid=False,
            nticks=10,
            fixedrange=True,
            ticksuffix=":00",
        ),
        # yaxis=dict(
        #     range=[0, max(yVal) + max(yVal) / 4],
        #     showticklabels=False,
        #     showgrid=False,
        #     fixedrange=True,
        #     rangemode="nonnegative",
        #     zeroline=False,
        # ),
        # annotations=[
        #     dict(
        #         x=xi,
        #         y=yi,
        #         text=str(yi),
        #         xanchor="center",
        #         yanchor="bottom",
        #         showarrow=False,
        #         font=dict(color="white"),
        #     )
        #     for xi, yi in zip(xVal, yVal)
        # ],
    )

    return go.Figure(
        data=[
            go.Histogram(
                x = xVal,
                nbinsx = 10,
                # nbinsy = 8,
            )
            # go.Bar(x=xVal, y=yVal, marker=dict(color=colorVal), hoverinfo="x"),
            # go.Scatter(
            #     opacity=0,
            #     x=xVal,
            #     y=yVal / 2,
            #     hoverinfo="none",
            #     mode="markers",
            #     marker=dict(color="rgb(66, 134, 244, 0)", symbol="square", size=40),
            #     visible=True,
            # ),
        ],
        layout=layout,
    )


# Get the Coordinates of the chosen months, dates and times
def getLatLonColor(selectedData, month, day):
    listCoords = totalList[month][day]

    # No times selected, output all times for chosen month and date
    if selectedData is None or len(selectedData) is 0:
        return listCoords
    listStr = "listCoords["
    for time in selectedData:
        if selectedData.index(time) is not len(selectedData) - 1:
            listStr += "(totalList[month][day].index.hour==" + str(int(time)) + ") | "
        else:
            listStr += "(totalList[month][day].index.hour==" + str(int(time)) + ")]"
    return eval(listStr)


# Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("map_mismatch", "figure"),
    [
        Input("data-dropdown", "value"),
        # Input("bar-selector", "value"),
        # Input("location-dropdown", "value"),
    ],
)
def update_graph(datasource):
    zoom = 12.0
    latInitial = 40.7573868055177
    lonInitial = -73.98225504782917
    bearing = 0

    # if selectedLocation:
    #     zoom = 15.0
    #     latInitial = list_of_locations[selectedLocation]["lat"]
    #     lonInitial = list_of_locations[selectedLocation]["lon"]

    # date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    # monthPicked = date_picked.month - 4
    # dayPicked = date_picked.day - 1
    # listCoords = getLatLonColor(selectedData, monthPicked, dayPicked)
    color_min = df_geo[datasource].min()
    color_max = df_geo[datasource].max()

    fig_temp =  go.Figure(
            # Data for all rides based on date and time
        go.Scattermapbox(
            lat=[i[1] for i in list(df_geo.geometry[0].coords)],
            lon=[i[0] for i in list(df_geo.geometry[0].coords)],
            mode="lines",
            hoverinfo="none",
            line=dict(width=2, color="#ff4931"),
        ),
    )

    for i, feature in enumerate(df_geo.iloc):
        if 500>i>0:
            fig_temp.add_trace(
                go.Scattermapbox(
                    mode = "lines",
                    lat = [j[1] for j in list(feature.geometry.coords)],
                    lon = [j[0] for j in list(feature.geometry.coords)],
                    line = dict(width=feature['store_num'] / 180 * 16 + 1, color=map_color(color_min, color_max, feature[datasource])),
                )
            )

    fig_temp.update_layout(
        autosize=True,
        margin=go.layout.Margin(l=0, r=35, t=0, b=0),
        showlegend=False,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            center=dict(lat=latInitial, lon=lonInitial),  # 40.7272  # -73.991251
            style="mapbox://styles/tianyusu/cka0fm6r317nf1ik59o3q72qi",
            bearing=bearing,
            zoom=zoom,
        ),
        updatemenus=[
            dict(
                buttons=(
                    [
                        dict(
                            args=[
                                {
                                    "mapbox.zoom": 12,
                                    "mapbox.center.lon": "-73.991251",
                                    "mapbox.center.lat": "40.7272",
                                    "mapbox.bearing": 0,
                                    "mapbox.style": "mapbox://styles/tianyusu/cka0fm6r317nf1ik59o3q72qi",
                                }
                            ],
                            label="Reset Zoom",
                            method="relayout",
                        )
                    ]
                ),
                direction="left",
                pad={"r": 0, "t": 0, "b": 0, "l": 0},
                showactive=False,
                type="buttons",
                x=0.45,
                y=0.02,
                xanchor="left",
                yanchor="bottom",
                bgcolor="#323130",
                borderwidth=1,
                bordercolor="#6d6d6d",
                font=dict(color="#FFFFFF"),
            )
        ],
    )
    
    return fig_temp






if __name__ == "__main__":
    app.run_server(debug=False)
