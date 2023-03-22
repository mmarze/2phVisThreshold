# Run this app with `python main.py` and visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from app_functions import log_threshold, threshold

prf = np.logspace(6, 8, 201)
len_prf = len(prf)
pul_dur = np.logspace(-13, -9, 401)
len_pul_dur = len(pul_dur)
thr0 = np.zeros((len_prf, len_pul_dur))
thr25 = np.zeros((len_prf, len_pul_dur))
thr5 = np.zeros((len_prf, len_pul_dur))
thr0lin = np.zeros((len_prf, len_pul_dur))
thr25lin = np.zeros((len_prf, len_pul_dur))
thr5lin = np.zeros((len_prf, len_pul_dur))

for i in range(0, len_prf):
    for j in range(0, len_pul_dur):
        thr0[i, j] = log_threshold(prf[i], pul_dur[j], 0)
        thr25[i, j] = log_threshold(prf[i], pul_dur[j], 1)
        thr5[i, j] = log_threshold(prf[i], pul_dur[j], 2)
        thr0lin[i, j] = threshold(prf[i], pul_dur[j], 0)
        thr25lin[i, j] = threshold(prf[i], pul_dur[j], 1)
        thr5lin[i, j] = threshold(prf[i], pul_dur[j], 2)
        
thr_plot0 = pd.DataFrame(thr0, prf, pul_dur)
thr_plot25 = pd.DataFrame(thr25, prf, pul_dur)
thr_plot5 = pd.DataFrame(thr5, prf, pul_dur)
thr_plot0lin = pd.DataFrame(thr0lin, prf, pul_dur)
thr_plot25lin = pd.DataFrame(thr25lin, prf, pul_dur)
thr_plot5lin = pd.DataFrame(thr5lin, prf, pul_dur)

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Expected visual threshold value in the function of pulse train parameters for 1030 nm sech\u00b2 '
            'pulsed laser'),
    html.Div([
        html.Label('Retinal location'),
        dcc.Dropdown(['0 deg retinal eccentricity (fovea center)', '2.5 deg retinal eccentricity',
                      '5 deg retinal eccentricity'], '0 deg retinal eccentricity (fovea center)',
                     id='retinal_eccentricity')], style={'padding': 10, 'flex': 1}),
    html.P('Click on the heatmap plot below to get more info'),
    dcc.Graph(id='indicator-graphic'),
    html.Div(id='click-data'),
    html.Div(id='hover-data'),
    dcc.Graph(id='indicator-graphic2')  
])


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('retinal_eccentricity', 'value'))
def heatmap_graph(retinal_eccentricity_value):
    
    if retinal_eccentricity_value == '0 deg retinal eccentricity (fovea center)':
        thr_plot = thr_plot0
    elif retinal_eccentricity_value == '2.5 deg retinal eccentricity':
        thr_plot = thr_plot25
    else:
        thr_plot = thr_plot5
   
    fig = go.Figure(data=go.Heatmap(
                    z=np.array(thr_plot),
                    x=np.array(thr_plot.columns),
                    y=np.array(thr_plot.index),
                    hovertemplate="<b>log(threshold): %{z:.2f} log(W)</b><br>pulse duration: %{x} <br>pulse repetition "
                                  "frequency: %{y}<extra></extra>",
                    colorscale='rainbow', zmax=-3.4, zmin=-6.7,
                    colorbar=dict(title="log(Expected mean visual threshold value [W])")))

    fig.update_xaxes(showspikes=True, spikecolor="red", spikethickness=1, spikesnap="cursor", spikemode="across")
    fig.update_yaxes(showspikes=True, spikecolor="red", spikethickness=1, spikemode="across")

    fig.update_layout(xaxis_title='Pulse duration', yaxis_title='Pulse repetition frequency', xaxis_type='log',
                      yaxis_type='log')
    fig['layout']['xaxis']['ticksuffix'] = 's'
    fig['layout']['yaxis']['ticksuffix'] = 'Hz'

    return fig


@app.callback(
    Output('click-data', 'children'),
    Output('indicator-graphic2', 'figure'),
    Input('retinal_eccentricity', 'value'),
    [Input('indicator-graphic', 'clickData')])
def display_data_on_click(retinal_eccentricity_value, click_data):

    if retinal_eccentricity_value == '0 deg retinal eccentricity (fovea center)':
        err = 0.0986
    elif retinal_eccentricity_value == '2.5 deg retinal eccentricity':
        err = 0.0606
    else:
        err = 0.0714

    if click_data is not None:
        x_val = click_data['points'][0]['x']
        y_val = click_data['points'][0]['y']
        z_val = np.format_float_scientific(np.power(10, click_data['points'][0]['z']), precision=3)
        err_val = np.format_float_scientific(err * float(z_val), precision=3)
        thr_str = f"Expected mean visual threshold value: {z_val} \u00B1 {err_val} W."
    else:
        thr_str = ''
        x_val = 1e-13
        y_val = 1e6
    
    x_val2 = np.format_float_scientific(x_val, precision=3)
    y_val2 = np.format_float_scientific(y_val, precision=3)
    
    fig2 = make_subplots(rows=1, cols=2)
    fig2.add_trace(go.Scatter(x=np.array(thr_plot0.columns), y=np.array(thr_plot0lin.loc[:, x_val]),
                              name=f'0 deg retinal eccentricity, {y_val2} Hz PRF'), row=1, col=1)
    fig2.add_trace(go.Scatter(x=np.array(thr_plot0.columns), y=np.array(thr_plot25lin.loc[:, x_val]),
                              name=f'2.5 deg retinal eccentricity, {y_val2} Hz PRF'), row=1, col=1)
    fig2.add_trace(go.Scatter(x=np.array(thr_plot0.columns), y=np.array(thr_plot5lin.loc[:, x_val]),
                              name=f'5 deg retinal eccentricity, {y_val2} Hz PRF'), row=1, col=1)
    fig2.add_trace(go.Scatter(x=np.array(thr_plot0.index), y=np.array(thr_plot0lin.loc[y_val])[:],
                              name=f'0 deg retinal eccentricity, {x_val2} s pulse duration'), row=1, col=2)
    fig2.add_trace(go.Scatter(x=np.array(thr_plot0.index), y=np.array(thr_plot25lin.loc[y_val])[:],
                              name=f'2.5 deg retinal eccentricity, {x_val2} s pulse duration'), row=1, col=2)
    fig2.add_trace(go.Scatter(x=np.array(thr_plot0.index), y=np.array(thr_plot5lin.loc[y_val])[:],
                              name=f'5 deg retinal eccentricity, {x_val2} s pulse duration'), row=1, col=2)
    fig2['layout']['xaxis']['title'] = 'Pulse duration'
    fig2['layout']['xaxis2']['title'] = 'Pulse repetition frequency'
    fig2['layout']['yaxis']['title'] = 'Expected mean visual threshold value'
    fig2['layout']['yaxis2']['title'] = 'Expected mean visual threshold value'
    fig2['layout']['xaxis']['type'] = 'log'
    fig2['layout']['xaxis2']['type'] = 'log'
    fig2['layout']['xaxis']['ticksuffix'] = 's'
    fig2['layout']['xaxis2']['ticksuffix'] = 'Hz'
    fig2['layout']['yaxis']['ticksuffix'] = 'W'
    fig2['layout']['yaxis2']['ticksuffix'] = 'W'
    
    return thr_str, fig2
    

if __name__ == '__main__':
    app.run_server(debug=False)
