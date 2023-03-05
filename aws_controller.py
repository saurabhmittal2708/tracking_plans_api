import boto3
from typing import List, Optional, Tuple
from decouple import config
import uuid


AWS_ACCESS_KEY_ID     = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME           = config("REGION_NAME")

client = boto3.client(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)
resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)

TRACKING_PLANS_TABLE='Tracking_Plans'
EVENTS_TABLE = 'Events'

TrackingPlansRes = resource.Table(TRACKING_PLANS_TABLE)
EventsRes = resource.Table(EVENTS_TABLE)
PAGE_SIZE = 50

def generate_key():
    uuid_str = uuid.uuid1()
    return str(uuid_str)

class DynamoDBTable:
    def __init__(self, table_name, primary_key):
      self.table = resource.Table(table_name)
      self.primary_key = primary_key
    
    def get_item(self, primary_key_value: Optional[str] = None):
        if primary_key_value:
            res = self.table.get_item(
                Key={
                    self.primary_key: primary_key_value
                }
            )
            if 'Item' in res:
                return res['Item']
            else:
                return []
        else:
            res = self.table.scan()
            if 'Items' in res:
                return res['Items']
            else:
                return []
    def delete_item(self, primary_key_value: str):
        return self.table.delete_item(
            Key={
                self.primary_key: primary_key_value
            }
        )
    def update_item(self, data: dict):
        return self.table.update_item(
            Key={
                self.primary_key: data[self.primary_key]
            },
            AttributeUpdates={
            key: {
                'Value'  : val,
                'Action' : 'PUT'
            } for key, val in data.items() if key != self.primary_key
        },
        ReturnValues = "UPDATED_NEW"
    )


class TrackingPlansTable(DynamoDBTable):
    def __init__(self):
        super().__init__(table_name=TRACKING_PLANS_TABLE, primary_key='PlanId')
    def put(self, data: dict):
        key = generate_key()
        display_name = data['display_name']
        if 'events' in data.get('rules', {}):
            events = [event['name'] for event in data['rules']['events']]
        else:
            events = []
        return self.table.put_item(
            Item={
                'PlanId': key,
                'display_name': display_name,
                'events': events
            },
            ReturnValues='NONE'
        )

class EventsTable(DynamoDBTable):
    def __init__(self):
        super().__init__(table_name=EVENTS_TABLE, primary_key='name')
    def put(self, data: dict):
        return self.table.put_item(
            Item={
                'name': data['name'],
                'description': data.get('description', None),
                'rules': data['rules']
            },
            ReturnValues='NONE'
        )

# def get_tracking_plan(plan_id: Optional[str] = None):
#     if plan_id:
#         return TrackingPlansRes.get_item(
#             Key={
#                 'PlanId': plan_id
#             }
#         )
#     else:
#         return TrackingPlansRes.scan()

# def get_events(event_name: Optional[str] = None):
#     if event_name:
#         return EventsRes.get_item(
#             Key={
#                 'name': event_name
#             }
#         )
#     else:
#         return EventsRes.scan()