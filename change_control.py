"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta

def on_start(container):
    phantom.debug('on_start() called')
    phantom.set_action_limit(15)
    # call 'create_ticket_1' block
    create_ticket_1(container=container)

    return

def create_ticket_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('create_ticket_1() called')

    # collect data for 'create_ticket_1' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.destinationAddress', 'artifact:*.id'])

    parameters = []
    
    # build parameters list for 'create_ticket_1' call
    for container_item in container_data:
        parameters.append({
            'short_description': "IP Block Request",
            'table': "incident",
            'vault_id': "",
            'description': container_item[0],
            'fields': "",
            # context (artifact id) is added to associate results with the artifact
            'context': {'artifact_id': container_item[1]},
        })

    phantom.act("create ticket", parameters=parameters, assets=['service now'], callback=join_get_ticket_1, name="create_ticket_1")

    return

def get_ticket_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('get_ticket_1() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'get_ticket_1' call
    results_data_1 = phantom.collect2(container=container, datapath=['create_ticket_1:action_result.summary.created_ticket_id', 'create_ticket_1:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []
    
    # build parameters list for 'get_ticket_1' call
    for results_item_1 in results_data_1:
        if results_item_1[0]:
            parameters.append({
                'id': results_item_1[0],
                'table': "incident",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': results_item_1[1]},
            })
    # calculate start time using delay of 1 minutes
    start_time = datetime.now() + timedelta(minutes=1)
    
    # print out the time to copy to ticket to use as example change control window
    phantom.debug(start_time)
    phantom.act("get ticket", parameters=parameters, assets=['service now'], callback=decision_1, start_time=start_time, name="get_ticket_1", parent_action=action)

    return

def join_get_ticket_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('join_get_ticket_1() called')

    # check if all connected incoming actions are done i.e. have succeeded or failed
    if phantom.actions_done([ 'create_ticket_1' ]):
        
        # call connected block "get_ticket_1"
        get_ticket_1(container=container, handle=handle)
    
    return

def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('decision_1() called')

    # check for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["get_ticket_1:action_result.data.*.close_notes", "==", ""],
        ])

    # call connected blocks if condition 1 matched
    if matched_artifacts_1 or matched_results_1:
        join_get_ticket_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    # call connected blocks for 'else' condition 2
    add_artifact_1(action=action, success=success, container=container, results=results, handle=handle)

    return

def update_ticket_success(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('update_ticket_success() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'update_ticket_success' call
    results_data_1 = phantom.collect2(container=container, datapath=['create_ticket_1:action_result.summary.created_ticket_id', 'create_ticket_1:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []
    
    # build parameters list for 'update_ticket_success' call
    for results_item_1 in results_data_1:
        if results_item_1[0]:
            parameters.append({
                'table': "incident",
                'vault_id': "",
                'id': results_item_1[0],
                'fields': "{\"state\":7, \"work_notes\":\"Successfully blocked ip\"}",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': results_item_1[1]},
            })

    phantom.act("update ticket", parameters=parameters, assets=['service now'], name="update_ticket_success")

    return

def block_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('block_ip_1() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'block_ip_1' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.destinationAddress', 'artifact:*.id'])
    time_to_block = phantom.collect2(container=container, datapath=['artifact:*.cef.time_to_block'])
    for i in time_to_block:
        if i[0]:
            start_time = i[0]

    parameters = []
    
    # build parameters list for 'block_ip_1' call
    for container_item in container_data:
        if container_item[0]:
            parameters.append({
                'ip_hostname': "10.0.0.75",
                'remote_ip': container_item[0],
                'remote_port': "",
                'protocol': "all",
                'direction': "Out",
                'comment': "",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': container_item[1]},
            })

    phantom.act("block ip", parameters=parameters, assets=['raspberry pi'], callback=decision_3, start_time=datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f"), name="block_ip_1", parent_action=action)

    return

def add_artifact_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('add_artifact_1() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'add_artifact_1' call
    results_data_1 = phantom.collect2(container=container, datapath=['get_ticket_1:action_result.data.*.close_notes', 'get_ticket_1:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []
    
    # build parameters list for 'add_artifact_1' call
    for results_item_1 in results_data_1:
        parameters.append({
            'container_id': "",
            'name': "time to add",
            'contains': "",
            'source_data_identifier': "1",
            'label': "event",
            'cef_value': results_item_1[0],
            'cef_name': "time_to_block",
            'cef_dictionary': "",
            # context (artifact id) is added to associate results with the artifact
            'context': {'artifact_id': results_item_1[1]},
        })

    phantom.act("add artifact", parameters=parameters, assets=['local phantom'], callback=block_ip_1, name="add_artifact_1")

    return

def decision_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('decision_3() called')

    # check for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["block_ip_1:action_result.status", "==", "success"],
        ])

    # call connected blocks if condition 1 matched
    if matched_artifacts_1 or matched_results_1:
        update_ticket_success(action=action, success=success, container=container, results=results, handle=handle)
        return

    # call connected blocks for 'else' condition 2
    update_ticket_error(action=action, success=success, container=container, results=results, handle=handle)

    return

def update_ticket_error(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('update_ticket_error() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'update_ticket_error' call
    results_data_1 = phantom.collect2(container=container, datapath=['create_ticket_1:action_result.summary.created_ticket_id', 'create_ticket_1:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []
    
    # build parameters list for 'update_ticket_error' call
    for results_item_1 in results_data_1:
        if results_item_1[0]:
            parameters.append({
                'table': "incident",
                'vault_id': "",
                'id': results_item_1[0],
                'fields': "{\"work_notes\":\"error blocking ip\"}",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': results_item_1[1]},
            })

    phantom.act("update ticket", parameters=parameters, assets=['service now'], name="update_ticket_error")

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