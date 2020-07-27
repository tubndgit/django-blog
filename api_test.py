# -*- coding: utf-8 -*-
"""
HOW TO USE

python manage.py generateschema > static/openapi-schema.yml

#1 - Get token
python api_test.py --opt=1

#2 - Refresh token
python api_test.py --opt=2

#3 - Get all posts
python api_test.py --opt=3

#4 - Get a post
python api_test.py --opt=4 --id=1

#5 - Add a post
python api_test.py --opt=5

#6 - Update a post
python api_test.py --opt=6 --id=5

#7 - Delete a post
python api_test.py --opt=7 --id=5

"""
import os
import string, json
import sys
import argparse
from pprint import pprint
import requests
import uuid

user = 'username'
passwd = 'password'

main_api = 'http://127.0.0.1:8000'

def read_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        f.close()
    return content

def get_token():
    try:
        token = read_file('token.txt')
        return token
    except:
        return ''

def test(args):
    token = get_token()
    headers = {'Authorization': 'Bearer {}'.format(token)}
    if args.opt:

        opt = int(args.opt)

        # Get token
        if opt == 1:                        

            # Get access token
            myobj = {
                "username": user,
                "password": passwd
            }
            token_api = main_api + '/api/token/'
            r1 = requests.post(token_api, json=myobj, headers={'Content-Type': 'application/json'})    
            print(r1.status_code)        
            json_data = json.loads(r1.text)
            print(json_data)

        # Refresh token
        if opt == 2:
            myobj = {
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU5NDE3NDcyNCwianRpIjoiNzAyMjcyNWM1ODE1NDVkMjliNzliODc0YmUyMjQ0NjciLCJ1c2VyX2lkIjoyfQ.eQb6_h9kmpUHrRZsICcTMjjmKZeEj2AQCStjQKsPTJs"
            }        
            
            # Get access token
            token_api = main_api + '/api/token/refresh/'
            r1 = requests.post(token_api, json=myobj, headers={'Content-Type': 'application/json'})  
            print(r1.status_code)         
            json_data = json.loads(r1.text)
            print(json_data)

        # Get all posts
        if opt == 3:            
            url = main_api + '/api/post/'

            # Get access token
            # Get access token
            myobj = {
                "username": user,
                "password": passwd
            }
            token_api = main_api + '/api/token/'
            r1 = requests.post(token_api, json=myobj, headers={'Content-Type': 'application/json'})            
            print(r1.status_code)
            json_data = json.loads(r1.text)
            try:
                token = json_data['access']
                #headers = {'Authorization': 'Bearer {}'.format(token)}
                headers = {}

                r = requests.get(url, headers = headers)
                print("Status Code: {}".format(r.status_code))
                pprint(json.loads(r.text))
            except:
                print(json_data)

        # Get a post
        if opt == 4:            
            _id = args.id
            url = main_api + '/api/post/{}'.format(_id)
            
            # Get access token
            myobj = {
                "username": user,
                "password": passwd
            }
            token_api = main_api + '/api/token/'
            r1 = requests.post(token_api, json=myobj, headers={'Content-Type': 'application/json'})            
            print(r1.status_code)
            json_data = json.loads(r1.text)
            try:
                token = json_data['access']
                #headers = {'Authorization': 'Bearer {}'.format(token)}
                headers = {}

                r = requests.get(url, headers = headers)
                print("Status Code: {}".format(r.status_code))
                pprint(json.loads(r.text))
            except:
                print(json_data)

        # Add a post
        if opt == 5:
            uid = uuid.uuid1()
            data = { 
                "title": "testing add post via api {}".format(uid),
                "slug": "testing-add-post-via-api-{}".format(uid),
                "author": 1,
                "status": 1,
                "meta_description": "meta description",
                "category": 1,
                "tag": [1, 2]               
            }
                        
            url = main_api + '/api/post/'
            
            # Get access token
            myobj = {
                "username": user,
                "password": passwd
            }
            token_api = main_api + '/api/token/'
            r1 = requests.post(token_api, json=myobj, headers={'Content-Type': 'application/json'})            
            print(r1.status_code)
            json_data = json.loads(r1.text)
            try:
                token = json_data['access']
                headers = {'Authorization': 'Bearer {}'.format(token)}
                #headers = {}

                r = requests.post(url, json = data, headers = headers)
                print("Status Code: {}".format(r.status_code))
                pprint(json.loads(r.text))
            except:
                print(json_data)


        # Update a post
        if opt == 6:
            uid = uuid.uuid1()
            data = {                 
                "content": "Update post",                
                "meta_description": "Update meta description",
                "category": 2,
                "tag": [2, 3]               
            }
                        
            _id = args.id
            url = main_api + '/api/post/{}'.format(_id)
            
            # Get access token
            myobj = {
                "username": user,
                "password": passwd
            }
            token_api = main_api + '/api/token/'
            r1 = requests.post(token_api, json=myobj, headers={'Content-Type': 'application/json'})            
            print(r1.status_code)
            json_data = json.loads(r1.text)
            try:
                token = json_data['access']
                headers = {'Authorization': 'Bearer {}'.format(token)}
                #headers = {}

                r = requests.put(url, json = data, headers = headers)
                print("Status Code: {}".format(r.status_code))
                pprint(json.loads(r.text))
            except:
                print(json_data)

        # Delete a post
        if opt == 7:
            _id = args.id
            url = main_api + '/api/post/{}'.format(_id)
            
            # Get access token
            myobj = {
                "username": user,
                "password": passwd
            }
            token_api = main_api + '/api/token/'
            r1 = requests.post(token_api, json=myobj, headers={'Content-Type': 'application/json'})            
            print(r1.status_code)
            json_data = json.loads(r1.text)
            try:
                token = json_data['access']
                headers = {'Authorization': 'Bearer {}'.format(token)}
                #headers = {}

                r = requests.delete(url, headers = headers)
                print("Status Code: {}".format(r.status_code))
                pprint(json.loads(r.text))
            except:
                print(json_data)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command lines')
    parser.add_argument('--opt', metavar='path', required=True, 
                        help="Option")
    parser.add_argument('--id', metavar='path', required=False, 
                        help="id")

    args = parser.parse_args()    
    test(args)