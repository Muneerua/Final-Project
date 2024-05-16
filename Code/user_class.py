class Users:
    def __init__(self, data, username):
        self.data = data
        self.username = username

    def find_user_role(self):

        role = self.data[self.username]['role']
        return role