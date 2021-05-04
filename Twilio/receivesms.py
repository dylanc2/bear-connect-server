from flask import Flask, request, redirect, session
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests
import uuid
import json



# account_sid = 'AC5f64d1e6b804bf55ed3125b84f93fa2b'
# auth_token = 'cee5beca64a486de2b082834546dcd01'
# client = Client(account_sid, auth_token)
SECRET_KEY = 'a secret key22'
app = Flask(__name__)
app.config.from_object(__name__)


#run this after launching in localhost
#ngrok http 5000

ppl_dict = {}
groups = []

#print (uuid.uuid1())

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    # Increment the counter
    counter = session.get('counter', 0)
    counter += 1
    print('counter')
    print(counter)

    # Save the new counter value in the session
    session['counter'] = counter
    resp = MessagingResponse()

    if counter == 1:
        resp.message("Thank you for choosing Bear Connect! What is your name?")
        ppl_dict["_id"] = str(uuid.uuid1())

    elif counter == 2:
        name = request.form['Body']
        ppl_dict['name'] = name.lower()
        message = 'Hi {}, what is your major? (e.g. cs, ds, eecs)'.format(name)
        resp.message(message)

    elif counter == 3:
        major = request.form['Body']
        resp.message("What class/Department would you like to find a study group for? (e.g. reply CS61B or INFO253B)")
        ppl_dict['major'] = major.lower().replace(" ", "")

    elif counter == 4:
        class_dept = request.form['Body']
        ppl_dict['selectedClass'] = class_dept.lower()
        resp.message("What year are you? (e.g. Freshman, Sophomore, Junior, Senior, Graduate, Other)")

    elif counter == 5:

        year = request.form['Body']
        loweredYear = year.lower()
        validYears = ['freshman', 'sophomore', 'junior', 'senior', 'graduate', 'other']
        if loweredYear not in validYears:
            counter = 4
            session['counter'] = counter
            resp.message('Input is invalid. What year are you? (e.g. Freshman, Sophomore, Junior, Senior, Graduate, Other)')
            return str(resp)
        ppl_dict['year'] = loweredYear
        message = 'Are you an early bird or night owl? Reply 1 for early bird, 2 for night owl'
        resp.message(message)

    elif counter == 6:
        study_time  = request.form['Body']
        if study_time == '1':
            ppl_dict['studyTimes'] = 'early_bird'
        elif study_time == '2':
            ppl_dict['studyTimes'] = 'night_owl'
        else:
            counter = 5
            session['counter'] = counter
            resp.message('Input is invalid. Are you an early bird or night owl? Reply 1 for early bird, 2 for night owl')
            return str(resp)
        message = 'Do you normally study on weekends or during weekdays? Reply 1 for weekends, 2 for weekdays'
        resp.message(message)
    elif counter == 7:
        meetingTimes = request.form['Body']
        if meetingTimes == '1':
            ppl_dict['meetingTimes'] = 'weekends'
        elif meetingTimes == '2':
            ppl_dict['meetingTimes'] = 'weekdays'
        else:
            counter = 6
            session['counter'] = counter
            resp.message('Input is invalid.Do you normally study on weekends or during weekdays? Reply 1 for weekends, 2 for weekdays')
            return str(resp)
        message = 'Which of the following best describe your study style? \n Reply 1 - Debugging Master  \n Reply 2 - Clubhouse Activists \n Reply 3 - Piazza Frontsitter \n Reply 4 - Visualization Guru'
        resp.message(message)
    elif counter == 8:
        studyStyle = request.form['Body']
        if studyStyle == '1':
            ppl_dict['studyStyle'] = 'debugging master'
        elif studyStyle == '2':
            ppl_dict['studyStyle'] = 'clubhouse activists'
        elif studyStyle == '3':
            ppl_dict['studyStyle'] = 'piazza frontsitter'
        elif studyStyle == '4':
            ppl_dict['studyStyle'] = 'visualization guru'
        else:
            counter = 7
            session['counter'] = counter
            resp.message('Input is invalid. Which of the following best describe your study style? \n Reply 1 - Debugging Master  \n Reply 2 - Clubhouse Activists \n Reply 3 - Piazza Frontsitter \n Reply 4 - Visualization Guru')
            return str(resp)

#relative logic
        r = requests.post(url='http://localhost:5001/users/add', json=json.dumps(ppl_dict))
        print(r.status_code)
        print(r.reason)
        resp.message('Awesome! Send any text to continue and then please wait a moment for results')

#display group choices or return a new group
    elif counter == 9:
        r = requests.get(url='http://localhost:5001/groups/bestMatches', params=ppl_dict['_id'])
        data = r.json()
        groups = data['groups']
        # if len(data['groups']) == 0:
            # r = requests.post(url='http://localhost:5001/groups/startNew', json=json.dumps({"members": }))
            # discordURL = r.json()['discordLink']
            # resp.message('Ok, we created a new channel for ya! Here is the url: ' + discordURL + 'Feel free to invite others to discuss the topic on your mind!')

        # TODO: format output strings displaying group choices
        group1 = groups[0]
        group2 = groups[1]
        group3 = groups[2]

#a group chosen
    elif counter == 10:
        groupChoice = request.form['Body']
        if groupChoice == '1':
            urlID = 'http://localhost:5001/groups/' + groups[0]['groupID']
            r = requests.put(url=urlID, json = json.dumps({"userID":ppl_dict["id"]}))
            discordURL = r.json()['discordLink']
            resp.message("Done! You may now find your new group at " + discordURL )

        elif groupChoice == '2':
            urlID = 'http://localhost:5001/groups/' + groups[0]['groupID']
            r = requests.put(url=urlID, json = json.dumps({"userID":ppl_dict["id"]}))
            discordURL = r.json()['discordLink']
            resp.message("Done! You may now find your new group at " + discordURL )

        elif groupChoice == '3':
            urlID = 'http://localhost:5001/groups/' + groups[0]['groupID']
            r = requests.put(url=urlID, json = json.dumps({"userID":ppl_dict["id"]}))
            discordURL = r.json()['discordLink']
            resp.message("Done! You may now find your new group at " + discordURL )

    print(ppl_dict)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
