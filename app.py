from flask import Flask, jsonify, request, make_response
from aws_controller import TrackingPlansTable, EventsTable
from flask_cors import CORS, cross_origin

tracking_plans_table = TrackingPlansTable()
events_table = EventsTable()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/tracking_plans/', methods=['GET', 'POST', 'DELETE', 'PUT'])
@cross_origin()
def tracking_plans():
    if request.method == 'GET':
        plan_id = request.args.get('plan_id', None)
        plans = tracking_plans_table.get_item(plan_id)
        if plan_id:
            return jsonify(enrich_with_event_defs(plans))
        compund_plans = []
        for plan in plans:
            compund_plan = enrich_with_event_defs(plan)
            compund_plans.append(compund_plan)
        return jsonify(compund_plans)

    elif request.method == 'DELETE':
        plan_id = request.args.get('plan_id')
        return jsonify(tracking_plans_table.delete_item(plan_id))
    elif request.method == 'PUT':
        data = request.get_json()
        if 'PlanId' not in data:
            return make_response(f'Invalid payload. Primary key: `PlanId` missing', 422)
        for key in data.keys():
            if key not in ('display_name', 'rules', 'PlanId'):
                return make_response(f'Invalid field {key}', 422)
        return jsonify(tracking_plans_table.update_item(data))
    elif request.method == 'POST':
        data = request.get_json()
        for key in data.keys():
            if key not in ('display_name', 'rules'):
                return make_response(f'Invalid field {key}', 422)
        if 'events' in data.get('rules', {}):
            for event in data['rules']['events']:
                events_table.put(event)
        return jsonify(tracking_plans_table.put(data))



@app.route('/events/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def events():
    if request.method == 'GET':
        event_name = request.args.get('name', None)
        return jsonify(events_table.get_item(event_name))
    elif request.method == 'DELETE':
        event_name = request.args.get('name')
        return jsonify(events_table.delete_item(event_name))
    elif request.method == 'PUT':
        if 'name' not in data:
            return make_response(f'Invalid payload. Primary key: `name` missing', 422)
        for key in data.keys():
            if key not in ('name', 'rules', 'description'):
                return make_response(f'Invalid field {key}', 422)
        data = request.get_json()
        return jsonify(events_table.update_item(data))
    elif request.method == 'POST':
        if 'name' not in data:
            return make_response(f'Invalid payload. Primary key: `name` missing', 422)
        for key in data.keys():
            if key not in ('name', 'rules', 'description'):
                return make_response(f'Invalid field {key}', 422)
        data = request.get_json()
        return jsonify(events_table.put(data))

def enrich_with_event_defs(plan: dict) -> dict:
    compund_plan = {'PlanId': plan['PlanId'],
            'display_name': plan['display_name'],
            'rules': {'events': []}
            }
    for event_name in plan['events']:
        event_definition = events_table.get_item(event_name)
        compund_plan['rules']['events'].append(event_definition)
    return compund_plan


if __name__ == '__main__':
    app.run()