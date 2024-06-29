
import base64
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed,NotFound
from . import serializers
import json
import smtplib, threading
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def threaded(func):
    def wrapper(*args,**kwargs):
        threading.Thread(target=func,args=args,kwargs=kwargs).start()
    
    return wrapper

def  get_object_or_404(Model,field_name=None,**fields):
    '''
    Parameters :- 
        a Model as parameter 
    Returns :- 
        object or 404 NotFound along with custom response
    '''
    try:
        return Model.objects.get(**fields)
    except Model.DoesNotExist:
        if field_name:
            raise NotFound({f"{field_name}":"Not found."})
        raise NotFound({f"{Model.__name__}":"Not found."})
    

def get_username_password(encoded_data):
    try:
        original_data = base64.b64decode(base64.b64decode(encoded_data)).decode()
        if original_data:
            username, password = original_data.split(":")
            return username, password
        else:
            raise AuthenticationFailed("authentication failed1")
    except base64.binascii.Error:
        raise AuthenticationFailed("authentication failed2")
    except UnicodeDecodeError:
        raise AuthenticationFailed("authentication failed3")
    except ValueError:
        raise AuthenticationFailed("authentication failed4")