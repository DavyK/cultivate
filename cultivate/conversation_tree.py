
class ConversationTree:
    def __init__(self, data):
        self.data = data
        self._progress = []

    def progress(self):
        if self._progress == None:



data = [
    'root': {
        'text': 'this is a test',
        'responses': ['r1', 'r2',],
    },
    'r1': {
        'text': 'this is a response',
        'responses': ['r3', 'r4', 'r5'],
    },
    'r2': {
        'text': 'this is a response',
        'responses': ['r6'],
    },
    'r3': {
        'text': 'this is a response',
        'responses': [],
    },
    'r4': {
        'text': 'this is a response',
        'responses': [],
    },
    'r5': {
        'text': 'this is a response',
        'responses': [],
    },
    'r6': {
        'text': 'this is a response',
        'responses': [],
    }
]





