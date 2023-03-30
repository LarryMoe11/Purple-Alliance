import requests, json
from flask import Flask, render_template, request, redirect

global eventCode
eventCode = "2023milak"

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index():
  return render_template('index.html')


@app.route('/events', methods=['GET', 'POST'])
def events():
  if request.method == 'POST':
    eventCode = request.form['eventCode']
    KEY = "1K2AJrKNO9qKz53MjFpFMCIsWFyaLp5JfHKWGqd89y84Ok689RBD1PW6wGV73nP1"
    r = requests.get('https://www.thebluealliance.com/api/v3/event/' + eventCode + '/teams?X-TBA-Auth-Key=' + KEY)

    pullData = {eventCode: r.json()}

    for attrs in pullData[eventCode]:
      if pullData[eventCode] == {'Error': 'event key: ' + eventCode + ' does not exist'}:
        return render_template('index.html')

    EventData = open("eventData.json", "w")
    data = json.dumps(pullData, sort_keys=True, indent=2)
    EventData.write(data)
    EventData.close()

    eventDataList = []
    EventData = open("eventData.json", "r")
    jsonData = json.load(EventData)
    for attrs in jsonData[eventCode]:
      team = attrs["team_number"]
      name = attrs["nickname"]
      eventDataDict = {"team": team, "name": name}
      eventDataList.append(eventDataDict)
    EventData.close()

    dataHTML = "<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>PurpleAlliance - " + eventCode + "</title></head><style> html {height: 100%; width: 100%;}</style><body>" + str(eventDataList) + "</body></html>"

    f = open("templates/" + eventCode + ".html", "w")
    f.write(dataHTML)
    f.close()

    return redirect('/' + eventCode)
  else:  
    return render_template('events.html')

@app.route('/' + eventCode, methods=['GET', 'POST'])
def eventPage():
  return render_template(eventCode + '.html')