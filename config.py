
with open('config.init.txt','r') as file:

  apiKey = file.readline().split("=",1)[1].strip()
  apiSecret = file.readline().split("=",1)[1].strip()
  
apiKey = apiKey
apiSecurity = apiSecret
