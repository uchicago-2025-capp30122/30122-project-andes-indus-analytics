from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv("data/data_pumas.csv")

app = Dash(__name__)

# 1) Define the layout with a parent Div using "display: flex"
app.layout = html.Div(
    style={'display': 'flex'},  # Makes children arrange horizontally
    children=[
        # 2) Left column: text and controls
        html.Div(
            style={'width': '50%', 'padding': '20px'}, 
            children=[
                html.H1(
                    "Understanding School Dropouts in Chicago",
                    style={'textAlign': 'center'}
                ),
                html.P(
                    "This is a paragraph with background info  "
                    ""
                ),
                html.Label("Select Year:"),
                dcc.Dropdown(
                    options=sorted(df['year'].unique()),
                    value=sorted(df['year'].unique())[0],
                    id='dropdown-year'
                ),
                html.P(
                    "story or problem we are tackling. "
                    "Use this space for any narrative or instructions."
                )
            ]
        ),

        # 3) Right column: the graphs
        html.Div(
            style={'width': '50%', 'padding': '20px'}, 
            children=[
                dcc.Graph(id='scatter-graph'),
                dcc.Graph(id='bar-graph')
            ]
        )
    ]
)

# 4) Callback that updates both graphs based on the selected year
@callback(
    Output('scatter-graph', 'figure'),
    Output('bar-graph', 'figure'),
    Input('dropdown-year', 'value')
)
def update_charts(selected_year):
    # Filter data for the selected year
    dff = df[df['year'] == selected_year]

    # First graph: scatter plot
    fig_scatter = px.scatter(
        dff,
        x='attendance_rate_high',
        y='robbery',
        title=f"Scatter Plot for Year {selected_year}"
    )

    # Second graph: bar chart, sorted by 'attendance_rate_high' descending
    dff_sorted = dff.sort_values('attendance_rate_high', ascending=False)
    fig_bar = px.bar(
        dff_sorted,
        x='puma',
        y='attendance_rate_high',
        title=f"Attendance rate for Year {selected_year} - highschool"
    )

    return fig_bar, fig_scatter

if __name__ == '__main__':
    app.run_server(debug=True)
