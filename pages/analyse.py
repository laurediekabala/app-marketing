# pages/analyse.py
import dash
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from utils import theme
from transformation import dataset, type_col
from dash.exceptions import PreventUpdate
import plotly.figure_factory as ff
from scipy.stats import chi2_contingency, kruskal, shapiro, jarque_bera, kstest

try:
    df = dataset()
except Exception as e:
    print(f"Erreur de chargement des données: {e}")
    df = pd.DataFrame({'error': [f'Impossible de charger les données: {e}']})

numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
options = [{"label": "tous", "value": "all"}] + [
    {"label": str(val), "value": val} for val in df["y"].dropna().unique()
]
filtr = [{"label": val, "value": val} for val in categorical_cols]
filtr_y = [{"label": str(val), "value": val} for val in df["y"].dropna().unique()]

GRAPH_CONFIG = {
    'responsive': True,
    'displayModeBar': True,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'displaylogo': False
}

GRAPH_STYLE = {
    'width': '100%',
    'minHeight': '300px'
}

modal_num = dbc.Modal([
    dbc.ModalHeader(
        dbc.ModalTitle("📊 Analyse Bivariée Numérique"),
        close_button=True
    ),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.Label("Variable X :", className="fw-bold small"),
                dcc.Dropdown(
                    id='bivariate-num-x',
                    options=[{'label': col, 'value': col} for col in numerical_cols],
                    value=numerical_cols[0] if numerical_cols else None,
                    className="mb-2"
                )
            ], xs=12, sm=12, md=4),
            dbc.Col([
                dbc.Label("Variable Y :", className="fw-bold small"),
                dcc.Dropdown(
                    id='bivariate-num-y',
                    options=[{'label': col, 'value': col} for col in numerical_cols],
                    value=numerical_cols[1] if len(numerical_cols) > 1 else numerical_cols[0],
                    className="mb-2"
                )
            ], xs=12, sm=12, md=4),
            dbc.Col([
                dbc.Label("Filtre :", className="fw-bold small"),
                dcc.Dropdown(
                    id='filtre',
                    options=filtr,
                    value=numerical_cols[0] if numerical_cols else None,
                    className="mb-2"
                )
            ], xs=12, sm=12, md=4)
        ]),
        html.Div(id='bivariate-num-plot', className="mt-3")
    ]),
], id="modal-bivariate-num", is_open=False, centered=True,
   fade=True, backdrop=True, size="xl", scrollable=True,
   className="modal-responsive")

modal_cat = dbc.Modal([
    dbc.ModalHeader(
        dbc.ModalTitle("📋 Analyse Bivariée Catégorielle"),
        close_button=True
    ),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.Label("Variable X :", className="fw-bold small"),
                dcc.Dropdown(
                    id='bivariate-cat-x',
                    options=[{'label': col, 'value': col} for col in categorical_cols],
                    value=categorical_cols[0] if categorical_cols else None,
                    className="mb-2"
                )
            ], xs=12, sm=6),
            dbc.Col([
                dbc.Label("Variable Y :", className="fw-bold small"),
                dcc.Dropdown(
                    id='bivariate-cat-y',
                    options=[{'label': col, 'value': col} for col in categorical_cols],
                    value=categorical_cols[1] if len(categorical_cols) > 1 else categorical_cols[0],
                    className="mb-2"
                )
            ], xs=12, sm=6),
        ]),
        html.Div(id='bivariate-cat-plot', className="mt-3")
    ]),
], id="modal-bivariate-cat", is_open=False, centered=True,
   fade=True, backdrop=True, size="xl", scrollable=True,
   className="modal-responsive")

modal_cat_num = dbc.Modal([
    dbc.ModalHeader(
        dbc.ModalTitle("🔀 Analyse Bivariée Num-Cat"),
        close_button=True
    ),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.Label("Variable numérique :", className="fw-bold small"),
                dcc.Dropdown(
                    id='bivariate-num-cat-x',
                    options=[{'label': col, 'value': col} for col in numerical_cols],
                    value=numerical_cols[0] if numerical_cols else None,
                    className="mb-2"
                )
            ], xs=12, sm=12, md=4),
            dbc.Col([
                dbc.Label("Variable catégorielle :", className="fw-bold small"),
                dcc.Dropdown(
                    id='bivariate-num-cat-y',
                    options=[{'label': col, 'value': col} for col in categorical_cols],
                    value=categorical_cols[1] if len(categorical_cols) > 1 else categorical_cols[0],
                    className="mb-2"
                )
            ], xs=12, sm=12, md=4),
            dbc.Col([
                dbc.Label("Filtre :", className="fw-bold small"),
                dcc.Dropdown(
                    id='bfiltre',
                    options=filtr,
                    value=categorical_cols[0] if categorical_cols else None,
                    className="mb-2"
                )
            ], xs=12, sm=12, md=4)
        ]),
        html.Div(id='bivariate-num-cat-plot', className="mt-3")
    ]),
], id="modal-bivariate-num_cat", is_open=False, centered=True,
   fade=True, backdrop=True, size="xl", scrollable=True,
   className="modal-responsive")

