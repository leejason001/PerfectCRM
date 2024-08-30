
class BaseKingAdmin(object):
    list_filter = []
    list_display = []
    search_fields = []
    readonly_fields = []
    default_actions = ["delelteSelected"]
    actions = []
    def __init__(self):
        self.actions.extend(self.default_actions)