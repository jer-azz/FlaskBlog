from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
#from . import queryandmap as qm

bp = Blueprint('docagen', __name__)

@bp.route('/docagen')
def mapgenerator():
    
    return render_template('docagen/mapgen.html')



    
