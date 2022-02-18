# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash

from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

app = dash.Dash(__name__)

# Import data

df = pd.read_csv("whisky.csv", delimiter=',')
df.drop(columns=['Latitude', 'Longitude'])
# Extract data

taste = (df.loc[:, "Body":"Floral"])
df['OverallPoint'] = taste.sum(numeric_only=True, axis=1)
df['Flavor'] = taste[taste == 3].count(axis=1) + taste[taste == 4].count(axis=1)

# Charts
fig1 = px.scatter(df.sort_values(by=['OverallPoint'], ascending=True), x='Longitude', y='Latitude', color='Flavor',
                  size='OverallPoint', hover_name="Distillery", color_continuous_scale=px.colors.sequential.YlOrBr,
                  height=600, width=600, title='Geographic location of Whisky Distillery')

fig2 = px.bar(df.sort_values(by=['OverallPoint'], ascending=False).head(10),
              x='Distillery', y="OverallPoint", hover_data=['Sweetness', 'Smoky'],
              color='OverallPoint', title='Top well rounded Scotch Whisky')

character = pd.DataFrame(
    {'character': taste.keys(), 'points': taste.mean()}
)
character = character.sort_values(by=['points'], ascending=True)
fig3 = px.pie(character, values='points', names='character', color_discrete_sequence=px.colors.sequential.Inferno,
              title='Whisky Characteristic')

# Number 4
df['SmokePoint'] = taste.iloc[:, [0, 1, 2]].mean(numeric_only=True, axis=1)
ranking = df.sort_values(by=['OverallPoint', 'SmokePoint'], ascending=False).head(50)

fig4 = px.scatter(ranking, x="OverallPoint", y="SmokePoint",
                  size="Flavor", color="Smoky", hover_name="Distillery",
                  color_continuous_scale=px.colors.sequential.YlOrBr,
                  size_max=60, title="Smoke vs Well-rounded Flavor")

# Number 5
fig5 = make_subplots(rows=1, cols=3, specs=[[{'type': 'polar'}] * 3] * 1)

fig5.add_trace(go.Scatterpolar(
    name="Aberlour",
    r=[3, 3, 1, 0, 0, 4, 3, 2, 2, 3, 3, 2],
    theta=["Body", "Sweetness", "Smoky", "Medicinal", "Tobacco", "Honey", "Spicy", "Winey", "Nutty", "Malty", "Fruity",
           "Floral"],
    fillcolor='orange', connectgaps=True),
    row=1, col=3
)
fig5.add_trace(go.Scatterpolar(
    name="Laphroig",
    r=[4, 2, 4, 4, 1, 0, 0, 1, 1, 1, 0, 0],
    theta=["Body", "Sweetness", "Smoky", "Medicinal", "Tobacco", "Honey", "Spicy", "Winey", "Nutty", "Malty", "Fruity",
           "Floral"],
    fillcolor='green', connectgaps=True),
    row=1, col=1
)

fig5.add_trace(go.Scatterpolar(
    name="Talisker",
    r=[4, 2, 3, 3, 0, 1, 3, 0, 1, 2, 2, 0],
    theta=["Body", "Sweetness", "Smoky", "Medicinal", "Tobacco", "Honey", "Spicy", "Winey", "Nutty", "Malty", "Fruity",
           "Floral"],
    fillcolor='blue', connectgaps=True),
    row=1, col=2
)

fig5.update_traces(fill='toself')
fig5.update_layout(title_text="Closer look at the taste of our top 3 choice")


# Layout

app.layout = html.Div(children=[
    html.H2(children='Whisky Catalog'),

    html.Div(children='''
        The geographic location of Whisky Distillery, it show the center Highland area is specialize at making
        whisky with mixed strong flavor, with exception of Talisker on the south getting 4 point of Flavor
    '''),
    dcc.Graph(
        id='The Whisky Map',
        figure=fig1
    ),

    html.Div(children='''
        
    '''),
    dcc.Graph(
        id='Whisky Character',
        figure=fig2
    ),
    html.Div(children='''
        What do you taste when you drink a Whisky: It is a well rounded drink isn't it!
    '''),
    dcc.Graph(
        id='Whisky Character 3',
        figure=fig3
    ),
    html.Div(children='''
       Now we want to have information about Smoky Whisky, which have smoke flavor but really hard to make and
       it has less of other flavor, which lead to lower Overall Rating than the Well Rounded-Whisky
   '''),
    dcc.Graph(
        id='Whisky Character 4',
        figure=fig4
    ),
    html.Div(children='''
       So the best Smoke Whisky is Laphroig\t
       Best Rounded Whisky: Aberlour \t
       Best mixture: Talisker
   '''),
    html.Div(children='''
       Here is the closer look at our 3 choice (the color is resembling the brand)
   '''),
    dcc.Graph(
        id='Whisky Character 5',
        figure=fig5
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
