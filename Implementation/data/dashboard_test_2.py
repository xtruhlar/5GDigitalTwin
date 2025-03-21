import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# ✅ Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=["/assets/style.css"])

# ✅ Dashboard Layout (Scalable & Responsive)
app.layout = html.Div([

    # 🔹 Title & Key Metrics Row
    html.Div([
        # Status (Up or Down)
        html.Div([html.H1("Digital Twin Dashboard", className="title")]),
        html.Div([html.H3("Active UEs"), html.H2(id="active-ues")], className="metric-box"),
        html.Div([html.H3("CPU Usage (Open5GS)"), html.H2(id="cpu-usage")], className="metric-box"),
        html.Div([html.H3("Network Traffic (kbps)"), html.H2(id="net-traffic")], className="metric-box"),
    ], className="metrics-container"),

        # 🔹 Time Window Selection
    html.Div([
        html.Label("Select Time Window:"),
        dcc.Dropdown(
            id="time-window",
            options=[
                {"label": "Last 1 Minute", "value": 60},
                {"label": "Last 10 Minutes", "value": 600},
                {"label": "Last 30 Minutes", "value": 1800},
                {"label": "Last 1 Hour", "value": 3600},
                {"label": "Last 12 Hours", "value": 43200},
                {"label": "Last 24 Hours", "value": 86400},
                {"label": "Last Week", "value": 604800}
            ],
            value=600,  # Default to last 10 minutes
            clearable=False
        )
    ], className="time-selector"),
    
    # 🔹 Dynamic Graph Grid
    html.Div([
        html.Div(dcc.Graph(id='graph-ues', config={'displayModeBar': False}), className="graph-box"),
        html.Div(dcc.Graph(id='graph-cpu', config={'displayModeBar': False}), className="graph-box"),
        html.Div(dcc.Graph(id='graph-net-in', config={'displayModeBar': False}), className="graph-box"),
        html.Div(dcc.Graph(id='graph-net-out', config={'displayModeBar': False}), className="graph-box"),
        # html.Div(dcc.Graph(id='graph-snr', config={'displayModeBar': False}), className="graph-box"),
        # html.Div(dcc.Graph(id='graph-cqi', config={'displayModeBar': False}), className="graph-box"),
    ], className="graph-container"),  

    dcc.Interval(id='interval-component', interval=3000, n_intervals=0)
])

# ✅ Update Graphs & Metrics
@app.callback([
     Output('active-ues', 'children'),
     Output('cpu-usage', 'children'),
     Output('net-traffic', 'children'),
     Output('graph-ues', 'figure'),
     Output('graph-cpu', 'figure'),
     Output('graph-net-in', 'figure'),
     Output('graph-net-out', 'figure'),
    #  Output('graph-snr', 'figure'),
    #  Output('graph-cqi', 'figure')
    ],
    [Input('interval-component', 'n_intervals'),
     Input('time-window', 'value')]
     )


def update_graphs(n, time_window):
    df = pd.read_csv("./data/merged_data.csv")

    # 🛠️ Ensure timestamp is parsed correctly and sorted
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp")  # Sort by time

    # 🛠️ Apply Time Window Filter
    now = df["timestamp"].max()
    df = df[df["timestamp"] >= now - pd.Timedelta(seconds=time_window)]

    # 🛠️ Handle Duplicates (Remove same timestamps with different values)
    for metric in ["Active UEs", "CPU Usage (Open5GS)", "Network Traffic In (kbps)", "Network Traffic Out (kbps)"]:
        if metric in df.columns:
            df = df.drop_duplicates(subset=["timestamp", metric])  # Keep the latest data

    # 🛠️ Fill missing values using forward fill method
    df = df.ffill()

    # 🔹 Extract Latest Values
    latest_ues = df["Active UEs"].dropna().values[-1] if "Active UEs" in df else 0
    latest_cpu = df["CPU Usage (Open5GS)"].dropna().values[-1] if "CPU Usage (Open5GS)" in df else 0
    latest_net = df["Network Traffic In (kbps)"].dropna().values[-1] if "Network Traffic In (kbps)" in df else 0


    # ✅ Generate Graphs (Clean & Scalable)
    def create_figure(y, title):
        fig = px.line(df, x="timestamp", y=y, title=title)

        # Ensure Graph Moves Dynamically
        fig.update_xaxes(range=[df["timestamp"].min(), df["timestamp"].max()])  

        # Set text color to white
        fig.update_layout(font_color="white", margin=dict(l=10, r=10, t=40, b=10),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          xaxis=dict(showgrid=True, zeroline=False, showticklabels=True),
                          yaxis=dict(showgrid=True, zeroline=False, showticklabels=True),
                          height=242)  # Adaptive height
        return fig

    return latest_ues, f"{latest_cpu:.2f}%", f"{latest_net:.2f} kbps", \
           create_figure("Active UEs", "Active UEs Over Time"), \
           create_figure("CPU Usage (Open5GS)", "CPU Usage (Open5GS) Over Time"), \
           create_figure("Network Traffic In (kbps)", "Network Traffic In (kbps) Over Time"), \
           create_figure("Network Traffic Out (kbps)", "Network Traffic Out (kbps) Over Time")

if __name__ == '__main__':
    app.run(debug=False, port=8050)
