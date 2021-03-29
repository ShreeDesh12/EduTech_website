from flask import render_template, url_for,flash,redirect , request, session, abort
from flaskapp.form import loginForm, registerForm, TelephoneForm, otpForm, loginForm,questionForm, ansForm, uploadCourse
from flaskapp.models import User, Course, Post, Ans, subs
from flaskapp.token import generate_confirmation_token, confirm_token, send_email, generateOTP
from flaskapp import db, login_manager, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from PIL  import Image
from datetime import date
import os

