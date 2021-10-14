from flask import Flask, request, redirect
import random
import string

dict1 = {} 
dict2 = {}  
dict3 = {} 

flask_application = Flask(__name__)

def three_digit_code_gen():
    letters = string.ascii_lowercase
    while True:
        three_letters = random.choices(letters, k=3)
        three_letters = "".join(three_letters)
        if not three_letters in dict2:
            return three_letters

@flask_application.route('/<url>')
def redirection(url):
    if url not in dict2: return "URL does not exist" + '\n'
    long_url = dict2[url]
    dict3[url] += 1
    return redirect("".join(long_url))

@flask_application.route('/shorten', methods = ['POST'])
def shorten():
    if request.headers['Content-Type'] == 'text/plain':
        code = three_digit_code_gen()
        long_url = (request.data).decode('ascii')
        if long_url in dict1: return "New URL: 127.0.0.1:5000/" + str(dict1[long_url])[2:-2] + '\n'
        dict3[code] = 0
        dict1[long_url] = [code]
        dict2[code] = [long_url]
        return "New URL: 127.0.0.1:5000/" + code + '\n'

@flask_application.route('/retrieve/<x>/<url>', methods = ['GET'])
def long_url_display(x, url):
    if url in dict2: 
        return 'Long URL: ' + str(dict2[url])[2:-2] + '\n'
    else: return "URL does not exist" + '\n'

@flask_application.route('/update/<x>/<code>', methods = ['PATCH'])
def update_short_url(x, code):
    if code in dict3: 
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            dict3[code] = data['clicks']
            return "Count: " + str(data['clicks']) + '\n'
    else: return "URL does not exist" + '\n'

@flask_application.route('/clicks/<x>/<short>', methods = ['GET'])
def get_clicks(x, short):
    if short in dict3: 
        return 'Clicks: ' + str(dict3[short]) + '\n'   
    else: return "URL does not exist" + '\n'
    
if __name__ == '__main__':
    flask_application.run(port=5000, debug=True)
