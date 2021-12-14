import urllib.parse, urllib.request, urllib.error, json, jinja2

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request." )
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None



def foodREST(baseurl = 'https://api.fda.gov/food/event.json',
    api_key = "IlDlqwrlzh9xba19FKUXIEProVupzHfcmC0Ae4bU",
    search = "BANANA",
    count = "reactions.exact",
    limit = 3,
    params={},
    ):
    params['api_key'] = api_key
    params['search'] = search
    params['count'] = count
    params['limit'] = limit
    url = baseurl + "?" + urllib.parse.urlencode(params)
    return safe_get(url)









def foodLimit(countType, term, limitNum):
    r = foodREST(count=countType,search=term, limit=limitNum)
    limitInfo = r.read()
    finalInfo = json.loads(limitInfo)
    focus = len(finalInfo["results"])
    return(focus)


def foodSearch(countType,term,limitNum):
    if countType == 'no reaction':
        return("Sorry. " + countType + " results. Please check off the reaction")
    if countType == 'no outcome':
        return("Sorry. " + countType + " results. Please check off the outcome")
    else:
        actualMaxNum = foodLimit(countType=countType, term=term, limitNum=1000)
        if limitNum > actualMaxNum:
            limitNum = actualMaxNum
        r = foodREST(count=countType, search=term, limit=limitNum)
        fooding = r.read()
        food = json.loads(fooding)
        foodlist = []
        if len(food["results"]) >= limitNum:
            for num in range(len(food["results"])):
                foodlist.append(str(num+1) + ") " + (food["results"][num]["term"]).lower() + " - " +
                    str(food["results"][num]["count"]) + " counts")
        listString = ""
        for result in foodlist:
            listString = listString + result + "<br>"
        return(listString)




def food_URL_Maker(stringObject):
    object = stringObject.split()
    firstWord = object[1]
    link = "https://www.google.com/search?q=" + str(firstWord)
    return(link)



def noName():
    return("Please type in the name of the food")








from flask import Flask, render_template, request
import logging

app = Flask(__name__)

@app.route("/")
def main_handler():
    return render_template('index.html')

@app.route("/response")
def food_input_handler():
    foodName = request.args.get('food')
    if foodName =="":
        tryAgain = noName()
        return render_template('index.html', askForName=tryAgain)
    limitNumber = request.args.get('limit')
    reactionCheck = request.args.get('reactions')
    outcomeCheck = request.args.get('outcomes')

    if limitNumber == "":
        limitNumber = 5

    countTyping = ''
    secCountTyping =''

    if reactionCheck:
        countTyping = 'reactions.exact'
    else:
        countTyping = 'no reaction'
    if outcomeCheck:
        secCountTyping = 'outcomes.exact'
    else:
        secCountTyping = 'no outcome'

    reactionOutput = foodSearch(countType=countTyping,term=foodName, limitNum=int(limitNumber))
    outcomeOutput = foodSearch(countType=secCountTyping, term=foodName, limitNum=int(limitNumber))

    print(reactionOutput)

    firstLink = ""

    if reactionOutput != "Sorry. no reaction results. Please check off the reaction":
        firstLink = food_URL_Maker(reactionOutput)

    return render_template('index.html', result=reactionOutput, secResult=outcomeOutput,
                           reactionLink=firstLink)





if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)





























