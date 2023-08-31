class AddData(object):
    def __init__(self, bot_id, bot_name, bot_steps):
        self.bot_id = bot_id
        self.bot_name = bot_name
        self.bot_steps = bot_steps

    def __str__(self):
        return "{0} ,{1}".format(self.bot_id, self.bot_name)