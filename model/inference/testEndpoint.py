import requests

url = "http://0.0.0.0:6969/predict/"

files = {'audio_file': open('/home/reis/DeepfakeDetection/audio_samples/35.oga', 'rb')}

response = requests.post(url, files=files)
 
print(response.text)

#print(response.json())