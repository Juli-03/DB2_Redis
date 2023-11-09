import base64

class User:

    # HIER AUCH USER BILD EINFÜGEN
    # users have a name, email, userId and an avatar
    def __init__(self, name, email, userId, avatar):
        self.name = name
        self.email = email
        self.userId = userId
        # avatar image is saved in binary format
        # -> needs to be converted to base64 to give it to the html
        self.avatar = self.convert_avatar_to_base64(avatar[0])

    
    def to_json(self):
        # Convert the room object to a JSON-serializable dictionary
        return {
            'name' : self.name,
            'email' : self.email,
            'userId': self.userId,
            'avatar': self.avatar
        }
    
    # convert avatar image to base64
    def convert_avatar_to_base64(self, avatar):
        avatar_b64 = base64.b64encode(avatar).decode('utf-8')
        return avatar_b64