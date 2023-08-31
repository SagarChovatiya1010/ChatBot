class BotExecution(object):
    def __init__(self, _id, customerID, current_step_ID):
        self.id = _id
        self.customerID = customerID
        self.current_step_ID = current_step_ID

    def __str__(self):
        return "{0} ,{1}".format(self.customerID, self.current_step_ID)
