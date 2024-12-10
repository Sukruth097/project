import http.client 
conn = http.client.HTTPSConnection("docinttesting0713.cognitiveservices.azure.com/") 
headers = { 'Ocp-Apim-Subscription-Key': "8edfb1cd41424654b155cb74ea0b9e3f" } 
conn.request("GET", "formrecognizer/documentClassifiers?api-version=2023-07-31", headers=headers) 
res = conn.getresponse() 
data = res.read() 
print(data.decode("utf-8"))