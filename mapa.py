import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

#Autor: Cristobal Maestre Vaz
file_path = 'F1DriversDataset_Updated.csv' 
df = pd.read_csv(file_path)


def get_top_5_pilots(country, metric):
    pilots = df[df["Nationality"] == country].sort_values(by=metric, ascending=False)
    top_pilots = pilots.head(5)
    metric_label = metrics_labels[metric] 
    return "<br>".join([f"{row['Driver']} - {row[metric]} {metric_label.lower()}" for _, row in top_pilots.iterrows()])


metrics = {
    "Race_Wins": "Victorias",
    "Pole_Positions": "Poles",
    "Points": "Puntos",
    "Championships": "Campeonatos"
}

metrics_labels = {
    "Race_Wins": "Victorias",
    "Pole_Positions": "Poles",
    "Points": "Puntos",
    "Championships": "Campeonatos mundiales"
}

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Mapa Interactivo de Pilotos de Fórmula 1"),
    dcc.Dropdown(
        id="metric-dropdown",
        options=[{"label": label, "value": metric} for metric, label in metrics.items()],
        value="Race_Wins", 
        clearable=False,
    ),
    dcc.Graph(id="map-graph", style={"height": "800px"}),
])

@app.callback(
    Output("map-graph", "figure"),
    Input("metric-dropdown", "value")
)
def update_map(selected_metric):
    df["Top 5 Pilotos"] = df["Nationality"].apply(lambda country: get_top_5_pilots(country, selected_metric))
    
    country_data = df.groupby("Nationality").agg(
        Total_Value=(selected_metric, "sum"),
        Top_5_Pilotos=("Top 5 Pilotos", "first"),
    ).reset_index()

    fig = px.choropleth(
        country_data,
        locations="Nationality",
        locationmode="country names",
        color="Total_Value", 
        hover_name="Nationality",
        hover_data={
            "Total_Value": True,
            "Top_5_Pilotos": True
        },
        title=f"Top 5 Pilotos por {metrics[selected_metric]}",
        color_continuous_scale=px.colors.sequential.Plasma,
        height=800,
        width=1200,
    )

    fig.update_layout(
        coloraxis_colorbar=dict(
            title=metrics_labels[selected_metric]
        )
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
