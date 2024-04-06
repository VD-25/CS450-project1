import dash
from dash import dcc, html, Input,Output
import plotly.express as px
from dash.exceptions import PreventUpdate
import pandas as pd

#load dataset
df = pd.read_csv('mxmh_survey_results.csv', encoding='utf-8')

app = dash.Dash(__name__)
server = app.server

disorders = ['Anxiety', 'Depression', 'Insomnia', 'OCD']
freqs = ['Never', 'Rarely', 'Sometimes', 'Very frequently']
genres_df = ['Frequency [Classical]','Frequency [Country]','Frequency [EDM]','Frequency [Folk]','Frequency [Gospel]','Frequency [Hip hop]','Frequency [Jazz]','Frequency [K pop]','Frequency [Latin]','Frequency [Lofi]','Frequency [Metal]','Frequency [Pop]','Frequency [R&B]','Frequency [Rap]','Frequency [Rock]','Frequency [Video game music]']
app.layout = html.Div([
    html.H1('Effect of Music on Well Being Dashboard'),
    html.Label("1. Genre Frequence vs. Disorder Severity Rating"),
    dcc.Dropdown(
        id='disorder_dropdown',
        options=[{'label': disorder, 'value': disorder} for disorder in disorders],
        value=disorders[0]
    ),
    dcc.Dropdown(
        id='genre_dropdown',
        options=[{'label': genre, 'value': genre} for genre in genres_df],
        value=genres_df[0]
    ),
    dcc.Graph(id='graph1'),

    html.Label("2. Hours spent listening to music vs disorder"),
    dcc.RangeSlider(
        id='slider2',
        min=(df['Hours per day']).min(),
        max=(df['Hours per day']).max(),
        step=1,
        value=(1,5)  
    ),
    dcc.Graph(id='graph2'),

    html.Label("3. Age vs. Favorite Genre"),
    dcc.RangeSlider(
        id='slider3',
        min=(df['Age']).min(),
        max=(df['Age']).max(),
        step=1,
        value=(15,25)  
    ),
    dcc.Graph(id='graph3'),

    html.Label("4. Effect of mood based on genre and frequency"),
    dcc.Dropdown(
        id='freq_dropdown',
        options=[{'label': freq, 'value': freq} for freq in freqs],
        value='Never'
    ),
    dcc.Dropdown(
        id='genre_dropdown2',
        options=[{'label': genre, 'value': genre} for genre in genres_df],
        value=genres_df[0]
    ),
    dcc.Graph(id='graph4'),
])

#callback for the first graph
@app.callback(
    Output('graph1', 'figure'),
    [Input('genre_dropdown', 'value'),
     Input('disorder_dropdown', 'value')]
)
def update_graph1(genre, disorder):
    my_avg = df.groupby(genre)[disorder].mean()
    fig = px.bar(x=my_avg.index, y=my_avg.values)
    fig.update_layout(yaxis=dict(range=[0, 10]))
    return fig


#callback for the second graph:
@app.callback(Output('graph2', 'figure'), [Input('slider2', 'value')])
def update_graph2(hours_range):
    filtered_df = df[(df['Hours per day'] >= hours_range[0]) & (df['Hours per day'] <= hours_range[1])]
    ylist=[]
    ylist.append(filtered_df['Anxiety'].mean())
    ylist.append(filtered_df['Depression'].mean())
    ylist.append(filtered_df['Insomnia'].mean())
    ylist.append(filtered_df['OCD'].mean())
    fig = px.bar(x=['Anxiety','Depression','Insomnia','OCD'], y=ylist)
    return fig


#callback for graph 3:
@app.callback(Output('graph3','figure'), [Input('slider3', 'value')])
def update_graph3(age_range):
    filtered_df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    fig = px.pie(filtered_df, names=filtered_df['Fav genre'], title='Pie Chart with Range Slider')
    return fig


#callback for graph4:
@app.callback(Output('graph4', 'figure'), [Input('genre_dropdown2', 'value'), Input('freq_dropdown', 'value')])
def update_graph4(selected_genre, selected_freq):
    filtered_df = df[df[selected_genre] == selected_freq]
    fig = px.bar(filtered_df, x = filtered_df['Music effects'])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

