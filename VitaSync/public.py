from flask import *
from flask import Blueprint
from database import *
import os

public = Blueprint('public',__name__)

@public.route('/')
def hame():
    return render_template('register.html')

@public.route('/login')
def login():
    return render_template('admin_h.html')


@public.route('/demo')
def demo():
    return render_template('demo.html')
