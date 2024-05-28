from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral5
from bokeh.io import output_file
from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.palettes import viridis
from bokeh.models import NumeralTickFormatter
from bokeh.palettes import Category20
from bokeh.models.tools import ResetTool, PanTool, HoverTool
import numpy as np
import pandas as pd

df = pd.read_csv('laptop_final.csv')


# VISUALIZATION ONE
p = figure(height=600, width=850, title='Price Most Preferred')
hist, edges = np.histogram(df['Price'], bins=10)
# Compute the center of each bin
x = (edges[:-1] + edges[1:]) / 2
# Define a list of colors
colors = Category20[10]
# Plot the histogram bars using the Quad glyph with different colors
for i in range(len(hist)):
    p.quad(top=hist[i], bottom=0, left=edges[i], right=edges[i+1], fill_color=colors[i % len(colors)], line_color='black')
# Customize the plot
p.title.text_font_size = '16pt'
p.title.align = 'center'
p.background_fill_color = "#E0F9F2"
p.xaxis.axis_label = 'Price'
p.yaxis.axis_label = 'Count'
p.yaxis.axis_label_text_font_style = "bold"
p.xaxis.axis_label_text_font_style = "bold"
p.tools = []
formatter = NumeralTickFormatter(format='0,0')
p.yaxis.formatter = formatter


# VISUALIZATION TWO
gpu=df.loc[:, 'Gpu brand'].value_counts()

from math import pi
from bokeh.palettes import Category20c
from bokeh.transform import cumsum

x =gpu
data = pd.Series(x).reset_index(name='value')
data = data.rename(columns={'Gpu brand': 'Gpu'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(x)]

p1 = figure(height=600, width=850, title="Most used Gpu brand by Laptops.", toolbar_location=None,
           tools="hover", tooltips="@Gpu: @value", x_range=(-0.5, 1.0))

p1.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Gpu', source=data)

p1.axis.axis_label = None
p1.axis.visible = False
p1.grid.grid_line_color = None
p1.background_fill_color = "#E0F9F2"
p1.title.text_font_size = '16pt'
p1.title.align = 'center'
p1.xaxis.minor_tick_line_color = "black"


#   VISUALIZATION THREE
from bokeh.palettes import Category10
p2 = figure(x_range=df['TypeName'].unique(), height=600, width=850, title='Price by TypeName')

# Define the color palette
colors = Category10[len(df['TypeName'].unique())]

# Plot the bars with different colors
p2.vbar(x=df['TypeName'].value_counts().index, top=df['TypeName'].value_counts().values, width=0.5, color=colors)

# Customize the plot
p2.xaxis.axis_label = 'TypeName'
p2.yaxis.axis_label = 'Value count by Laptop TypeName'
p2.yaxis.axis_label_text_font_style = "bold"
p2.xaxis.axis_label_text_font_style = "bold"
p2.xaxis.major_label_orientation = 'vertical'
p2.title.align = 'center'
p2.title.text_font_size = '16pt'
p2.background_fill_color = "#E0F9F2"
p2.xaxis.major_label_orientation = 'vertical'


#   VISUALIZATION FOUR
ddat= df['Company'].value_counts().reset_index()
ddat.columns = ['Company', 'Count']

p3 = figure(x_range=ddat['Company'], height=600, width=850, title="Count of Laptops for each brand")
x=ddat['Company']
y=ddat['Count']
p3.circle(x,y)

p3.grid.bounds = (4, 8)

p3.toolbar_location = 'above'
p3.toolbar.logo = None
p3.yaxis.major_label_orientation = "vertical"
p3.xaxis.major_label_orientation = 'vertical'
p3.xaxis.axis_label = "Company"
p3.yaxis.axis_label = "Count"
p3.yaxis.axis_label_text_font_style = "bold"
p3.xaxis.axis_label_text_font_style = "bold"
p3.background_fill_color = "#E0F9F2"
p3.title.text_font_size = '16pt'
p3.title.align = 'center'

p3.tools = [PanTool(), ResetTool()]
hover = HoverTool(tooltips=[("Company", "@x"), ("Count", "@y")])
p3.add_tools(hover)

f = gridplot([[p],[p1],[p2],[p3]])
js, div = components(f)
cdn_jss= CDN.js_files[0]


