import json


class Message:
    # messages have an Id which identifies the person who sent the message in the db, the message itself, a timestamp and an room id to specify
    # in which room the message was sent
    def __init__(self, sentById, message, timestamp, roomId, sentByUser):
        self.sentById = sentById
        self.message = message
        self.timestamp = timestamp
        self.roomId = roomId
        self.sentByUser = sentByUser

class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            # Define how to serialize the Message object to a dictionary
            return {
                'user_id': obj.sentById,
                'message': obj.message,
                'timestamp': obj.timestamp,
                'room_id': obj.roomId,
                'sent_by_User': obj.sentByUser.to_json()
            }
        return super(MessageEncoder, self).default(obj)
