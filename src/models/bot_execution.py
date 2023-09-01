class BotExecution(object):
    def __init__(self, _id, cid, bot_id, current_step):
        self._id = _id
        self.cid = cid
        self.bot_id = bot_id
        self.current_step = current_step

    def __str__(self):
        return "{0} ,{1}".format(self.cid, self.current_step)
