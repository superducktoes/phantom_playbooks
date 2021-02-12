"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
##############################
# Start - Global Code Block

def workbook_classifier(notable_name):
    
    workbook_choices = {
        "ESCU - Access LSASS Memory for Dump Creation - Rule": "Response Template 1",
        "ESCU - Detect Credential Dumping through LSASS access - Rule": "Response Template 1",
        "Emotet Malware DHS Report TA18-201A": "Self-Replicating Malware",
        "Suspicious DNS Traffic": "Network Indicator Enrichment"
    }
    
    phantom_workbook = workbook_choices[notable_name]
    
    if(phantom_workbook == ""):
        phantom_workbook = "Response Template 1"
    
    return phantom_workbook

# End - Global Code block
##############################

def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'promote_to_case_1' block
    promote_to_case_1(container=container)

    return

def promote_to_case_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('promote_to_case_1() called')
    
    workbook_template = workbook_classifier(container["name"])
    
    phantom.promote(container=container, template=workbook_template)

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all details of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return