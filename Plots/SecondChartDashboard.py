import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/Olympic2016Rio.csv')
df2 = pd.read_csv('../Datasets/Weather2014-15.csv')

app = dash.Dash()

# Bar chart data
data_barchart = [go.Bar(x=df1['NOC'], y=df1['Total'])]

# Stack bar chart data
stackbarchart_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
stackbarchart_df = stackbarchart_df.groupby(['NOC']).agg(
    {'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum', 'Total': 'sum'}).reset_index()
trace1_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Bronze'], name='Bronze',
                              marker={'color': '#CD7F32'})
trace2_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Silver'], name='Silver',
                              marker={'color': '#9EA0A1'})
trace3_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Gold'], name='Gold',
                              marker={'color': '#FFD700'})
data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart]

# Line Chart
line_df = df2
line_df['date'] = pd.to_datetime(line_df['date'])
data_linechart = [go.Scatter(x=line_df['date'], y=line_df['actual_mean_temp'], mode='lines', name='Mean_Temp')]

# Multi Line Chart
multiline_df = df2
multiline_df['date'] = pd.to_datetime(multiline_df['date'])
trace1_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_max_temp'], mode='lines', name='Max')
trace2_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_mean_temp'], mode='lines', name='Mean')
trace3_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_min_temp'], mode='lines', name='Min')
data_multiline = [trace1_multiline, trace2_multiline, trace3_multiline]

# Bubble chart
bubble_df = df2.groupby(['month']).agg({
  'average_min_temp': 'mean',
  'average_max_temp': 'mean',
  'record_max_temp': 'max'
}).reset_index()

data_bubblechart = [go.Scatter(x=bubble_df['average_min_temp'], y=bubble_df['average_max_temp'],
                   text=bubble_df['month'], mode='markers',
                   marker=dict(size=bubble_df['record_max_temp'], color=bubble_df['record_max_temp'], showscale=True))]

# Heatmap
heatmap_df = df2.groupby(['month', 'day']).agg({
  'record_max_temp': 'max'
}).reset_index()

data_heatmap = [go.Heatmap(x=heatmap_df['day'], y=heatmap_df['month'], z=heatmap_df['record_max_temp'])]

# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Olympics 2016 Rio', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent of Gold, Silver, and Bronze medals per country.'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a country', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-continent',
        options=[
            {'label': 'United States', 'value': 'United States(USA)'},
            {'label': 'Great Britain', 'value': 'Great Britain(GBR)'},
            {'label': 'China', 'value': 'China(CHN)'},
            {'label': 'Russia', 'value': 'Russia(RUS)'},
            {'label': 'Germany', 'value': 'Germany(GER)'},
            {'label': 'France', 'value': 'France(FRA)'}
        ],
        value='United States(USA)'
    ),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the total number of medals won by the US.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Gold, Silver, and Bronze medals won by the US',
                                      xaxis={'title': 'Medals'}, yaxis={'title': 'Number of medals'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represent the number of Gold, Silver, and Bronze medals won by each country.'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Number of Gold, Silver, and Bronze medals won by each country.',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Number of medals'},
                                      barmode='stack')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represent the average mean temperature by date.'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_linechart,
                  'layout': go.Layout(title='Average mean temperature by date.',
                                      xaxis={'title': 'Date'}, yaxis={'title': 'Average mean temperature'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This line chart represent the max, mean, and min temperatures by date'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='Max, mean, and min temperatures by date',
                      xaxis={'title': 'Date'}, yaxis={'title': 'Temperature'})
              }
              ),
    #html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble chart', style={'color': '#df1e56'}),
    html.P('This bubble chart represents the record min and max temperatures'),
    dcc.Graph(id='graph6', figure={
        'data': data_bubblechart,
        'layout': go.Layout(title='Min and Max Temperatures',
                            xaxis={'title': 'Average Min Temp'},
                            yaxis={'title': 'Average Max Temp'},
                            hovermode='closest')
    }),
])


@app.callback(Output('graph1', 'figure'),
              [Input('select-continent', 'value')])
def update_figure(selected_continent):
    filtered_df = df1[df1['Continent'] == selected_continent]

    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    new_df = filtered_df.groupby(['Country'])['Confirmed'].sum().reset_index()
    new_df = new_df.sort_values(by=['Confirmed'], ascending=[False]).head(20)
    data_interactive_barchart = [go.Bar(x=new_df['Country'], y=new_df['Confirmed'])]
    return {'data': data_interactive_barchart, 'layout': go.Layout(title='Corona Virus Confirmed Cases in '+selected_continent,
                                                                   xaxis={'title': 'Country'},
                                                                   yaxis={'title': 'Number of confirmed cases'})}


if __name__ == '__main__':
    app.run_server()
