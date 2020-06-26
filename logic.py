import hashlib

def createIdHash(request_ip):
    return hashlib.sha224(bytes(str(request_ip), "utf-8")).hexdigest()[-16:]

  
