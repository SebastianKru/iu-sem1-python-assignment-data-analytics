class CustomParameterException(Exception): 


    def __init__(self, exc_parameter, exc_message):
        super().__init__(self, exc_parameter, exc_message)


class CustomTextException(Exception):

    def __init__(self, exc_message):
        super().__init__(self, exc_message)