from collections import OrderedDict

NO_QUESTIONS = 'The dedication ceremony is sacred, like everything we do here, and asking for explanations only profanes our experience of such things.'

BYE = 'K, thanks. Byeeeeeeeee!'

task_conversations = OrderedDict({
    'welcome the newcomers': [{
        'text': 'A very special group have just arrived in our community. They will be part of the dedication ceremony in a 6 days. Please, welcome them and show them around.',
        'responses': [(1, 'Sure, no problem')]
    },{
        'text': 'Thanks, I can always count on you',
        'responses': []
    }],

    'dig some holes': [{
        'text': 'Hi. I have a very important task for you. The dedication ceremony of our new members is in 5 days. I need you to dig 6 holes, 6ft deep.',
        'responses': [(1, 'Sure, no problem'), (2, 'ehhhhh... why?'), (3, 'ehhhhh, ok, how?')],
    },{
        'text': 'I can always count on you!',
        'responses': [(4, 'Thanks')]
    },{
        'text': NO_QUESTIONS,
        'responses': [(4, 'oh, ok then')],
    },{
        'text': "You'll find a shovel in the toolshed. Dig the holes in the dirt patch in the east side of the river.",
        'responses': [(1, 'Sure, no problem'), (2, 'ehhhhh... why?')],
    },{
        'text': BYE,
        'responses': []
    }],

    'make lemonade': [{
        'text': 'Hello. Can you do me a favour. I need you to make some lemonade for the dedication ceremony. You can leave it in the kitchen when you are done.',
        'responses': [(1, 'Sure, no problem'), (2, 'ehhhhh... why?'), (3, 'ehhhhh, ok, how?')],
    },{
        'text': 'I can always count on you!',
        'responses': [(4, 'Thanks')]
    },{
        'text': NO_QUESTIONS,
        'responses': [(4, 'oh, ok then')],
    },{
        'text': "Get some lemons, and sugar. Add them to water and heat, BOOM! Lemonade.",
        'responses': [(1, 'Sure, no problem'), (2, 'ehhhhh... why?')],
    },{
        'text': BYE,
        'responses': []
    }],

    'wash the robes': [{
        'text': 'You, I have another task. Wash the dirty robes in the laundry room. They need to be sparkling white for the dedication ceremony.',
        'responses': [(1, 'Sure, no problem'), (2, 'ehhhhh... why?'), (3, 'ehhhhh, ok, how?')],
    },{
        'text': 'I can always count on you!',
        'responses': [(4, 'Thanks')]
    },{
        'text': NO_QUESTIONS,
        'responses': [(4, 'oh, ok then')],
    },{
        'text': "Get some water, add soap, but the robes in and scrub. Don't mix the colors though!",
        'responses': [(1, 'Sure, no problem'), (2, 'ehhhhh... why?')],
    },{
        'text': BYE,
        'responses': []
    }],

    'make candles': [{
        'text': 'The dedication ceremony needs some black candles. Will you to make some',
        'responses': [(1, 'Sure, no problem'), (2, 'ehhhhh... why?'), (3, 'ehhhhh, ok, how?')],
    },{
        'text': 'I can always count on you!',
        'responses': [(4, 'Thanks')]
    },{
        'text': NO_QUESTIONS,
        'responses': [(4, 'oh, ok then')],
    },{
        'text': "You'll need to get some wax from the beehives, melt it and combine it with black dye.",
        'responses': [(1, 'Sure, no problem'), (2, 'ehhhhh... why?')],
    },{
        'text': BYE,
        'responses': []
    }],

    'edit & copy the prayer sheets': [{
        'text': 'Here is a very important book. Plesae make 6 copies of the marked pages for the newcomers to read from.',
        'responses': [(1, 'Sure, no problem'), (2, 'ehhhhh... why?'), (3, 'ehhhhh, ok, how?')],
    },{
        'text': 'I can always count on you!',
        'responses': [(4, 'Thanks')]
    },{
        'text': NO_QUESTIONS,
        'responses': [(4, 'oh, ok then')],
    },{
        'text': "Go to the library, you will be able to get the paper and ink there.",
        'responses': [(1, 'Sure, no problem'), (3, 'ehhhhh... why?')],
    },{
        'text': BYE,
        'responses': []
    }]
})
