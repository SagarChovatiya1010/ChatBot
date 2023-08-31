class BotExecution(object):
    def __init__(self, _id, cid, current_step):
        self.id = _id
        self.cid = cid
        self.current_step = current_step

    def __str__(self):
        return "{0} ,{1}".format(self.cid, self.current_step)
