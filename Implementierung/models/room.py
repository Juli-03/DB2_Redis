class Room:

    # rooms have two partners a and b, a roomID and messages with timestamps
    def __init__(self, partnerA, partnerB, roomId, messages=None):
        self.partnerA = partnerA
        self.partnerB = partnerB
        self.roomId = roomId
        self.messages = messages

    def to_json(self):
        # Convert the room object to a JSON-serializable dictionary
        return {
            'partnerA'   : self.partnerA.to_json(),
            'partnerB'   : self.partnerB.to_json(),
            'room_id'    : self.roomId,
            'messages'   : self.messages,
        }