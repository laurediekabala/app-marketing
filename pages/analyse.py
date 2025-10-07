 # pages/analyse.py
import dash
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from utils import theme
from transformation import dataset,type_col
from dash.exceptions import PreventUpdate
import plotly.figure_factory as ff
from scipy.stats import chi2_contingency,kruskal,shapiro,jarque_bera,kstest

# --- Chargement et préparation des données ---
# URL du jeu de données sur Kaggle (version brute)

try:
    df = dataset()
    # Pour simplifier, nous allons convertir les colonnes numériques potentielles
except Exception as e:
    print(f"Erreur de chargement des données: {e}")
    # Créer un dataframe vide en cas d'erreur pour que l'app ne plante pas
    df = pd.DataFrame({'error': [f'Impossible de charger les données: {e}']})

# Séparer les colonnes numériques et catégorielles
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
options =[{"label" :"tous","value":"all"}]+[{"label":str(val),"value":val} for val in df["y"].dropna().unique()]
filtr = [{"label":val,"value":val} for val in categorical_cols]
filtr_y =[{"label":str(val),"value":val} for val in df["y"].dropna().unique()]

modal_num = dbc.Modal([
        dbc.ModalHeader("Analyse Bivariée Numérique"),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Variable X:"),
                    dcc.Dropdown(
                        id='bivariate-num-x',
                        options=[{'label': col, 'value': col} for col in numerical_cols],
                        value=numerical_cols[0] if numerical_cols else None
                    )
                ]),
                dbc.Col([
                    dbc.Label("Variable Y:"),
                    dcc.Dropdown(
                        id='bivariate-num-y',
                        options=[{'label': col, 'value': col} for col in numerical_cols],
                        value=numerical_cols[1] if len(numerical_cols) > 1 else numerical_cols[0]
                    )
                ]),
                   dbc.Col([
                    dbc.Label("filtre:"),
                    dcc.Dropdown(
                        id='filtre',
                        options=filtr,
                        value=numerical_cols[0] if numerical_cols else None )
                ])
            ]),
            html.Div(id='bivariate-num-plot', className="mt-4")
        ]),
    ], id="modal-bivariate-num", is_open=False,centered=True,fade=True,backdrop=True,size="xl",scrollable=True)
modal_cat = dbc.Modal([
        dbc.ModalHeader("Analyse Bivariée Catégorielle"),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Variable X:"),
                    dcc.Dropdown(
                        id='bivariate-cat-x',
                        options=[{'label': col, 'value': col} for col in categorical_cols],
                        value=categorical_cols[0] if categorical_cols else None
                    )
                ]),
                dbc.Col([
                    dbc.Label("Variable Y:"),
                    dcc.Dropdown(
                        id='bivariate-cat-y',
                        options=[{'label': col, 'value': col} for col in categorical_cols],
                        value=categorical_cols[1] if len(categorical_cols) > 1 else categorical_cols[0]
                    )
                ]),
            ]),
            html.Div(id='bivariate-cat-plot', className="mt-4")
        ]),
    ], id="modal-bivariate-cat",is_open=False,centered=True,fade=True,backdrop=True,size="xl",scrollable=True)
modal_cat_num = dbc.Modal([
        dbc.ModalHeader("Analyse Bivariée num-cat"),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("select var num:"),
                    dcc.Dropdown(
                        id='bivariate-num-cat-x',
                        options=[{'label': col, 'value': col} for col in numerical_cols],
                        value=numerical_cols[0] if numerical_cols else None
                    )
                ]),
                dbc.Col([
                    dbc.Label("select var cat:"),
                    dcc.Dropdown(
                        id='bivariate-num-cat-y',
                        options=[{'label': col, 'value': col} for col in categorical_cols],
                        value=categorical_cols[1] if len(categorical_cols) > 1 else categorical_cols[0]
                    )
                ]),
                    dbc.Col([
                    dbc.Label("filtre:"),
                    dcc.Dropdown(
                        id='bfiltre',
                        options=filtr,
                        value=categorical_cols[0] if categorical_cols else None )
                ])
            ]),
            html.Div(id='bivariate-num-cat-plot', className="mt-4")
        ]),
    ], id="modal-bivariate-num_cat", is_open=False,centered=True,fade=True,backdrop=True,size="xl",scrollable=True)
collapse_st=dbc.Collapse([
        dbc.ModalHeader("Test statistique"),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Variable X:"),
                    dcc.Dropdown(
                        id='bivariate-num-x',
                        options=[{'label': col, 'value': col} for col in numerical_cols],
                        value=numerical_cols[0] if numerical_cols else None
                    )
                ]),     
            ]),
            html.Div(id='test_stat', className="mt-4")
        ]),
    ], id="collapse_stat", is_open=False)
