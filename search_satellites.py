import config
import requests
import xmltodict

class Session:
    """main session class for interacting with the nasa cmr"""
    def __init__(self):
        self.token = None
    
    def get_token(self, username, password):
        token_url = "https://cmr.earthdata.nasa.gov/legacy-services/rest/tokens"
        payload = f"<token><username>{username}</username><password>{password}</password><client_id>search_satellites</client_id><user_ip_address>192.168.1.1</user_ip_address> </token>"
        headers = { 'Content-Type': 'application/xml' }
        resp = requests.post(token_url,data=payload,headers=headers).text
        resp_dict = xmltodict.parse(resp)
        self.token = resp_dict['token']['id']

    
    def delete_token(self):
        token_url = f"https://cmr.earthdata.nasa.gov/legacy-services/rest/tokens/{self.token}"
        headers = { 'Content-Type': 'application/xml' }
        resp = requests.delete(token_url, headers=headers)
        print(resp.status_code)

cmr_session = Session()
cmr_session.get_token(config.earthdata_user, config.earthdata_pass)
print(cmr_session.token)
cmr_session.delete_token()