from flask import Flask, request, redirect, session
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests
import uuid
import json


SECRET_KEY = str(uuid.uuid1())
app = Flask(__name__)
app.config.from_object(__name__)

ppl_dict = {}
ppl_dict["_id"] = SECRET_KEY
groups = []

def add_group(retstr, groupnum):
    retstr = retstr + "\n\nHere is your Group " + groupnum+ " option:"
    return retstr

def add_member(retstr, membernum, name, major, year, style):
    style = style.replace("_", " ")
    retstr = retstr + "\n\tMember "+ membernum + "-\n\t\t Name: " + name + "\n\t\t Major: " + major + "\n\t\t Year: " + year + "\n\t\t Study Style: " + style
    return retstr

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    # Increment the counter
    global groups, ppl_dict
    counter = session.get('counter', 0)
    counter += 1
    print('counter')
    print(counter)

    # Save the new counter value in the session
    session['counter'] = counter
    resp = MessagingResponse()

    if counter == 1:
        resp.message("Thank you for choosing Bear Connect! What is your name?")

    elif counter == 2:
        name = request.form['Body']
        ppl_dict["name"] = str(name.lower())
        message = 'Hi {}, what is your major? (e.g. cs, ds, eecs, mims, mids)'.format(name)
        resp.message(message)

    elif counter == 3:
        major = request.form['Body']
        resp.message("What class/Department would you like to find a study group for? (e.g. reply CS61B or INFO253B)")
        ppl_dict["major"] = str(major.lower())

    elif counter == 4:
        class_dept = request.form['Body']
        ppl_dict["selectedClass"] = str(class_dept.lower().replace(" ", ""))
        resp.message("What year are you? (e.g. Freshman, Sophomore, Junior, Senior, Master\'s, PhD)")

    elif counter == 5:
        year = request.form['Body']
        loweredYear = year.lower()
        validYears = ['freshman', 'sophomore', 'junior', 'senior', 'master\'s', 'phd']
        if loweredYear not in validYears:
            counter = 4
            session['counter'] = counter
            resp.message('Input is invalid. What year are you? (e.g. Freshman, Sophomore, Junior, Senior, Master\'s, PhD)')
            return str(resp)
        ppl_dict["year"] = str(loweredYear)
        message = 'Are you an early bird or night owl? Reply 1 for early bird, 2 for night owl'
        resp.message(message)

    elif counter == 6:
        study_time  = request.form['Body']
        if study_time == '1':
            ppl_dict["studyTimes"] = "early_bird"
        elif study_time == '2':
            ppl_dict["studyTimes"] = "night_owl"
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
            ppl_dict["meetingTimes"] = "weekends"
        elif meetingTimes == '2':
            ppl_dict["meetingTimes"] = "weekdays"
        else:
            counter = 6
            session['counter'] = counter
            resp.message('Input is invalid. Do you normally study on weekends or during weekdays? Reply 1 for weekends, 2 for weekdays')
            return str(resp)
        message = 'Which of the following best describe your study style? \n Reply 1 - Debugging Master  \n Reply 2 - Clubhouse Activists \n Reply 3 - Piazza Frontsitter \n Reply 4 - Visualization Guru'
        resp.message(message)

    elif counter == 8:
        studyStyle = request.form['Body']
        if studyStyle == '1':
            ppl_dict["studyStyle"] = "debugging master"
        elif studyStyle == '2':
            ppl_dict["studyStyle"] = "clubhouse activists"
        elif studyStyle == '3':
            ppl_dict["studyStyle"] = "piazza frontsitter"
        elif studyStyle == '4':
            ppl_dict["studyStyle"] = "visualization guru"
        else:
            counter = 7
            session['counter'] = counter
            resp.message('Input is invalid. Which of the following best describe your study style? \n Reply 1 - Debugging Master  \n Reply 2 - Clubhouse Activists \n Reply 3 - Piazza Frontsitter \n Reply 4 - Visualization Guru')
            return str(resp)

        r = requests.post(url='http://host.docker.internal:5001/users/add', json=ppl_dict)
        print(r.status_code)
        print(r.reason)
        resp.message('Awesome! Send any text to continue and then please wait a moment for results')

#display group choices or return a new group
    elif counter == 9:
        reqURL = 'http://host.docker.internal:5001/groups/bestGroups/' + ppl_dict['_id']
        r = requests.get(url=reqURL)

        groups = r.json()
        if len(groups) == 0:
            newGroupData = {"members": [ppl_dict], "open": True, "sizeLimit": "3", "className": ppl_dict["selectedClass"]}
            print("got here")
            r = requests.post(url='http://host.docker.internal:5001/groups/add', json=newGroupData)
            discordURL = r.json()['discordLink']
            resp.message('Unfortunately, we were unable to find any open study groups for your class. We created a new channel for you instead, here is the url: ' + discordURL + ' \n Feel free to invite others to discuss the topic on your mind!')

        else:
            msgStr = "\n"
            for i in range(len(groups)):
                group = groups[i]
                members = group["members"]
                groupNumStr = str(i+1)
                msgStr = add_group(msgStr, groupNumStr)
                for j in range(len(members)):
                    member = members[j]
                    memberNumStr = str(j+1)
                    msgStr = add_member(msgStr, memberNumStr, member["name"], member["major"], member["year"], member["studyStyle"]) + "\n"

            msgStr += "\n Reply the number for the group you'd like to join. e.g. "
            for i in range(len(groups)):
                msgStr += str(i+1)
                if i != len(groups)-1:
                    msgStr += " or "
            resp.message(msgStr)

#a group chosen
    elif counter == 10:
        groupChoice = request.form['Body']
        groupNum = int(groupChoice) - 1

        if groupNum >= len(groups) or groupNum < 0:
            counter = 9
            session['counter'] = counter

            msgStr = "Input is invalid. Reply the number for the group you'd like to join. e.g. "
            for i in range(len(groups)):
                msgStr += str(i+1)
                if i != len(groups)-1:
                    msgStr += " or "
            resp.message(msgStr)
            return str(resp)

        urlID = 'http://host.docker.internal:5001/groups/addUser/' + groups[groupNum]['_id']
        r = requests.put(url=urlID, json = {"user":ppl_dict})
        discordURL = r.json()['discordLink']
        resp.message("Done! You may now find your new group at " + discordURL )


    print(ppl_dict)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
