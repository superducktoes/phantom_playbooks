"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
results_dict = {}

# add information from the results_dict to the container
def add_results_to_container(container):
    cef = results_dict
    raw = {}
    success, message, artifact_id = phantom.add_artifact(
        container=container, raw_data=raw, cef_data=cef, label='aws',
        name='AWS SNS Message', severity='medium',
        identifier=None,
        artifact_type='aws')
    
    phantom.error("=== success/error status message ===")
    phantom.debug(success)
    phantom.error(message)
    return success

# parse and flatten the json to store in results_dict
def parse_json(d):
    for k, v in d.items():
        if isinstance(v, dict):
            parse_json(v)
        else:
            key = "{0}".format(k)
            value = "{0}".format(v)
            results_dict.update({key:value})
            
def on_start(container):
    import email
    phantom.debug('on_start() called')
    raw_email = json.loads(phantom.get_raw_data(container)).get('raw_email')
    b = email.message_from_string(raw_email)
    # parse the email to get the body of the email
    if b.is_multipart():
        email_message = b.get_payload()[0]
        for part in email_message.walk():
            payload = part.get_payload() #returns a bytes object
            payload = json.loads(payload, strict=False)
            phantom.error("=== email payload ===")
            phantom.debug(payload)
            parse_json(payload)
    else:
        phantom.debug("=== not multipart ===")
        phantom.error(b.get_payload())
        payload = b.get_payload()
        parse_json(payload)
    
    phantom.error("=== results dict ===")
    phantom.debug(results_dict)
    add_results_to_container(container)
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