class BotSteps(object):
    def __init__(self, _id, bot_step_id, bot_next_steps):
        self.id = _id
        self.bot_step_id = bot_step_id
        self.bot_next_steps = bot_next_steps

    def __str__(self):
        return "{0} ,{1}".format(self.bot_step_id, self.bot_next_steps)