collapse_st = dbc.Collapse([
    dbc.Card([
        dbc.CardHeader(html.H5("📐 Test Statistique", className="mb-0")),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Variable X :", className="fw-bold small"),
                    dcc.Dropdown(
                        id='bivariate-num-x',
                        options=[{'label': col, 'value': col} for col in numerical_cols],
                        value=numerical_cols[0] if numerical_cols else None,
                        className="mb-2"
                    )
                ], xs=12, sm=6, md=4),
            ]),
            html.Div(id='test_stat', className="mt-3")
        ]),
    ], className="shadow-sm")
], id="collapse_stat", is_open=False)


def layout():
    return dbc.Container([
        html.H1("Page d'Analyse des Données", className="mb-3 mb-md-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Filtration :", className="fw-bold"),
                dcc.Dropdown(
                    id='filtration',
                    options=options,
                    value='all',
                    clearable=False
                ),
            ], xs=12, sm=8, md=6, lg=4, className="mb-3"),
        ]),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Button([
                        html.I(className="fas fa-chart-scatter me-1 d-none d-sm-inline"),
                        "Bivariée Numérique"
                    ], id="btn-bivariate-num", color="primary", size="sm"),
                    dbc.Button([
                        html.I(className="fas fa-table me-1 d-none d-sm-inline"),
                        "Bivariée Catégorielle"
                    ], id="btn-bivariate-cat", color="secondary", size="sm"),
                    dbc.Button([
                        html.I(className="fas fa-exchange-alt me-1 d-none d-sm-inline"),
                        "Num-Catégorielle"
                    ], id="btn-bivariate-num-cat", color="info", size="sm"),
                    dbc.Button([
                        html.I(className="fas fa-flask me-1 d-none d-sm-inline"),
                        "Test Statistique"
                    ], id="collap_st", color="warning", size="sm"),
                ], className="analysis-buttons mb-3")
            ], xs=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Spinner(html.Div(id="bivariate-num-container"), color="primary", type="grow"),
            ], xs=12, className="mb-3"),
            dbc.Col([
                dbc.Spinner(html.Div(id="bivariate-cat-container"), color="secondary", type="grow"),
            ], xs=12, className="mb-3"),
        ]),
        
        modal_num,
        modal_cat,
        modal_cat_num,
        collapse_st,
        
        dbc.Tabs([
            dbc.Tab(label="📊 Analyse Descriptive", tab_id="tab-descriptive"),
            dbc.Tab(label="📈 KPIs", tab_id="tab-kpi"),
        ], id="analyse-tabs", active_tab="tab-descriptive", className="mb-3 mb-md-4"),
        
        html.Div(id="tabs-content")
        
    ], fluid=True, className="py-3 py-md-4")


@callback(
    Output("modal-bivariate-num", "is_open"),
    Input("btn-bivariate-num", "n_clicks"),
    [State("modal-bivariate-num", "is_open"), State('theme-store', 'data')],
)
def update_bivariate_numeric(n, is_open, theme_value):
    if n:
        return not is_open
    return is_open


@callback(
    Output("modal-bivariate-cat", "is_open"),
    Input("btn-bivariate-cat", "n_clicks"),
    [State('modal-bivariate-cat', 'is_open'), State('theme-store', 'data')],
)
def update_bivariate_categorical(n, is_open, theme_value):
    if n:
        return not is_open
    return is_open


