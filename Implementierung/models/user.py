class User:

    # users have a name, email and an userId
    def __init__(self, name, email, userId):
        self.name = name
        self.email = email
        self.userId = userId

    
    def to_json(self):
        # Convert the room object to a JSON-serializable dictionary
        return {
            'name' : self.name,
            'email' : self.email,
            'userId': self.userId
        }