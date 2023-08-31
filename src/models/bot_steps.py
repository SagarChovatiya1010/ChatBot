class BotSteps(object):
    def __init__(self, _id, step_id, next_steps):
        self.id = _id
        self.step_id = step_id
        self.next_steps = next_steps

    def __str__(self):
        return "{0} ,{1}".format(self.step_id, self.next_steps)