@callback(
    Output('bivariate-num-plot', 'children'),
    [Input('bivariate-num-x', 'value'),
     Input('bivariate-num-y', 'value'),
     Input('filtre', 'value')],
    State('theme-store', 'data')
)
def update_bivariate_num_plot(var_x, var_y, filtre, theme_value):
    if not var_x or not var_y:
        return dbc.Alert("Sélectionnez deux variables", color="info", className="text-center")
    template = theme.THEMES[theme_value]['plotly']
    fig = px.scatter(df, x=var_x, y=var_y,
                     title=f'Analyse Bivariée : {var_x} vs {var_y}',
                     color=filtre, template=template)
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20), autosize=True)
    return html.Div([dcc.Graph(figure=fig, config=GRAPH_CONFIG, style=GRAPH_STYLE)], className="graph-container")


@callback(
    Output('bivariate-cat-plot', 'children'),
    [Input('filtration', 'value'),
     Input('bivariate-cat-x', 'value'),
     Input('bivariate-cat-y', 'value')],
    State('theme-store', 'data')
)
def update_bivariate_cat_plot(filtration, var_x, var_y, theme_value):
    if not var_x or not var_y:
        return dbc.Alert("Sélectionnez deux variables", color="info", className="text-center")
    template = theme.THEMES[theme_value]['plotly']
    if filtration == "all":
        filtered_df = df
        contingency = pd.crosstab(filtered_df[var_x], filtered_df[var_y])
        stat = chi2_contingency(contingency, correction=True)[1]
        title = f'Contingence : {var_x} vs {var_y}\n(Tous — p-value : {stat:.4f})'
    else:
        filtered_df = df.loc[df['y'].isin([filtration])]
        status = "ayant souscrit" if filtration == 'yes' else "n'ayant pas souscrit"
        contingency = pd.crosstab(filtered_df[var_x], filtered_df[var_y])
        stat = chi2_contingency(contingency, correction=True)[1]
        title = f'Contingence : {var_x} vs {var_y}\n(Clients {status} — p-value : {stat:.4f})'
    fig = px.imshow(contingency, labels=dict(x=var_x, y=var_y, color="Fréquence"),
                    title=title, template=template)
    fig.update_layout(margin=dict(l=20, r=20, t=80, b=20), autosize=True)
    return html.Div([dcc.Graph(figure=fig, config=GRAPH_CONFIG, style=GRAPH_STYLE)], className="graph-container")


@callback(
    Output("modal-bivariate-num_cat", "is_open"),
    Input("btn-bivariate-num-cat", "n_clicks"),
    [State("modal-bivariate-num_cat", "is_open"), State('theme-store', 'data')],
)
def update_bivariate_numeric_cat(n, is_open, theme_value):
    if n:
        return not is_open
    return is_open


@callback(
    Output('bivariate-num-cat-plot', 'children'),
    [Input('bivariate-num-cat-x', 'value'),
     Input('bivariate-num-cat-y', 'value'),
     Input('bfiltre', 'value')],
    State('theme-store', 'data')
)
def update_bivariate_num_cat_plot(var_x, var_y, filtre, theme_value):
    if not var_x or not var_y:
        return dbc.Alert("Sélectionnez deux variables", color="info", className="text-center")
    template = theme.THEMES[theme_value]['plotly']
    fig = px.box(df, x=var_y, y=var_x,
                 labels=dict(x=var_x, y=var_y, color="Fréquence"),
                 title=f'Box Plot : {var_x} vs {var_y}',
                 color=filtre, template=template)
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20), autosize=True)
    return html.Div([dcc.Graph(figure=fig, config=GRAPH_CONFIG, style=GRAPH_STYLE)], className="graph-container")


@callback(
    Output("collapse_stat", "is_open"),
    Input("collap_st", "n_clicks"),
    [State("collapse_stat", "is_open"), State('theme-store', 'data')],
)
def update_test_statistique(n, is_open, theme_value):
    if n:
        return not is_open
    return is_open


@callback(
    Output('test_stat', 'children'),
    Input('bivariate-num-x', 'value'),
    State('theme-store', 'data')
)
def test_hypothse(var_x, theme_value):
    if not var_x:
        return dbc.Alert("Sélectionnez une variable", color="info", className="text-center")
    data_no = df.loc[df["y"] == "no"]
    data_yes = df.loc[df["y"] == "yes"]
    pvalue = kruskal(data_no[var_x], data_yes[var_x])[1]
    if pvalue < 0.05:
        return dbc.Alert([
            html.I(className="fas fa-check-circle me-2"),
            html.Strong("Différence significative"),
            html.Br(),
            html.Span(
                f"Il existe une différence significative selon {var_x} "
                f"entre les souscripteurs et les non-souscripteurs "
                f"(p-value = {round(pvalue, 4)})"
            )
        ], color="success", className="test-stat-result")
    else:
        return dbc.Alert([
            html.I(className="fas fa-times-circle me-2"),
            html.Strong("Pas de différence significative"),
            html.Br(),
            html.Span(
                f"Il n'existe pas de différence significative selon {var_x} "
                f"entre les souscripteurs et les non-souscripteurs "
                f"(p-value = {round(pvalue, 4)})"
            )
        ], color="warning", className="test-stat-result")


