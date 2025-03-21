import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="urllib3 v2 only supports OpenSSL 1.1.1+")
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load Data
df = pd.read_csv("./data/merged_data.csv")

# Get numeric columns (metrics)
numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Real-time 5G Network Metrics", style={'textAlign': 'center'}),

    # Dropdown to select metric
    html.Label("Select Metric:"),
    dcc.Dropdown(
        id='metric-dropdown',
        options=[{'label': col, 'value': col} for col in numeric_columns],
        value="Active UEs",  # Default
        multi=False
    ),

    # Graph
    dcc.Graph(id='live-update-graph'),

    # Refresh interval
    dcc.Interval(id='interval-component', interval=1000, n_intervals=4)  # Refresh every 5 sec
])

@app.callback(
    dash.Output('live-update-graph', 'figure'),
    [dash.Input('interval-component', 'n_intervals'),
     dash.Input('metric-dropdown', 'value')]
)
def update_graph(n, selected_metric):
    df = pd.read_csv("./data/merged_data.csv")

    # 🛠️ Ensure timestamp is parsed correctly and sorted
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp")  # Sort by time

    # 🛠️ Remove duplicate timestamps if any
    df = df.drop_duplicates(subset=["timestamp", selected_metric])

    # 🛠️ Fill missing values (optional)
    df[selected_metric] = df[selected_metric].ffill()

    # 🛠️ Plot single trace, ensuring a clean line
    fig = px.line(df, x="timestamp", y=selected_metric, title=f"{selected_metric} Over Time")
    fig.update_layout(xaxis_title="Time", yaxis_title=selected_metric, template="plotly_dark")

    return fig


if __name__ == '__main__':
    app.run(debug=True)
