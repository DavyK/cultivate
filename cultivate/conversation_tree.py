import pygame

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

DEFAULT_CONVERSATION = [
    {
        'text': "Isn't it wonderful here! So peaceful.",
        'responses': [(1, 'yes')],
    },
    {
        'text': 'Have a blessed day!',
        'responses': [],
    },
]


class ConversationTree:
    def __init__(self, npc_name='Community Member', conversation_data=DEFAULT_CONVERSATION):
        self.data = conversation_data
        self.current = self.data[0]
        self.npc_name = npc_name

    def progress(self, key):
        try:
            key_pressed = NUM_KEYS.index(key)
            response_idx, text = self.current['responses'][key_pressed]
            self.current = self.data[response_idx]
            return True
        except (IndexError, ValueError):
            return False
