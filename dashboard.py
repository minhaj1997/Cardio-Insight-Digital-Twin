import dash
from dash import dcc, html, callback_context, dash_table, State
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pandas as pd
from patient_service import get_latest_patient, fetch_all_patients, fetch_patient_data_by_id


class Dashboard:
    def __init__(self, trainer, clustertrainer):
        self.app = dash.Dash(__name__, suppress_callback_exceptions=True)
        self.app.index_string = '''
        <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <title>{%title%}</title>
                {%favicon%}
                {%css%}
                <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
                <style>
                @keyframes blink {
                    0% { opacity: 1; }
                    50% { opacity: 0; }
                    100% { opacity: 1; }
                }
                body {
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    margin: 0;
                    padding: 0;
                }
                .blinking {
                    animation: blink 1s infinite;
                    color: #e74c3c;
                    font-size: 15px;
                    padding: 10px;
                    border-radius: 5px;
                    background-color: rgba(231, 76, 60, 0.1);
                    margin: 5px 0;
                }
                .nav-link {
                    transition: all 0.3s ease;
                    padding: 10px 20px;
                    border-radius: 5px;
                    background-color: #ffffff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }
                .nav-link:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                }
                .dashboard-container {
                    background-color: rgba(255, 255, 255, 0.9);
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    padding: 20px;
                    margin: 20px;
                }
                .graph-container {
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    padding: 15px;
                    margin: 10px 0;
                    transition: all 0.3s ease;
                }
                .graph-container:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                }
                .page-title {
                    color: #2c3e50;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
                    margin-bottom: 30px;
                }
                </style>
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
        '''
        self.trainer = trainer
        self.clustertrainer = clustertrainer


    def layout(self):
        
        self.app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            dcc.Store(id='current-patient-data'),
            html.Div(id='page-content')
        ])

        
        
    def navigation_layout(self):
        return html.Div([
            dcc.Link('View Latest Patient Insights', href='/digital-twin',
                     className='nav-link',
                     style={
                         'marginRight': '20px',
                         'textDecoration': 'none',
                         'color': '#2980b9',
                         'fontSize': '18px',
                         'fontWeight': '500'
                     }),
            dcc.Link('List of Past Patients', href='/past-patients',
                     className='nav-link',
                     style={
                         'textDecoration': 'none',
                         'color': '#2980b9',
                         'fontSize': '18px',
                         'fontWeight': '500'
                     })
        ], style={'textAlign': 'center', 'marginTop': '30px', 'marginBottom': '30px'})
        
    
    def digital_twin_layout(self):
        return html.Div(
            className='dashboard-container',
            style={'padding': '30px'},
            children=[
            self.navigation_layout(),
            html.H1(
                children='Cardio Insight Digital Twin',
                className='page-title',
                style={
                    'textAlign': 'center',
                    'fontSize': '2.5em',
                    'fontWeight': '600',
                    'color': '#2c3e50',
                    'marginBottom': '40px'
                }
            ),
            html.H2(
                id='patient-name-display',
                style={
                    'textAlign': 'center',
                    'color': '#2980b9',
                    'fontSize': '1.8em',
                    'fontWeight': '500',
                    'marginBottom': '40px'
                }
            ),

            # Main content container
            html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'gap': '30px'}, children=[
                # Left column
                html.Div(style={'flex': '1'}, children=[
                    html.Div([
                        html.H3('Metabolic Syndrome Risk Assessment', 
                               style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
                        dcc.Graph(id='risk-gauge')
                    ], className='graph-container', style={'backgroundColor': '#f8f9fa', 'border': '1px solid #e9ecef'}),
                    
                    html.Div([
                        html.H3('Key Health Indicators Trend', 
                               style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
                        
                        # Health Alerts Section
                        html.Div([
                            html.H4('Health Alerts', 
                                   style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '10px'}),
                            html.Div(id='risk-monitoring-text', 
                                    style={'maxHeight': '150px', 'overflow': 'auto', 'padding': '15px'})
                        ], style={'marginBottom': '20px', 'borderBottom': '1px solid #e9ecef', 'paddingBottom': '10px'}),
                        
                        dcc.Graph(id='risk-monitoring-graph')
                    ], className='graph-container', style={'backgroundColor': '#f8f9fa', 'border': '1px solid #e9ecef'}),
                    
                    dcc.Interval(id='interval-update', interval=1000, n_intervals=0),
                ]),
                
                # Right column
                html.Div(style={'flex': '1'}, children=[
                    html.Div([
                        html.H3('Risk Factor Analysis', 
                               style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
                        dcc.Graph(id='feature-importance-graph')
                    ], className='graph-container', style={'backgroundColor': '#f8f9fa', 'border': '1px solid #e9ecef'}),
                    
                    html.Div([
                        html.H3('Risk Category', 
                               style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
                        html.Div(id='cluster-text', 
                                style={'maxHeight': '100px', 'overflow': 'auto', 'padding': '15px'})
                    ], className='graph-container', style={'backgroundColor': '#f8f9fa', 'border': '1px solid #e9ecef'}),
                    
                    html.Div([
                        html.H3('Patient Health Metrics', 
                               style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
                        dcc.Graph(id='cluster-graph')
                    ], className='graph-container', style={'backgroundColor': '#f8f9fa', 'border': '1px solid #e9ecef'}),
                    
                    dcc.Interval(id='interval-update2', interval=1000, n_intervals=0),
                ]),
            ]),
        ])
    
    def past_patients_layout(self):
        patient_data = fetch_all_patients()

        data = [{
            "Name": patient.name,
            "Age": patient.age,
            "Waist Circumference": patient.waist_circ,
            "BMI": patient.bmi,
            "Blood Glucose": patient.blood_glucose,
            "HDL": patient.hdl,
            "Triglycerides": patient.triglycerides,
            "Created At": patient.created_at.strftime("%Y-%m-%d %H:%M:%S") if patient.created_at else ""
        } for patient in patient_data]
        
        data = sorted(data, key=lambda x: x["Created At"], reverse=True)
    
        return html.Div([
            self.navigation_layout(),
            html.H1('List of Past Patients',
                   className='page-title',
                   style={'textAlign': 'center', 'fontSize': '2.5em', 'fontWeight': '600'}),
            html.Div([
                dash_table.DataTable(
                    id='patient-table',
                    columns=[
                        {"name": "Name", "id": "Name"},
                        {"name": "Age", "id": "Age"},
                        {"name": "Waist Circumference", "id": "Waist Circumference"},
                        {"name": "BMI", "id": "BMI"},
                        {"name": "Blood Glucose", "id": "Blood Glucose"},
                        {"name": "HDL", "id": "HDL"},
                        {"name": "Triglycerides", "id": "Triglycerides"},
                        {"name": "Created At", "id": "Created At"}
                    ],
                    data=data,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    sort_by=[{"column_id": "Created At", "direction": "desc"}],
                    page_action="native",
                    page_current=0,
                    page_size=10,
                    style_table={
                        'overflowX': 'auto',
                        'backgroundColor': 'white',
                        'border': '1px solid #ddd',
                        'borderRadius': '10px',
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'
                    },
                    style_cell={
                        'minWidth': '80px',
                        'width': '100px',
                        'maxWidth': '180px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'textAlign': 'center',
                        'padding': '12px 8px',
                        'fontFamily': "'Poppins', sans-serif"
                    },
                    style_header={
                        'backgroundColor': '#2980b9',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'textAlign': 'center',
                        'fontSize': '14px',
                        'padding': '12px 8px'
                    },
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f8f9fa'
                        },
                        {
                            'if': {'state': 'selected'},
                            'backgroundColor': '#e3f2fd',
                            'border': '1px solid #2980b9'
                        }
                    ],
                    row_selectable='single',
                )
            ], className='dashboard-container')
        ], style={'maxWidth': '1400px', 'margin': 'auto', 'padding': '20px'})


    def add_callbacks(self):
        @self.app.callback(
            [Output('page-content', 'children'),
             Output('current-patient-data', 'data')],
            [Input('url', 'pathname')]
        )
        def display_page(pathname):
            if pathname.startswith('/patient/'):
                patient_id = int(pathname.split('/')[-1])  # Extract the patient ID from the URL
                patient_data = fetch_patient_data_by_id(patient_id)
                if patient_data:
                    # Create a dictionary with the patient data
                    patient_dict = {
                        'age': patient_data.age,
                        'waist_circ': patient_data.waist_circ,
                        'bmi': patient_data.bmi,
                        'blood_glucose': patient_data.blood_glucose,
                        'hdl': patient_data.hdl,
                        'triglycerides': patient_data.triglycerides,
                        'name': patient_data.name
                    }
                    return self.digital_twin_layout(), patient_dict
                else:
                    return html.Div([
                        html.H1("Patient not found"),
                        self.navigation_layout()
                    ]), None
            elif pathname == '/digital-twin':
                latest_patient = get_latest_patient()
                if latest_patient:
                    patient_dict = {
                        'age': latest_patient.age,
                        'waist_circ': latest_patient.waist_circ,
                        'bmi': latest_patient.bmi,
                        'blood_glucose': latest_patient.blood_glucose,
                        'hdl': latest_patient.hdl,
                        'triglycerides': latest_patient.triglycerides,
                        'name': latest_patient.name
                    }
                    return self.digital_twin_layout(), patient_dict
                return self.digital_twin_layout(), None
            elif pathname == '/past-patients':
                return self.past_patients_layout(), None
            else:
                return html.Div([
                    html.H1("Welcome to the Main Page"),
                    self.navigation_layout()
                ]), None
        
        @self.app.callback(
            Output('patient-name-display', 'children'),
            [Input('interval-update', 'n_intervals'),
             Input('current-patient-data', 'data')]
        )
        def update_patient_name(n, patient_data):
            if patient_data:
                return f"Patient Name: {patient_data['name']}"
            else:
                latest_patient = get_latest_patient()
                if latest_patient:
                    return f"Patient Name: {latest_patient['name']}"
                else:
                    return "No patient data available"
            
        @self.app.callback(
            Output('url', 'pathname'),
            Input('patient-table', 'selected_rows'),
            State('patient-table', 'data')
        )
        def update_url_on_row_select(selected_rows, rows):
            if selected_rows:
                # Get the selected patient's name
                selected_name = rows[selected_rows[0]]['Name']
                # Find the patient with this name in the database
                patient_data = fetch_all_patients()
                for patient in patient_data:
                    if patient.name == selected_name:
                        return f'/patient/{patient.id}'
            return dash.no_update
        
        @self.app.callback(
            dash.dependencies.Output('risk-gauge', 'figure'),
            [dash.dependencies.Input('interval-update', 'n_intervals'),
             Input('current-patient-data', 'data')]
        )
        def update_risk_gauge(n_intervals, patient_data):
            if patient_data:
                patient_data_array = [
                    patient_data['age'],
                    patient_data['waist_circ'],
                    patient_data['bmi'],
                    patient_data['blood_glucose'],
                    patient_data['hdl'],
                    patient_data['triglycerides']
                ]
            else:
                latest_patient = get_latest_patient()
                if latest_patient:
                    patient_data_array = [
                        latest_patient['age'],
                        latest_patient['waist_circ'],
                        latest_patient['bmi'],
                        latest_patient['blood_glucose'],
                        latest_patient['hdl'],
                        latest_patient['triglycerides']
                    ]
                else:
                    return go.Figure()

            patient_data_array = np.array([patient_data_array], dtype='float32')
            probability = self.trainer.model.predict_proba(patient_data_array)[0][1] * 100

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probability,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Risk Level", 'font': {'size': 24, 'color': '#2c3e50'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#2c3e50"},
                    'bar': {'color': "#2980b9"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "#2c3e50",
                    'steps': [
                        {'range': [0, 25], 'color': "#2ecc71"},  # Green
                        {'range': [25, 75], 'color': "#f1c40f"},  # Yellow
                        {'range': [75, 100], 'color': "#e74c3c"}  # Red
                    ],
                }
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=60, b=10),
                height=300
            )
            return fig
        
        @self.app.callback(
            Output('risk-monitoring-text', 'children'),
            [Input('interval-update', 'n_intervals'),
             Input('current-patient-data', 'data')]
        )
        def update_health_alerts(n, patient_data):
            if patient_data:
                patient_data_array = [
                    patient_data['age'],
                    patient_data['waist_circ'],
                    patient_data['bmi'],
                    patient_data['blood_glucose'],
                    patient_data['hdl'],
                    patient_data['triglycerides']
                ]
            else:
                latest_patient = get_latest_patient()
                if latest_patient:
                    patient_data_array = [
                        latest_patient['age'],
                        latest_patient['waist_circ'],
                        latest_patient['bmi'],
                        latest_patient['blood_glucose'],
                        latest_patient['hdl'],
                        latest_patient['triglycerides']
                    ]
                else:
                    return html.Div()

            # Define thresholds for health alerts
            thresholds = {
                'BloodGlucose': 126,  # higher than this is considered diabetic
                'HDL': 40,            # lower than this is considered at risk for heart disease
                'Triglycerides': 200  # higher than this is considered high
            }

            alerts = []
            
            # Check blood glucose
            if patient_data_array[3] > thresholds['BloodGlucose']:
                value = patient_data_array[3]
                alerts.append(html.Div([
                    html.I(className="fas fa-exclamation-triangle", style={'color': '#e74c3c', 'marginRight': '10px'}),
                    f"High Blood Glucose Alert: {value:.2f} mg/dL (Normal range: < 126 mg/dL)"
                ], className='blinking'))
                
            # Check HDL
            if patient_data_array[4] < thresholds['HDL']:
                value = patient_data_array[4]
                alerts.append(html.Div([
                    html.I(className="fas fa-exclamation-triangle", style={'color': '#e74c3c', 'marginRight': '10px'}),
                    f"Low HDL Alert: {value:.2f} mg/dL (Normal range: > 40 mg/dL)"
                ], className='blinking'))
                
            # Check triglycerides
            if patient_data_array[5] > thresholds['Triglycerides']:
                value = patient_data_array[5]
                alerts.append(html.Div([
                    html.I(className="fas fa-exclamation-triangle", style={'color': '#e74c3c', 'marginRight': '10px'}),
                    f"High Triglycerides Alert: {value:.2f} mg/dL (Normal range: < 200 mg/dL)"
                ], className='blinking'))
            
            if not alerts:
                return html.Div([
                    html.I(className="fas fa-check-circle", style={'color': '#2ecc71', 'marginRight': '10px'}),
                    "No health alerts at this time. All indicators are within normal ranges."
                ], style={'color': '#2ecc71', 'fontWeight': 'bold'})
                
            return html.Div(alerts)
            
        @self.app.callback(
             Output('risk-monitoring-graph', 'figure'),
             Input('interval-update', 'n_intervals'),
             Input('current-patient-data', 'data')
         )
        def update_risk_monitoring(n, patient_data):
            if patient_data:
                patient_data_array = [
                    patient_data['age'],
                    patient_data['waist_circ'],
                    patient_data['bmi'],
                    patient_data['blood_glucose'],
                    patient_data['hdl'],
                    patient_data['triglycerides']
                ]
            else:
                latest_patient = get_latest_patient()
                if latest_patient:
                    patient_data_array = [
                        latest_patient['age'],
                        latest_patient['waist_circ'],
                        latest_patient['bmi'],
                        latest_patient['blood_glucose'],
                        latest_patient['hdl'],
                        latest_patient['triglycerides']
                    ]
                else:
                    return go.Figure()

            fig = go.Figure()
            metrics = ['BloodGlucose', 'HDL', 'Triglycerides']
            metric_indices = [3, 4, 5]

            for i, metric in enumerate(metrics):
                value = patient_data_array[metric_indices[i]]
                y_values = [value] * 10

                fig.add_trace(go.Scatter(
                    y=y_values,
                    mode='lines+markers',
                    name=metric
                ))

            fig.update_layout(
                title={
                    
                    'font': {
                        'family': 'Times New Roman, sans-serif',
                        'size': 20,
                        'color': 'black'
                    }
                },
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
            )
            
            return fig
        
        @self.app.callback(
            [Output('cluster-text', 'children'),
             Output('cluster-graph', 'figure')],
            [Input('interval-update2', 'n_intervals'),
             Input('current-patient-data', 'data')]
        )
        def update_cluster(n, patient_data):
            if patient_data:
                patient_data_array = [
                    patient_data['age'],
                    patient_data['waist_circ'],
                    patient_data['bmi'],
                    patient_data['blood_glucose'],
                    patient_data['hdl'],
                    patient_data['triglycerides']
                ]
            else:
                latest_patient = get_latest_patient()
                if latest_patient:
                    patient_data_array = [
                        latest_patient['age'],
                        latest_patient['waist_circ'],
                        latest_patient['bmi'],
                        latest_patient['blood_glucose'],
                        latest_patient['hdl'],
                        latest_patient['triglycerides']
                    ]
                else:
                    return html.Div(), go.Figure()

            patient_df = pd.DataFrame([patient_data_array], columns=['age', 'waist_circ', 'bmi', 'blood_glucose', 'hdl', 'triglycerides'])
            cluster = self.clustertrainer.predict(patient_df)[0]

            cluster_descriptions = {
                0: "Lower risk",
                1: "Moderate risk",
                2: "Higher risk"
            }

            cluster_colors = {0: '#2ecc71', 1: '#f1c40f', 2: '#e74c3c'}  # Green, Yellow, Red

            description = f"Risk Category: {cluster_descriptions[cluster]}"
            color = cluster_colors[cluster]

            styled_description = html.Div(
                [html.P(description, style={'color': color})],
                style={'font-weight': 'bold', 'margin': '20px', 'font-size':'20px', 'text-align': 'center'}
            )

            # Create bar chart for metrics
            metrics = ['Age', 'Waist\nCirc', 'BMI', 'Blood\nGlucose', 'HDL', 'Triglycerides']
            values = patient_data_array

            fig = go.Figure(data=[
                go.Bar(
                    x=metrics,
                    y=values,
                    marker_color=color,
                    text=values,
                    textposition='auto',
                )
            ])

            fig.update_layout(
                title={
                    
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 16, 'color': '#2c3e50'}
                },
                yaxis_title="Values",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=60, b=10),
                height=300,
                font={'color': '#2c3e50'}
            )

            return styled_description, fig
        
        @self.app.callback(
            Output('feature-importance-graph', 'figure'),
            [Input('interval-update2', 'n_intervals'),
             Input('current-patient-data', 'data')]
        )
        def update_feature_importance(n, patient_data):
            if patient_data:
                patient_data_array = [
                    patient_data['age'],
                    patient_data['waist_circ'],
                    patient_data['bmi'],
                    patient_data['blood_glucose'],
                    patient_data['hdl'],
                    patient_data['triglycerides']
                ]
            else:
                latest_patient = get_latest_patient()
                if latest_patient:
                    patient_data_array = [
                        latest_patient['age'],
                        latest_patient['waist_circ'],
                        latest_patient['bmi'],
                        latest_patient['blood_glucose'],
                        latest_patient['hdl'],
                        latest_patient['triglycerides']
                    ]
                else:
                    return go.Figure()

            # Get feature importances from the model
            base_importances = self.trainer.model.feature_importances_

            # Define feature names and their corresponding maximum values
            feature_info = [
                {'name': 'Age', 'display_name': 'Age', 'max_value': 100},
                {'name': 'Waist Circumference', 'display_name': 'Waist\nCircumference', 'max_value': 150},
                {'name': 'BMI', 'display_name': 'BMI', 'max_value': 50},
                {'name': 'Blood Glucose', 'display_name': 'Blood\nGlucose', 'max_value': 200},
                {'name': 'HDL', 'display_name': 'HDL\nCholesterol', 'max_value': 100},
                {'name': 'Triglycerides', 'display_name': 'Triglycerides', 'max_value': 300}
            ]
            
            # Extract lists for processing
            max_values = [info['max_value'] for info in feature_info]
            display_names = [info['display_name'] for info in feature_info]
            
            # Normalize patient values relative to typical maximum values
            normalized_values = [min(1.0, value / max_val) for value, max_val in zip(patient_data_array, max_values)]
            
            # Calculate relative importance and convert to percentages
            relative_importances = [base_imp * norm_val * 100 for base_imp, norm_val in zip(base_importances, normalized_values)]
            
            # Create DataFrame for visualization
            df_feature_importances = pd.DataFrame({
                'Features': display_names,
                'Importance': relative_importances,
                'Values': patient_data_array
            })
            
            # Sort by relative importance
            df_feature_importances = df_feature_importances.sort_values('Importance', ascending=True)
            
            # Create the bar chart
            fig = go.Figure(go.Bar(
                x=df_feature_importances['Importance'],
                y=df_feature_importances['Features'],
                orientation='h',
                marker_color='#3498db',
                text=[f'Value: {val:.1f} | Impact: {imp:.1f}%' 
                      for val, imp in zip(df_feature_importances['Values'], 
                                        df_feature_importances['Importance'])],
                textposition='auto',
            ))
            
            fig.update_layout(
                title={
                    
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 16, 'color': '#2c3e50'}
                },
                xaxis_title="Relative Impact (%)",
                yaxis_title="Health Factors",
                yaxis={'categoryorder':'total ascending'},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=60, b=10),
                height=300,
                font={'color': '#2c3e50'},
                xaxis=dict(
                    ticksuffix="%",
                    range=[0, max(df_feature_importances['Importance']) * 1.1]  # Add 10% padding
                )
            )
            return fig
        
    def run(self):
        self.app.run_server(host='0.0.0.0', port=8050, debug=True)