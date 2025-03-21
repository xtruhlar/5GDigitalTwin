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
        # Logo from assets folder logo.png
        # html.Img(src="/assets/logo.png", className="title"),
        html.Div([html.H3("Active UEs"), html.H2(id="active-ues")], className="metric-box"),
        html.Div([html.H3("CPU Usage (Open5GS)"), html.H2(id="cpu-usage")], className="metric-box"),
        html.Div([html.H3("Network Traffic (kbps)"), html.H2(id="net-traffic")], className="metric-box"),
    ], className="metrics-container"),
    
    # 🔹 Dynamic Graph Grid
    html.Div([
        html.Div(dcc.Graph(id='graph-ues', config={'displayModeBar': False}), className="graph-box"),
        html.Div(dcc.Graph(id='graph-cpu', config={'displayModeBar': False}), className="graph-box"),
        html.Div(dcc.Graph(id='graph-net-in', config={'displayModeBar': False}), className="graph-box"),
        html.Div(dcc.Graph(id='graph-net-out', config={'displayModeBar': False}), className="graph-box"),
        html.Div(dcc.Graph(id='graph-snr', config={'displayModeBar': False}), className="graph-box"),
        html.Div(dcc.Graph(id='graph-cqi', config={'displayModeBar': False}), className="graph-box"),
    ], className="graph-container"),  

    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
])

# ✅ Update Graphs & Metrics
@app.callback(
    [Output('active-ues', 'children'),
     Output('cpu-usage', 'children'),
     Output('net-traffic', 'children'),
     Output('graph-ues', 'figure'),
     Output('graph-cpu', 'figure'),
     Output('graph-net-in', 'figure'),
     Output('graph-net-out', 'figure'),
     Output('graph-snr', 'figure'),
     Output('graph-cqi', 'figure')],
    Input('interval-component', 'n_intervals')
)
def update_graphs(n):
    df = pd.read_csv("./data/merged_data.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp")

    # 🔹 Extract Latest Values
    latest_ues = df["Active UEs"].dropna().values[-1] if "Active UEs" in df else 0
    latest_cpu = df["CPU Usage (Open5GS)"].dropna().values[-1] if "CPU Usage (Open5GS)" in df else 0
    latest_net = df["Network Traffic In (kbps)"].dropna().values[-1] if "Network Traffic In (kbps)" in df else 0

    # ✅ Generate Graphs (Clean & Scalable)
    def create_figure(y, title):
        fig = px.line(df, x="timestamp", y=y, title=title)
        fig.update_layout(
            margin=dict(l=10, r=10, t=40, b=10),  
            paper_bgcolor="rgba(0,0,0,0)",  
            plot_bgcolor="rgba(0,0,0,0)",  
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=True),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=True),
            height=250,  # Adaptive height
        )
        return fig

    return latest_ues, f"{latest_cpu:.2f}%", f"{latest_net:.2f} kbps", \
           create_figure("Active UEs", "Active UEs Over Time"), \
           create_figure("CPU Usage (Open5GS)", "CPU Usage (Open5GS) Over Time"), \
           create_figure("Network Traffic In (kbps)", "Network Traffic In (kbps) Over Time"), \
           create_figure("Network Traffic Out (kbps)", "Network Traffic Out (kbps) Over Time"), \
           create_figure("Uplink SNR", "Uplink SNR Over Time") if "Uplink SNR" in df else px.line(), \
           create_figure("CQI", "CQI Over Time") if "CQI" in df else px.line()

if __name__ == '__main__':
    app.run(debug=True)
