# FlaskServ.py
from flask import Flask, request, abort, render_template, make_response
import queryandmap as qm
app = Flask(__name__)


@app.route("/")
def plot_results():
    connection = qm.connect()
    gdf1, gdf2 = qm.import_dev_site(connection, r'C:\Users\xazzje\Desktop\docAserv\data\study area buffer site.geojson')
      
    # Input parameters
    t = 'test title'
    i = 'M200/19'
    a = 'Jeremy Azzopardi'
    output = qm.produce_outmap([gdf1,gdf2],t, i, a)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    print(response)
    return response
    


    #return render_template('index.html', name = 'vJeremy', out_map = outmap)
    
if __name__ == "__main__":
    app.run(port=8000)
