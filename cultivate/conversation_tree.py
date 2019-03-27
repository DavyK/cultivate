import pygame

DATA = [
    {
        'text': 'Did you get the lemon yet?',
        'responses': [(1, 'yes'), (2, 'no'), (3, "I don't know where it is")],
    },
    {
        'text': 'Great! now make some lemonade!',
        'responses': [(4, 'ok')],
    },
    {
        'text': "Then go get it! It's in the building" ,
        'responses': [(4, 'Thanks!')],
    },
    {
        'text': "It's in the building!",
        'responses': [(4, 'Thanks!')],
    },
    {
        'text': 'Byeeeeeee!',
        'responses': [],
    },
]

NUM_KEYS = [
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4,
    pygame.K_5,
    pygame.K_6,
    pygame.K_7,
    pygame.K_8,
    pygame.K_9,
]


class ConversationTree:
    def __init__(self, npc_name='Community Member'):
        self.data = DATA
        self.current = self.data[0]
        self.npc_name = npc_name

    def progress(self, key):
        try:
            key_pressed = NUM_KEYS.index(key)
            response_idx, text = self.current['responses'][key_pressed]
            self.current = self.data[response_idx]
            print(self.current)
        except (IndexError, ValueError):
            return
        print(self.current)