@callback(
    Output('tabs-content', 'children'),
    Input('analyse-tabs', 'active_tab')
)
def render_tab_content(active_tab):
    if active_tab == "tab-descriptive":
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Variable numérique :", className="fw-bold small"),
                    dcc.Dropdown(
                        id='numeric-var-dropdown',
                        options=[{'label': i, 'value': i} for i in numerical_cols],
                        value=numerical_cols[0] if numerical_cols else None
                    )
                ], xs=12, sm=6, className="mb-2"),
                dbc.Col([
                    dbc.Label("Variable catégorielle :", className="fw-bold small"),
                    dcc.Dropdown(
                        id='categorical-var-dropdown',
                        options=[{'label': i, 'value': i} for i in categorical_cols],
                        value=categorical_cols[0] if categorical_cols else None
                    )
                ], xs=12, sm=6, className="mb-2")
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Graph(id='histogram', config=GRAPH_CONFIG, style=GRAPH_STYLE)
                    ], className="graph-container")
                ], xs=12, lg=6, className="mb-3"),
                dbc.Col([
                    html.Div([
                        dcc.Graph(id='boxplot', config=GRAPH_CONFIG, style=GRAPH_STYLE)
                    ], className="graph-container")
                ], xs=12, lg=6, className="mb-3")
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Graph(id='bar-chart', config=GRAPH_CONFIG, style=GRAPH_STYLE)
                    ], className="graph-container")
                ], xs=12, className="mb-3")
            ]),
            html.H4("📊 Statistiques Descriptives", className="mt-3 mb-3"),
            html.Div(id='descriptive-stats-table', className="table-responsive-container")
        ])
    elif active_tab == "tab-kpi":
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Sélectionner un KPI :", className="fw-bold"),
                    dcc.Dropdown(
                        id='kpi-dropdown',
                        options=[
                            {'label': '📊 Taux de souscription global', 'value': 'subscription_rate'},
                            {'label': '👤 Distribution des âges', 'value': 'age_distribution'},
                            {'label': '💍 Répartition par statut marital', 'value': 'marital_status'}
                        ],
                        value='subscription_rate'
                    ),
                ], xs=12, sm=8, md=6, lg=4, className="mb-3"),
            ]),
            html.Div(id='kpi-output', className="mt-3")
        ])
    return dbc.Alert("Sélectionnez un onglet", color="info", className="text-center")


@callback(
    Output('histogram', 'figure'),
    Output('boxplot', 'figure'),
    Output('descriptive-stats-table', 'children'),
    [Input('numeric-var-dropdown', 'value'), Input('filtration', 'value')],
    State('theme-store', 'data')
)
def update_numeric_graphs(selected_var, filtration, theme_value):
    try:
        if not selected_var or df.empty:
            empty_fig = px.scatter(title="Sélectionnez une variable")
            return empty_fig, empty_fig, dbc.Alert("Veuillez sélectionner une variable.", color="info")
        template = theme.THEMES[theme_value]['plotly']
        if filtration == "all":
            filtered_df = df
            test = jarque_bera(filtered_df[selected_var])[1]
            title_suffix = f"tous les clients (JB p-value : {test:.4f})"
        else:
            filtered_df = df.loc[df['y'].isin([filtration])]
            status = "ayant souscrit" if filtration == 'yes' else "non souscrit"
            test = jarque_bera(filtered_df[selected_var])[1]
            title_suffix = f"clients {status} (JB p-value : {test:.4f})"
        hist_fig = px.histogram(filtered_df, x=selected_var,
                                title=f'Distribution de {selected_var}<br><sub>{title_suffix}</sub>',
                                template=template)
        hist_fig.update_layout(margin=dict(l=20, r=20, t=70, b=20), autosize=True)
        box_fig = px.box(filtered_df, y=selected_var,
                         title=f'Box Plot de {selected_var}<br><sub>{title_suffix}</sub>',
                         template=template)
        box_fig.update_layout(margin=dict(l=20, r=20, t=70, b=20), autosize=True)
        stats = filtered_df[selected_var].describe().reset_index()
        stats.columns = ['Statistique', 'Valeur']
        stats['Valeur'] = stats['Valeur'].round(4)
        table = html.Div([
            dbc.Table.from_dataframe(stats, striped=True, bordered=True, hover=True,
                                     responsive=True,
                                     color='dark' if theme_value == 'dark' else 'light',
                                     style={
                                         'backgroundColor': '#343a40' if theme_value == 'dark' else '#ffffff',
                                         'color': '#ffffff' if theme_value == 'dark' else '#212529',
                                         'fontSize': '0.9rem'
                                     })
        ], className="table-responsive-container")
        return hist_fig, box_fig, table
    except Exception:
        empty_fig = px.scatter(title="Erreur")
        return empty_fig, empty_fig, dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            "Veuillez actualiser la page"
        ], color="warning")


