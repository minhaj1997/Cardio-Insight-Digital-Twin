import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pandas as pd

class Dashboard:
    def __init__(self, trainer, clustertrainer):
        self.app = dash.Dash(__name__)
        self.trainer = trainer
        self.clustertrainer = clustertrainer

    def layout(self):
        self.app.layout = html.Div(
            style={'backgroundColor': '#FAF9F6', 'minHeight': '100vh'},
            children=[
            html.H1(children='Digital Twin for Human Heart'),

            # Row div with two columns
            html.Div(
                children=[
                # Left column div
                html.Div(children=[
                    dcc.Graph(id='risk-gauge'),
                    html.Div(id='risk-monitoring-text' ,style={'max-height': '100px', 'overflow': 'auto'}),
                    dcc.Graph(id='risk-monitoring-graph'),
                    dcc.Interval(
                        id='interval-update',
                        interval=2000,  # in milliseconds
                        n_intervals=0
                    ),
                ], style={'display': 'inline-block', 'width': '50%'}),  # The className defines the width of the column
                
                # Right column div
                html.Div(children=[
                    dcc.Graph(id='feature-importance-graph'),
                    html.Div(id='cluster-text', style={'max-height': '100px', 'overflow': 'auto'}),
                    dcc.Graph(id='cluster-graph'),
                    dcc.Interval(
                        id='interval-update2', 
                        interval=2000, 
                        n_intervals=0
                    ),
                ], style={'display': 'inline-block', 'width': '50%'}),
                
            ]),  
        ])


    def add_callbacks(self):
        @self.app.callback(
            dash.dependencies.Output('risk-gauge', 'figure'),
           [dash.dependencies.Input('interval-update', 'n_intervals')]
        )
        def update_risk_gauge(n_intervals):
            idx = np.random.randint(0, len(self.trainer.X_test))
            sample_data = self.trainer.X_test.iloc[idx].values.reshape(1, -1)
            
            # Predict the probability of Metabolic Syndrome
            probability = self.trainer.model.predict_proba(sample_data)[0][1] * 100  # Probability for the positive class
            
            # Create a gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probability,
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={'axis': {'range': [0, 100]},
                       'steps': [{'range': [0, 50], 'color': "lightgreen"},
                                 {'range': [50, 75], 'color': "yellow"},
                                 {'range': [75, 100], 'color': "red"}]
                      }))
            # Update the layout for the gauge chart
            fig.update_layout(
                title="Risk of Metabolic Syndrome leading to heart disease",
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the graph
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent background for the plot
            )
            
            return fig
        
        # Calculate the thresholds
        thresholds = {
            'BloodGlucose': 126,  # higher than this is considered diabetic
            'HDL': 40,            # lower than this is considered at risk for heart disease
            'Triglycerides': 200  # higher than this is considered high

        }

        @self.app.callback(
            Output('risk-monitoring-text', 'children'),
            Input('interval-update', 'n_intervals')
        )
        def update_metrics(n):
            
            sample_index = np.random.randint(0, len(self.trainer.X_test))
            sample_data = self.trainer.X_test.iloc[sample_index]
            
            # Generate alerts based on thresholds
            alerts = []
            if sample_data['BloodGlucose'] > thresholds['BloodGlucose']:
                value = sample_data['BloodGlucose'];
                alerts.append(f"High Blood Glucose Alert: {value:.2f}")
            if sample_data['HDL'] < thresholds['HDL']:
                value = sample_data['HDL'];
                alerts.append(f"Low HDL Alert: {value:.2f}")
            if sample_data['Triglycerides'] > thresholds['Triglycerides']:
                value = sample_data['Triglycerides'];
                alerts.append(f"High Triglycerides Alert: {value:.2f}")
         
            # Create HTML elements for each alert
            return html.Div([html.P(alert) for alert in alerts])

        @self.app.callback(
            Output('risk-monitoring-graph', 'figure'),
            Input('interval-update', 'n_intervals')
        )
        def update_risk_monitoring(n):

            # Select multiple random samples from X_test to create a small sequence
            sample_indices = np.random.choice(len(self.trainer.X_test), size=10, replace=False)
            sample_data = self.trainer.X_test.iloc[sample_indices]

            # Create the graph with subplots
            fig = go.Figure()
            metrics = ['BloodGlucose', 'HDL', 'Triglycerides']

            # Loop through each metric and plot it as a line
            for metric in metrics:
                fig.add_trace(go.Scatter(
                    y=sample_data[metric].values,  # Use .values to ensure it's in array form
                    mode='lines+markers',  # Include both lines and markers
                    name=metric
                ))
            
            # Update the layout for the gauge chart
            fig.update_layout(
                title="Risk Monitoring",
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the graph
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent background for the plot
            )
            
            return fig
        
        @self.app.callback(
            [Output('cluster-text', 'children'),
             Output('cluster-graph', 'figure')],
            [Input('interval-update2', 'n_intervals')]
        )
        def update_cluster(n):
            # Simulate incoming patient data
            idx = np.random.randint(0, len(self.trainer.X_test))
            sample_data = self.trainer.X_test.iloc[idx].values.reshape(1, -1)
            cluster = self.clustertrainer.kmeans.predict(sample_data)[0]
            
            # Define cluster characteristics based on your analysis
            cluster_descriptions = {
                0: "Lower risk",
                1: "Moderate risk",
                2: "Higher risk"
            }

            # Color map for clusters
            cluster_colors = {0: 'green', 1: 'gold', 2: 'red'}
            
            description = f"Cluster {cluster+1}: {cluster_descriptions[cluster]}"
            color = cluster_colors[cluster]

            # Update graph
            fig = go.Figure()
            metrics = ['BMI', 'Age', 'Waist Circ', 'HDL', 'Triglycerides']
            values = sample_data.flatten()
            fig.add_trace(go.Bar(x=metrics, y=values, marker_color=color))

            fig.update_layout(
                title="Current Health Metrics Snapshot",
                xaxis_title="Metrics",
                yaxis_title="Values",
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the graph
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent background for the plot
            )

            return description, fig
        
        @self.app.callback(
            Output('feature-importance-graph', 'figure'),
            [Input('interval-update2', 'n_intervals')]
        )
        def update_graph(n):
            selected_features = ['Age', 'WaistCirc', 'BMI', 'BloodGlucose', 'HDL', 'Triglycerides']
            feature_importances = self.trainer.model.feature_importances_

            df_feature_importances = pd.DataFrame({
                'Features': selected_features,
                'Importance': feature_importances
            })
            df_feature_importances = df_feature_importances.sort_values('Importance', ascending=False)
            fig = px.bar(df_feature_importances, y='Features', x='Importance', title='Feature Importance for Predicting Health Outcomes', orientation='h')
            fig.update_layout(
                yaxis={'categoryorder':'total ascending'},
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the graph
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent background for the plot
            )
            return fig
        
    def run(self):
        self.app.run_server(debug=True)