def layout():

    return dbc.Container([
        html.H1("Page d'Analyse des Données", className="mb-4"),
        dbc.Label("filtration"),
        dcc.Dropdown(
                id='filtration',
                #options=[{'label': col, 'value': col} for col in df["y"].unique()],
                #value =[col for col in df["y"].unique()],multi=True
                options =options,
                value='all',
                clearable=False   
            ),
             # Ajout des boutons d'analyse bivariée
             dbc.Row([
            dbc.Col([
                dbc.Button(
                    "Analyse Bivariée Numérique",
                    id="btn-bivariate-num",
                    color="primary",
                    className="me-2 mb-2"
                ),
                dbc.Button(
                    "Analyse Bivariée Catégorielle",
                    id="btn-bivariate-cat",
                    color="secondary",
                    className="mb-2"
                ),
                   dbc.Button(
                    "Analyse Bivariée numeric-Catégorielle",
                    id="btn-bivariate-num-cat",
                    color="secondary",
                    className="mb-2"
                ),
                 dbc.Button(
                    "test statistique",
                    id="collap_st",
                    color="secondary",
                    className="mb-2"
                )
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Spinner(
                    html.Div(id="bivariate-num-container"),
                    color="primary",
                    type="grow",
                ),
            ], width=12, className="mb-4"),
            
            dbc.Col([
                dbc.Spinner(
                    html.Div(id="bivariate-cat-container"),
                    color="secondary",
                    type="grow",
                ),
            ], width=12, className="mb-4"),
        ]),
        modal_num,
        modal_cat,
        modal_cat_num,
        collapse_st,
        dbc.Tabs([
            dbc.Tab(label="Analyse Descriptive", tab_id="tab-descriptive"),
            dbc.Tab(label="KPIs", tab_id="tab-kpi"),
        ], id="analyse-tabs", active_tab="tab-descriptive", className="mb-4"),
        
        html.Div(id="tabs-content")
        
    ], fluid=True, className="py-4")
@callback(
    Output("modal-bivariate-num", "is_open"),
    Input("btn-bivariate-num", "n_clicks"),
    [State("modal-bivariate-num", "is_open"),
    State('theme-store', 'data')],
   
)
def update_bivariate_numeric(n,is_open,theme_value):
    if n :
        return not is_open
    return is_open
    #filtered_df = df if filtration == "all" else df[df['y'] == filtration]
    

@callback(
    Output("modal-bivariate-cat", "is_open"),
    Input("btn-bivariate-cat", "n_clicks"),
    [State('modal-bivariate-cat', 'is_open'),State('theme-store', 'data')],
)
def update_bivariate_categorical(n, is_open, theme_value):
    if n:
        return not is_open
    return is_open
    # Filtrage des données
    #filtered_df = df if filtration == "all" else df[df['y'] == filtration]
# Callbacks pour mettre à jour les graphiques bivariés
@callback(
    Output('bivariate-num-plot', 'children'),
    [Input('bivariate-num-x', 'value'),
     Input('bivariate-num-y', 'value'),Input('filtre', 'value')],
    State('theme-store', 'data')
)
def update_bivariate_num_plot(var_x, var_y,filtre, theme_value):
    if not var_x or not var_y:
        return "Sélectionnez deux variables"
    
    template = theme.THEMES[theme_value]['plotly']
    fig = px.scatter(df, x=var_x, y=var_y, 
                    title=f'Analyse Bivariée: {var_x} vs {var_y}',color=filtre,
                    template=template)
    
    return dcc.Graph(figure=fig)

@callback(
    Output('bivariate-cat-plot', 'children'),
    [Input('filtration', 'value'),Input('bivariate-cat-x', 'value'),
     Input('bivariate-cat-y', 'value')],
    State('theme-store', 'data')
)
def update_bivariate_cat_plot(filtration,var_x, var_y, theme_value):
    if not var_x or not var_y:
        return "Sélectionnez deux variables"
    # Création d'une table de contingence
    if filtration == "all":
        filtered_df = df
        contingency = pd.crosstab(filtered_df[var_x], filtered_df[var_y])
        stat =chi2_contingency(contingency,correction=True)[1]
        template = theme.THEMES[theme_value]['plotly']
        fig = px.imshow(contingency,
                    labels=dict(x=var_x, y=var_y, color="Fréquence"),
                    title=f'Table de contingence: {var_x} vs {var_y} pour tous les clients le test stat {stat}',
                    template=template)
    else:
        filtered_df = df.loc[df['y'].isin([filtration])]
        status = "ayant souscrit" if filtration=='yes' else "n'ayant pas souscrit"
        title_suffix = f"pour les clients {status}"
        contingency = pd.crosstab(filtered_df[var_x], filtered_df[var_y])
        stat =chi2_contingency(contingency,correction=True)[1]
        template = theme.THEMES[theme_value]['plotly']
        fig = px.imshow(contingency,
                        labels=dict(x=var_x, y=var_y, color="Fréquence"),
                        title=f'Table de contingence: {var_x} vs {var_y} pour les clients {status} le test stat {stat}',
                        template=template)
    
    return dcc.Graph(figure=fig)
