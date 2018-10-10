"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta

def on_start(container):
    phantom.debug('on_start() called')
    
    # get the _raw data from splunk
    data = phantom.collect2(container=container, datapath=['artifact:*.cef._raw'])
    data = data[0][0]

    phantom.debug(data)
    split_data = data.split(',')
    data_dict = {}
    custom_dict = {}
    # get a name for the container to update
    container_name = split_data[0]
    del(split_data[0])
    counter = 1
    
    # breaks out the data into items with k,v or additional items with multiple :
    for i in split_data:
        if len(i.split(":")) == 2:
            data_key = i.split(":")[0]
            data_value = i.split(":")[1]
            data_dict[data_key.replace(" ","")] = data_value        
        else:
            custom_dict["cs" + str(counter)] = i
            counter = counter + 1

    phantom.debug(container_name)
    phantom.debug(data_dict)
    phantom.debug(custom_dict)
    
    raw = {}
    # add our artifacts that were easily parsed
    phantom.add_artifact(
        container=container, raw_data=raw, cef_data=data_dict, label='event',
        name='splunk data', severity='low',
        identifier=None,
        artifact_type='network')
    
    # everything else
    phantom.add_artifact(
        container=container, raw_data=raw, cef_data=custom_dict, label='event',
        name='splunk data', severity='low',
        identifier=None,
        artifact_type='network')
    
    # update the name of the container
    update_data = { "name": container_name}
    success, message = phantom.update(container, update_data)
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