import config
import requests

class Session:
    """main session class for interacting with the nasa cmr"""
    def __init__(self):
        self.token = None
    
    def get_token(self, username, password):
        token_url = "https://cmr.earthdata.nasa.gov/legacy-services/rest/tokens"
        payload = f"<token><username>{username}</username><password>{password}</password><client_id>search_satellites</client_id><user_ip_address>192.168.1.1</user_ip_address> </token>"
        headers = { 'Content-Type': 'application/xml' }
        self.token = requests.post(token_url,data=payload,headers=headers).text

cmr_session = Session()
cmr_session.get_token(config.earthdata_user, config.earthdata_pass)
print(cmr_session.token)