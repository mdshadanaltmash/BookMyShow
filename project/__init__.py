from flask.helpers import flash, url_for
from werkzeug.wrappers import request
#from werkzeug.utils import redirect
#import project.forms 
#import project.models
#import LoginForm
from flask import Flask,redirect,url_for,flash
from flask.templating import render_template
from flask_login import LoginManager,login_user,logout_user,login_required
from flask_pymongo import PyMongo

app=Flask(__name__)
app.config['SECRET_KEY']='mysecretkey'


##############################################
############# Login Configuration ############
##############################################

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
print(login_manager)

#############################################
############# DATABASE SETUP ################
#############################################

app.config["MONGO_URI"]="mongodb+srv://sadaalt:sadaalt@cluster0.8s1ok.gcp.mongodb.net/BookMyShow?retryWrites=true&w=majority"
mongo=PyMongo(app)