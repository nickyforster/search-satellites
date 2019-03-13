import config
import requests
import xmltodict

class Session:
    """main session class for interacting with the nasa cmr"""
    def __init__(self):
        self.token = None
        self.client_id = 'AP-search-satellites'
    
    def get_token(self, username, password):
        token_url = "https://cmr.earthdata.nasa.gov/legacy-services/rest/tokens"
        payload = f"<token><username>{username}</username><password>{password}</password><client_id>{self.client_id}</client_id><user_ip_address>192.168.1.1</user_ip_address> </token>"
        headers = { 'Content-Type': 'application/xml' }
        resp = requests.post(token_url,data=payload,headers=headers).text
        resp_dict = xmltodict.parse(resp)
        self.token = resp_dict['token']['id']

    def delete_token(self):
        token_url = f"https://cmr.earthdata.nasa.gov/legacy-services/rest/tokens/{self.token}"
        headers = { 'Content-Type': 'application/xml' }
        resp = requests.delete(token_url, headers=headers)
        resp_code = resp.status_code
        if resp_code == 204:
            print('token deleted')
        else:
            print('couldn\'t delete token')
    
    ## There are three different environments for the CMR system
    ## Systems Integration Test, User Acceptance Test and Operations/Production
    ## We're using Operations/Production (open to users around the world) – https://cmr.earthdata.nasa.gov/
    ## query params: page_size, page_num, offset, scroll, sort_key, pretty, token, echo_compatible
    ## You can find collections a lot of different ways, we'll start with temporal and bounds
    ## The temporal datetime has to be in yyyy-MM-ddTHH:mm:ssZ format, range is inclusive for bounds default

    def search(self):
        search_collection_url = "https://cmr.earthdata.nasa.gov/search/collections"
        headers = {
            # 'Content-Type': 'application/json',
            'Echo-Token': self.token,
            'Accept': 'application/json',
            'Client-Id': self.client_id
        }
        payload = {
            'temporal': '1980-07-16T00:00:00Z,1985-07-16T00:00:00Z'
        }
        resp = requests.post(search_collection_url, headers=headers, data=payload).json()
        print(resp)

cmr_session = Session()
cmr_session.get_token(config.earthdata_user, config.earthdata_pass)
cmr_session.search()
cmr_session.delete_token()