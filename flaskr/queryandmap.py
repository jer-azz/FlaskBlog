# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 16:53:15 2018

@author: jeremy azzopardi
"""

import psycopg2
import shapely
import shapely.wkt
import geopandas as gpd
import contextily as ctx
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def connect():
    connection = psycopg2.connect(database="HeritageSites",user="postgres", password="admin", port=5433)
    return connection
    
#Import development site for querying
def import_dev_site(connection, fname):
    development_site = gpd.read_file(fname).set_index('id')['geometry']
    dev_site_wkt=shapely.wkt.dumps(development_site[1])
    SQL="SELECT geom, name_mt_1, name_en, type_1, location, id  FROM cultural_map_20_nov_2014_2 WHERE ST_DWithin(cultural_map_20_nov_2014_2.geom, ST_GeomFromText('{}'),4000)".format(dev_site_wkt)

    gdf1 = gpd.read_postgis(SQL, connection, geom_col='geom',crs={'init': u'epsg:3857'}, coerce_float=False)
    gdf2 = gpd.read_file(fname)
    connection.close()
    
    return gdf1,gdf2

# Add basemap
def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
    xmin, xmax, ymin, ymax = ax.axis()
    basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    # restore original x/y limits
    ax.axis((xmin, xmax, ymin, ymax))
        
        
    
  # Create output map
def produce_outmap(geodataframe, title, intervention_code, archaeologist):
    
    # Create image binary which will then be returned by method
    fig=Figure()
    ax = fig.add_subplot()
  
    sites_of_interest = geodataframe[0] # geodataframes[0] contains the results
    dev_site = geodataframe[1] #geodataframe[1] contains the development site
    
    #Add stuff to the plot
    ax = sites_of_interest.plot(color='Red', figsize= (35, 60))
    add_basemap(ax, zoom=15, url=ctx.sources.OSM_A)
    ax.axis('off')
    dev_site.plot(ax=ax, color='blue', edgecolor='black')
    ax.set_title('{} \n {} \n {}'.format(title, intervention_code, archaeologist))
    
    #Add figure to canvas
    canvas = FigureCanvas(fig)
    
    output = io.BytesIO()
    canvas.print_png(output)
    #response = make_response(output.getvalue())
    #response.mimetype = 'image/png'

    
    return output


    
    
    