
class CustomException(Exception):
    def __init__(self, message: str, args: list):
        self.message = message
        self.args = args

    def __str__(self):
        return self.message + ' : ' + str(self.args)
