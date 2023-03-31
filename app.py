import requests, json
from flask import Flask, render_template, request, redirect

global eventCode
# eventCode = "2023isde1"

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
    data = json.dumps(pullData)
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

    dataLength = len(data)
    eventCodeLength = len(eventCode)
    htmlData = data[eventCodeLength + 6:dataLength - 2]
    dataHTML = """
<!DOCTYPE html>
<html>

<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width'>
  <title>PurpleAlliance - 2023milak</title>
</head>
<style>
  html {
    height: 100%;
    width: 100%;
  }
</style>

<body>
  <link href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css' rel='stylesheet'>
  <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js'></script>
  <script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'></script>
  <script type='text/javascript'>
    var data = [""" + htmlData + """];
    $(document).ready(function () {
      var html = '<table class="table table-striped">';
      html += '<tr>';
      var flag = 0;
      $.each(data[0], function (index, value) {
        html += '<th>' + index + '</th>';
      });
      html += '</tr>';
      $.each(data, function (index, value) {
        html += '<tr>';
        $.each(value, function (index2, value2) {
          html += '<td>' + value2 + '</td>';
        });
        html += '<tr>';
      });
      html += '</table>';
      $('body').html(html);
    });
  </script>
</body>

</html>
    """

    f = open("templates/" + eventCode + ".html", "w")
    f.write(dataHTML)
    f.close()

    return redirect('/event/' + eventCode)
  else:  
    return render_template('events.html')

@app.route('/event/<path:event_id>', methods=['GET', 'POST'])
def eventPage(event_id):
  return render_template(event_id + '.html')