# modal de cat et numeric
@callback(
    Output("modal-bivariate-num_cat", "is_open"),
    Input("btn-bivariate-num-cat", "n_clicks"),
    [State("modal-bivariate-num_cat", "is_open"),
    State('theme-store', 'data')],
   
)
def update_bivariate_numeric_cat(n,is_open,theme_value):
    if n :
        return not is_open
    return is_open
    #filtered_df = df if filtration == "all" else df[df['y'] == filtration]

@callback(
    Output('bivariate-num-cat-plot', 'children'),
    [Input('bivariate-num-cat-x', 'value'),
     Input('bivariate-num-cat-y', 'value'),
     Input('bfiltre', 'value')
     ],
    State('theme-store', 'data')
)
def update_bivariate_num_cat_plot(var_x, var_y,filtre, theme_value):
    if not var_x or not var_y:
        return "Sélectionnez deux variables"
    
    # Création d'une table de contingence
    template = theme.THEMES[theme_value]['plotly']
    fig = px.box(df,x=var_y,y=var_x,
                    labels=dict(x=var_x, y=var_y, color="Fréquence"),
                    title=f'Table de contingence: {var_x} vs {var_y}',color=filtre,
                    template=template)
    
    return dcc.Graph(figure=fig)   
@callback(
    Output("collapse_stat", "is_open"),
    Input("collap_st", "n_clicks"),
    [State("collapse_stat", "is_open"),
    State('theme-store', 'data')],
   
)
def update_test_statistique(n,is_open,theme_value):
    if n :
        return not is_open
    return is_open
    #filtered_df = df if filtration == "all" else df[df['y'] == filtration] 
@callback(
    Output('test_stat', 'children'),
    Input('bivariate-num-x', 'value'),
    State('theme-store', 'data')
)
def test_hypothse(var_x, theme_value):
    if not var_x:
        return "Sélectionnez une variable"  
    data_no= df.loc[df["y"]=="no"]
    data_yes =df.loc[df["y"]=="yes"]
    pvalue= kruskal(data_no[var_x],data_yes[var_x])[1]
    if pvalue< 0.05 :
        return f"il y a une difference significative selon {var_x} entre les souscrits et les non souscrits avec pvalue={round(pvalue,2)}"
    else :
            return f"il n y a pas une difference significative selon {var_x} entre les souscrits et les non souscrits avec pvalue={round(pvalue,2)}"

@callback(
    Output('tabs-content', 'children'),
    Input('analyse-tabs', 'active_tab')
)
def render_tab_content(active_tab):
    if active_tab == "tab-descriptive":
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Choisir une variable numérique:"),
                    dcc.Dropdown(id='numeric-var-dropdown', options=[{'label': i, 'value': i} for i in numerical_cols], value=numerical_cols[0] if numerical_cols else None)
                ], width=6),
                dbc.Col([
                    dbc.Label("Choisir une variable catégorielle:"),
                    dcc.Dropdown(id='categorical-var-dropdown', options=[{'label': i, 'value': i} for i in categorical_cols], value=categorical_cols[0] if categorical_cols else None)
                ], width=6)
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col(dcc.Graph(id='histogram'), width=6),
                dbc.Col(dcc.Graph(id='boxplot'), width=6)
            ]),
            dbc.Row([
                 dbc.Col(dcc.Graph(id='bar-chart'), width=12)
            ]),
            html.H4("Statistiques Descriptives", className="mt-4"),
            html.Div(id='descriptive-stats-table')
        ])
    elif active_tab == "tab-kpi":
        return html.Div([
            dbc.Label("Sélectionner un KPI à visualiser:"),
            dcc.Dropdown(
                id='kpi-dropdown',
                options=[
                    {'label': 'Taux de souscription global', 'value': 'subscription_rate'},
                    {'label': 'Distribution des âges des clients', 'value': 'age_distribution'},
                    {'label': 'Répartition par statut marital', 'value': 'marital_status'}
                ],
                value='subscription_rate'
            ),
            html.Div(id='kpi-output', className="mt-4")
        ])
    return html.P("Sélectionnez un onglet")

# --- Callbacks pour l'analyse descriptive ---

