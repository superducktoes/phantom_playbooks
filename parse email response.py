"""
This playbook is designed to run against a monitored email for yes/no responses. Playbook A should have a last action that sends an email to a user
asking yes or no and send an email with the container name as the subject and then the id of the container.

"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
import email
import requests

def on_start(container):
    phantom.debug('on_start() called')

    # get the entire email from the container 
    raw_email = json.loads(phantom.get_raw_data(container)).get('raw_email')
    
    # parse the body of the email
    #phantom.debug(raw_email)
    msg = email.message_from_string(raw_email)
    email_body = ""
    if msg.is_multipart():
        for payload in msg.get_payload():
            #if payload.is_multipart():
            email_body += str(payload.get_payload())
    else:
        email_body += str(msg.get_payload())
    
    # take action is either yes or no
    take_action = email_body.split("<")[0].rstrip()
    
    # get the container id from the subject of the email
    take_action_container = container.get('name', None).split(" ")[1]
    
    phantom.debug(take_action)
    phantom.debug(take_action_container)
    
    # create our json data to post back to phantom
    playbook_json = {
        "container_id": int(take_action_container),
        "playbook_id": "local/cdm_dashboard",
        "scope": "all",
        "run": True
    }
    
    headers = {
        "ph-auth-token": "Xu/+IgVqEj9gu0einm3JcpoE5Vu15UcS8onVNBV2Awc=",
        "server": "https://192.168.254.138"
    }

    # if the user replies back with a yes run the playbook
    if take_action == "yes":
        run_playbook = requests.post("https://192.168.254.138/rest/playbook_run/",
                                     json=playbook_json,
                                     headers=headers,
                                     verify = False).json()
        phantom.debug(run_playbook)
    
    
    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all detals of actions 
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return