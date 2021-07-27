from flask import request, jsonify, make_response, render_template, Blueprint, redirect

from functools import wraps
from token_manager import TokenManager
import jwt

from datetime import datetime, timedelta

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #start by emptying token
        #print("args request***************************")
        #print(request.args)
        #print("form requests**************************")
        #print(request.form)
        print("openeed token_required")
        token = None

        token_manager = TokenManager()
        #check headers for "Authorization in the header"
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            print("Found Authorization in header")

        #check that token is not empty
        elif request.args.get('myToken', type=str) != "":
            print("got myToken in decorators")
            token = request.args.get('myToken', type=str)

        else:
            #not in header or under "Authorization", so no token
            token = None

        if not token:
            print("token is missing")
            return redirect("/invalid_token")

        #next: attempt to decode the token. Will return nonsense if not encoded with correct priv_key
        try:
            #print("started try block")
            token = token.replace('Bearer ', '', 1)
            #put decoded token into data
            #print("got past token replace")
            token_data = jwt.decode(token, 'SECRET_KEY_123456798', 'HS256')
            #print("extracted token_data")
            # secret key needs to be a stored variable, obviously.

            #should now have data stored in token_data. Add print statement which shoudl output token to Flask
            #print(token_data)

            #get expiry date, check if token is expired
            expiry_time = datetime.strptime(token_data['Expiry'], '%Y-%m-%d %H:%M:%S.%f')
            print(datetime.utcnow())

            if datetime.utcnow() > expiry_time:
                print("Expired token")
                raise
            print("check expiry time done")
            print(token_data.keys())
            #check sql database for token associated with user_nam
            username = token_data['Username']
            print(username)
            user_agent = request.headers['User-Agent']

            print("Going into check_token with: " + token +" "+ username +" "+ user_agent)
            if not token_manager.check_token(token, username, user_agent):
                print("token not in database")
                raise

            print("token check successful")

        except Exception as e:
            print(e)
            return redirect("/invalid_token")

        #assuming previous functions were all passed, should now have confirmed that token is valid, and isn't expired. Can then return the username and everythign else needed for the requesting function
        print("passed decorators")
        return f(token_data['Username'], *args, **kwargs)


    return decorated


def manager_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("opened manager_token_required")
        #start by emptying token
        print("args request***************************")
        print(request.args)
        print("form requests**************************")
        print(request.form)
        token = None

        token_manager = TokenManager()
        #check headers for "Authorization in the header"
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            print("Found Authorization in/ header")

        #check that token is not empty
        elif request.args.get('myToken', type=str) != "":
            print("got myToken in decorators")
            token = request.args.get('myToken', type=str)

        else:
            #not in header or under "Authorization", so no token
            token = None

        if not token:
            return redirect("/invalid_token")

        #next: attempt to decode the token. Will return nonsense if not encoded with correct priv_key
        try:
            print("started try block")
            token = token.replace('Bearer ', '', 1)
            #put decoded token into data
            print("got past token replace")
            token_data = jwt.decode(token, 'SECRET_KEY_123456798', 'HS256')
            print("extracted token_data")
            # secret key needs to be a stored variable, obviously.

            #should now have data stored in token_data. Add print statement which shoudl output token to Flask
            print(token_data)

            #get expiry date, check if token is expired
            expiry_time = datetime.strptime(token_data['Expiry'], '%Y-%m-%d %H:%M:%S.%f')
            print("check expiry time done")
            if datetime.utcnow() > expiry_time:
                print("Expired token")
                raise
            if token_data['Manager'] != "yes":
                print("not a manager")
                raise

            #check sql database for token associated with user_nam
            username = token_data['Username']
            user_agent = request.headers['User-Agent']
            if not token_manager.check_token(token, username, user_agent):
                print("token not in database")
                raise

            print("token check successful")


        except Exception as e:
            print(e)
            return redirect("/invalid_token")


        #assuming previous functions were all passed, should now have confirmed that token is valid, and isn't expired. Can then return the username and everythign else needed for the requesting function
        print("passed decorators")
        return f(token, token_data['Username'], *args, **kwargs)


    return decorated
