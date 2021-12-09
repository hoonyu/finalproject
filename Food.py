import urllib.parse, urllib.request, urllib.error, json

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

baseurl = 'https://api.fda.gov/food/event.json'

#headers= {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'}
# param = {'search': 'products.industry_code:23&limit=1'}
# response = request.get(baseurl, headers= headers, param = param)
# x = response.text
# print(x)
params = {
    "api_key":"IlDlqwrlzh9xba19FKUXIEProVupzHfcmC0Ae4bU",
    'search':'products.industry_code:23',
    'limit' : 5
}

adding = urllib.parse.urlencode(params)

foodadd = baseurl + "?" + adding



#req = urllib.request.Request(foodadd, headers=headers)
r = urllib.request.urlopen(foodadd)



fooding = r.read()

food = json.loads(fooding)

food = pretty(food)

print(food)

