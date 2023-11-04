class Room:

    # rooms have two partners a and b, a roomID and messages with timestamps
    def __init__(self, partnerA, partnerB, roomId):
        self.partnerA = partnerA
        self.partnerB = partnerB
        self.roomId = roomId
        #self.messages = messages
        #self.timestamps = timestamps