"""
Created on Mon Oct  6 12:15:18 2025
@author: Marco Contucci
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm

def rw_function(pd, lgd, M, EAD=1):
    pd = np.clip(pd, 1e-6, 1)
    R = 0.12 * (1 - np.exp(-50 * pd)) / (1 - np.exp(-50)) + \
        0.24 * (1 - (1 - np.exp(-50 * pd)) / (1 - np.exp(-50)))
    
    b = (0.11852 - 0.05478 * np.log(pd)) ** 2
    
    term1 = norm.ppf(pd) / np.sqrt(1 - R)
    term2 = np.sqrt(R / (1 - R)) * norm.ppf(0.999)
    
    capital_requirement = lgd * (norm.cdf(term1 + term2) - lgd * pd)
    maturity_adj = (1 + (M - 2.5) * b) / (1 - 1.5 * b)
    K = capital_requirement * maturity_adj
    return K * 12.5 * 1.06 * EAD

#Grid
pd_vals = np.linspace(0.0001, 0.15, 50)
lgd_vals = np.linspace(0.1, 0.9, 50)
PD, LGD = np.meshgrid(pd_vals, lgd_vals)
maturities = [1, 2, 3, 4, 5]
frames = []

#Prepara tutte le superfici per ciascun M
for M in maturities:
    RW = rw_function(PD, LGD, M)
    frame = go.Surface(z=RW, x=PD*100, y=LGD*100,
        colorscale='Plasma', name=f'M={M}',
        visible=False
    )
    frames.append(frame)

#Rendi visibile solo la prima
frames[0]['visible'] = True

#Layout con slider
steps = []
for i, M in enumerate(maturities):
    step = dict(
        method='update',
        args=[{'visible': [False] * len(frames)},
              {'title': f'<b> Maturity = {M}Y </b>'}],
        label=f'{M} Y'
    )
    step['args'][0]['visible'][i] = True
    steps.append(step)

sliders = [dict(active=0, steps=steps, x=0, y=-0.15, xanchor='left', yanchor='bottom')]




################################################
# 2. Create figure 3D #
################################################

fig = go.Figure(data=frames)
fig.update_layout(
    sliders=sliders,
    scene=dict(
        xaxis_title='PD (%)',
        yaxis_title='LGD (%)',
        zaxis_title='RW'
    ),
    height=600,
    title='<b> Maturity = 1Y </b>'
)

#Export Plotly graph to HTML string
plot_html = fig.to_html(include_plotlyjs='cdn', full_html=False)


################################################
# 1. Formula immagine
################################################

image_path = "Formula_RW.png"
image_html = f"""
<div style="text-align: center; margin-top: 20px;">
  <img src="{image_path}" alt="Formula RW" style="max-width: 60%; height: auto;">
</div>
"""


################################################
# 3. TABLE #
################################################

 #Range PD e LGD
pd_vals = np.array([0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.10])  # PD da 0.1% a 10%
lgd_vals = np.arange(0.1, 1.1, 0.1)  # LGD da 10% a 100%

#Calcolo tabella
data = {}
for lgd in lgd_vals:
    rw_vals = [rw_function(pd, lgd,M=2) for pd in pd_vals]
    data[f'LGD {int(lgd*100)}%'] = np.round(rw_vals, 2)
    
    
 #Costruzione DataFrame
df = pd.DataFrame(data, index=[f'PD {float(pd*100)}%' for pd in pd_vals])
df.index.name = 'RW'  
    
table_html = df.to_html(classes='table table-striped', border=1)


################################################
# 4. Funzione Python #
################################################

function_code_html = """
<div style="margin-top: 40px;">
  <h3>4. Python Function RW </h3>
  <pre style="background-color:#f4f4f4; padding:15px; border:1px solid #ddd; overflow-x:auto;">
import numpy as np
from scipy.stats import norm

def rw_function(pd, lgd, M):
    pd = np.clip(pd, 1e-6, 1)
    R = 0.12 * (1 - np.exp(-50 * pd)) / (1 - np.exp(-50)) +
        0.24 * (1 - (1 - np.exp(-50 * pd)) / (1 - np.exp(-50)))
    
    b = (0.11852 - 0.05478 * np.log(pd)) ** 2
    
    term1 = norm.ppf(pd) / np.sqrt(1 - R)
    term2 = np.sqrt(R / (1 - R)) * norm.ppf(0.999)
    
    capital_requirement = lgd * (norm.cdf(term1 + term2) - lgd * pd)
    maturity_adj = (1 + (M - 2.5) * b) / (1 - 1.5 * b)
    K = capital_requirement * maturity_adj
    return K * 12.5 * 1.06
  </pre>
</div>
"""
    

################################################
# Build full HTML #
################################################

full_html = f"""
<html>
<head>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
<h3>1. Formula RW (CRR 575/2013 p.97)</3>
  {image_html}
  <hr>
<h3>2. Interactive RW Surface </h3>
  {plot_html}
  <hr>
<h3>3. Tabella di Sensitivity RW (Maturity = 2)</h3>
<div style="text-align:center; margin-top: 30px;">
  <div style="display: inline-block; border-collapse: collapse;">
    {table_html}
  </div>
</div>
  <hr>
  {function_code_html}
</body>
</html>
"""

# HTML to file
with open("RW_surface.html", "w", encoding="utf-8") as f:
    f.write(full_html)
    