@callback(
    Output('bar-chart', 'figure'),
    [Input('categorical-var-dropdown', 'value'), Input('filtration', 'value')],
    State('theme-store', 'data')
)
def update_categorical_graph(selected_var, filtration, theme_value):
    if not selected_var or df.empty:
        return px.scatter(title="Sélectionnez une variable")
    template = theme.THEMES[theme_value]['plotly']
    if filtration == "all":
        filtered_df = df.copy()
        status = "tous les clients"
    else:
        filtered_df = df.loc[df['y'] == filtration]
        status = "ayant souscrit" if filtration == 'yes' else "n'ayant pas souscrit"
    counts = filtered_df[selected_var].value_counts().reset_index()
    counts.columns = [selected_var, 'count']
    if counts[selected_var].nunique() <= 3:
        fig = px.pie(counts, names=selected_var, values='count',
                     title=f'Répartition par {selected_var} ({status})', template=template)
    else:
        fig = px.bar(counts, x=selected_var, y='count',
                     title=f'Répartition par {selected_var} ({status})', template=template)
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20), autosize=True)
    return fig


@callback(
    Output('kpi-output', 'children'),
    [Input('kpi-dropdown', 'value'), Input('filtration', 'value')],
    State('theme-store', 'data')
)
def update_kpi(selected_kpi, filtre, theme_value):
    if df.empty:
        return dbc.Alert("Les données ne sont pas disponibles.", color="danger")
    template = theme.THEMES[theme_value]['plotly']
    if selected_kpi == 'subscription_rate':
        if filtre == "all":
            rate = df['y'].count()
            card = dbc.Card(
                dbc.CardBody([
                    html.H4([html.I(className="fas fa-users me-2"), "Total de clients"],
                            className="card-title text-center"),
                    html.P(f"{rate:,}", className="card-text fs-1 text-center fw-bold")
                ]),
                className="text-center kpi-card shadow-sm",
                color="success" if theme_value == 'light' else "secondary", inverse=True
            )
            return card
        else:
            rate = (df['y'].value_counts(normalize=True)[filtre] * 100).round(2)
            status = "Taux de Souscription" if filtre == "yes" else "Taux de Non-souscription"
            card = dbc.Card(
                dbc.CardBody([
                    html.H4([html.I(className="fas fa-percentage me-2"), status],
                            className="card-title text-center"),
                    html.P(f"{rate}%", className="card-text fs-1 text-center fw-bold")
                ]),
                className="text-center kpi-card shadow-sm",
                color="success" if theme_value == 'light' else "secondary", inverse=True
            )
            return card
    elif selected_kpi == 'age_distribution':
        fig = px.histogram(df, x='age', nbins=30, title='Distribution des Âges', template=template)
        fig.update_layout(margin=dict(l=20, r=20, t=50, b=20), autosize=True)
        return html.Div([dcc.Graph(figure=fig, config=GRAPH_CONFIG, style=GRAPH_STYLE)], className="graph-container")
    elif selected_kpi == 'marital_status':
        fig = px.pie(df, names='marital', title='Répartition par Statut Marital', template=template)
        fig.update_layout(margin=dict(l=20, r=20, t=50, b=20), autosize=True)
        return html.Div([dcc.Graph(figure=fig, config=GRAPH_CONFIG, style=GRAPH_STYLE)], className="graph-container")
    return dbc.Alert("KPI non implémenté.", color="info")