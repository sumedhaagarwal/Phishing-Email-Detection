from googleapiclient.discovery import build
import pprint

my_api_key = "AIzaSyBbRo__OeXIcxBo1329fu3-lj1UhHhjyKo"
my_cse_id = "014113642853987699976:f_egv3a8x6a"

def google_search(search_term, api_key, cse_id, **kwargs):
    ans = []
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs,start=1).execute()
        results = res['items']
        for result in results:
        	ans.append(result['link'])

        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs,start=11).execute()
        results = res['items']
        for result in results:
        	ans.append(result['link'])

        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs,start=21).execute()
        results = res['items']
        for result in results:
        	ans.append(result['link'])
    except:
        pass
    return ans
