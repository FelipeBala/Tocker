import requests
try:
    r = requests.get('http://localhost:8080')
    if r.status_code == 200:
        print("Success")
    else:
        print("Error")
except Exception as e:
    print("Error"+str(e))    