import json
import asyncio

from asgiref.sync import sync_to_async

from gingko.serializers import SubmissionSerializer
from gingko.tasks import align_sequences



async def create_submission(send, data):
    serializer = SubmissionSerializer(data=data)
    if serializer.is_valid():
        obj = await sync_to_async(serializer.save)()
        align_sequences.delay(send, obj.id)
        print(serializer.data)
        send(json.dumps({ "type": "websocket.send", "action": "submission", **{"text": serializer.data} }))
    else:
        print(serializer.errors)

# class SubmissionConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#     async def disconnect(self, close_code):
#         pass
#     async def submission(self, event):
#         await self.send(text_data=json.dumps(event))
#     async def receive(self, text_data):
#         json_dict = json.loads(text_data)
#         action = json_dict.get("action")
#         if action == "create_submission":
#             # await create_submission(self.send, json_dict["payload"])
#             serializer = SubmissionSerializer(data=json_dict["payload"])
#             if serializer.is_valid():
#                 obj = await sync_to_async(serializer.save)()
#                 await self.send(text_data=json.dumps({ "type": "websocket.send", "action": "submission", **{"text": serializer.data} }))
#                 result = await align_sequences.delay(self.send, obj.id)
#                 await self.send(text_data=json.dumps({"type": "websocket.send", "action": "result", **result}))
#             else:
#                 print(serializer.errors)

async def websocket_application(scope, receive, send):
    while True:
        event = await receive()

        if event['type'] == 'websocket.connect':
            await send({
                'type': 'websocket.accept'
            })

        if event['type'] == 'websocket.disconnect':
            break

        if event['type'] == 'websocket.receive':
            json_dict = json.loads(event['text'])
            action = json_dict.get("action")
            if action == "create_submission":
                # await create_submission(self.send, json_dict["payload"])
                serializer = SubmissionSerializer(data=json_dict["payload"])
                if serializer.is_valid():
                    obj = await sync_to_async(serializer.save)()
                    await send(
                        {
                            "type": "websocket.send", 
                            "text": json.dumps({"action": "submission", "payload": {"text": serializer.data}})
                        }
                    )
                    result = align_sequences.delay(obj.id)
                    while not result.ready():
                        await asyncio.sleep(1)

                    await send({"type": "websocket.send", "text": json.dumps({"action": "result", "payload": result})})