@callback(
    Output('histogram', 'figure'),
    Output('boxplot', 'figure'),
    Output('descriptive-stats-table', 'children'),
    [Input('numeric-var-dropdown', 'value'),Input('filtration', 'value')],
    State('theme-store', 'data')
)
def update_numeric_graphs(selected_var,filtration, theme_value):
    try :
        if not selected_var or df.empty:
            return {}, {}, "Veuillez sélectionner une variable numérique."
            
        template = theme.THEMES[theme_value]['plotly']
        # 1. Filtrage du DataFrame
        if filtration == "all":
            filtered_df = df
            test =jarque_bera(filtered_df[selected_var])[1]
            #test= round(test,2)
        
            title_suffix = f"pour tous les clients {test}"
        else:
            filtered_df = df.loc[df['y'].isin([filtration])]
            status = "ayant souscrit" if filtration=='yes' else "non souscrit"
            test =jarque_bera(filtered_df[selected_var])[1]
            #test= round(test,2)
            title_suffix = f"pour les clients {status} {test}"
        
        
        hist_fig = px.histogram(filtered_df, x=selected_var, title=f'Dist de {selected_var} pour {title_suffix}', template=template)
        box_fig = px.box(filtered_df, y=selected_var, title=f'Box de {selected_var} pour {title_suffix}', template=template)
        
        stats = filtered_df[selected_var].describe().reset_index().rename(columns={'index': 'Statistique', selected_var: 'Valeur'})
        
        table = dbc.Table.from_dataframe(stats, 
            striped=True, 
            bordered=True, 
            hover=True,
            color='dark' if theme_value == 'dark' else 'light',  # Couleur de la table selon le thème
            style={
                'background-color': '#343a40' if theme_value == 'dark' else '#ffffff',
                'color': '#ffffff' if theme_value == 'dark' else '#212529'
            })
        return hist_fig, box_fig, table
    except  :
        return dbc.Alert("veuillez actualiser")

@callback(
    Output('bar-chart', 'figure'),
    [Input('categorical-var-dropdown', 'value'),Input('filtration', 'value')],
    State('theme-store', 'data')
)
def update_categorical_graph(selected_var,filtration ,theme_value):
    if not selected_var or df.empty:
  
        return {}
    template = theme.THEMES[theme_value]['plotly']    
    if filtration == "all":
        filtered_df = df.copy()
        #title_suffix = "pour tous les clients"
        status="tous les clients"
    else:
        filtered_df = df.loc[df['y']==filtration]
        status = "ayant souscrit" if filtration=='yes' else "n'ayant pas souscrit"
        #title_suffix = f"pour les clients {status}"
    counts =  filtered_df[selected_var].value_counts().reset_index()
    counts.columns = [selected_var, 'count']
    if counts[selected_var].nunique()<=3 :
          bar_fig = px.pie(counts, names=selected_var, values='count', title=f'Répartition par {selected_var} {status}', template=template)
          return bar_fig
    else :
          bar_fig = px.bar(counts, x=selected_var, y='count', title=f'Répartition par {selected_var} {status}', template=template)
          return bar_fig
    
    
# Callbacks pour mettre à jour les graphiques bivariés


# --- Callback pour les KPIs ---

@callback(
    Output('kpi-output', 'children'),
    [Input('kpi-dropdown', 'value'),Input('filtration', 'value')],
    State('theme-store', 'data')
)
def update_kpi(selected_kpi,filtre, theme_value):
    if df.empty:
        return dbc.Alert("Les données ne sont pas disponibles.", color="danger")
        
    template = theme.THEMES[theme_value]['plotly']

    if selected_kpi == 'subscription_rate':
        if filtre=="all" :
            rate = df['y'].count()
            card = dbc.Card(
                dbc.CardBody([
                    html.H4("total de clients", className="card-title"),
                    html.P(f"{rate}", className="card-text fs-1 text-center")
                ]),
                className="text-center",
                color="success" if theme_value == 'light' else "secondary",
                inverse=True
            )
            return card
        else :
              rate = (df['y'].value_counts(normalize=True)[filtre] * 100).round(2)
              status= "Taux de Souscription" if filtre=="yes" else "Taux Non souscription"
              card = dbc.Card(
                dbc.CardBody([
                    html.H4("Taux de Souscription", className="card-title"),
                    html.P(f"{rate}%", className="card-text fs-1 text-center")
                ]),
                className="text-center",
                color="success" if theme_value == 'light' else "secondary",
                inverse=True
            )
              return card

    
    elif selected_kpi == 'age_distribution':
        fig = px.histogram(df, x='age', nbins=30, title='Distribution des Âges', template=template)
        return dcc.Graph(figure=fig)
        
    elif selected_kpi == 'marital_status':
        fig = px.pie(df, names='marital', title='Répartition par Statut Marital', template=template)
        return dcc.Graph(figure=fig)
        
    return "KPI non implémenté."
