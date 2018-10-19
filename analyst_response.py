"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta

##############################
# Start - Global Code Block

import requests

# End - Global Code block
##############################

def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'promote_to_case_1' block
    promote_to_case_1(container=container)

    return

def promote_to_case_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('promote_to_case_1() called')

    phantom.promote(container=container, template="responses")
    get_case_note_count(container=container)

    return

def get_case_note_count(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('no_op_1() called')
    
    # get the container id and phantom url to format for the request
    container_id = container.get('id', None)
    phantom_url = phantom.get_base_url()
    request_url = "{}/rest/container/{}/phases".format(str(phantom_url), str(container_id))
    
    # make the request
    r = requests.get(request_url, auth=("admin","password"), verify=False).json()
    
    # check to see if all notes fields are filled out
    notes_counter = 0
    for i in r["data"][0]["tasks"]:
        phantom.debug(i)
        if i["notes"]:
            notes_counter = notes_counter + 1

    # if all the fields are filled out prompt before emailing, if not sleep and check again
    if notes_counter != 3:
        no_op_2(container=container, handle=notes_counter)
    else:
        for i in r["data"][0]["tasks"]:
            raw = {}
            cef = {}
            cef['container_note'] = i["notes"][0]["content"]
    
            success, message, artifact_id = phantom.add_artifact(
                container=container, raw_data=raw, cef_data=cef, label='note',
                name='container note', severity='low',
                identifier=None,
                artifact_type='note')
        
        prompt_1(container=container)

    return

def send_email_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('send_email_1() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'send_email_1' call
    formatted_data_1 = phantom.get_format_data(name='format_1')

    parameters = []
    
    # build parameters list for 'send_email_1' call
    parameters.append({
        'body': formatted_data_1,
        'from': "",
        'attachments': "",
        'to': "niroy@splunk.com",
        'cc': "",
        'bcc': "",
        'headers': "",
        'subject': "Test Container Note",
    })

    phantom.act("send email", parameters=parameters, assets=['smtp'], name="send_email_1")

    return

def no_op_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    # handle passes count from the previous get_case_note_count
    
    phantom.debug('no_op_2() called')
    
    parameters = []
    
    # build parameters list for 'no_op_2' call
    parameters.append({
        'sleep_seconds': 10,
    })
    
    phantom.act("no op", parameters=parameters, assets=['local phantom'], callback=get_case_note_count, name="no_op_2", parent_action=action)
    return

def prompt_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('prompt_1() called')
    
    # set user and message variables for phantom.prompt call
    user = "admin"
    message = """is there enough information to send out"""

    # response options
    options = {
        "type": "list",
        "choices": [
            "Yes",
            "No",
        ]
    }

    phantom.prompt(container=container, user=user, message=message, respond_in_mins=30, name="prompt_1", options=options, callback=decision_2)

    return

def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('decision_2() called')

    # check for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["prompt_1:action_result.summary.response", "==", "Yes"],
        ])

    # call connected blocks if condition 1 matched
    if matched_artifacts_1 or matched_results_1:
        format_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    # call connected blocks for 'else' condition 2

    return

def format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('format_1() called')
    
    template = """{0}"""

    # parameter list for template variable replacement
    parameters = [
        "artifact:*.cef.container_note",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_1")

    send_email_1(container=container)

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