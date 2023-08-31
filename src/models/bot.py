class Bot(object):
    def __init__(self, _id, bot_id):
        self.id = _id
        self.bot_id = bot_id

    def __str__(self):
        return "{0} ,{1}".format(self.bot_id, self.bot_id)
