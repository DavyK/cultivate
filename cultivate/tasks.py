from collections import OrderedDict

SURE = "Sure, no problem"
WHY = "Ehhhhh... why?"
HOW = "Ehhhhh, ok, how?"
OK = "Oh, ok then"
NO_QUESTIONS = 'The dedication ceremony is sacred, like everything we do here, and asking for explanations only profanes our experience of such things.'
BYE = 'K, thanks. Byeeeeeeeee!'

task_conversations = OrderedDict({
    # day 0
    "welcome the newcomers": [{}],  # this is implemented in day_0_conversations
    # day 1
    'dig some holes': [{
        'text': 'Hi. I have a very important task for you. The dedication ceremony of our new members is in 5 days. I need you to dig 6 holes, 6ft deep.',
        'responses': [(1, SURE), (2, WHY), (3, HOW)],
    },{
        'text': 'I can always count on you!',
        'responses': [(4, 'Thanks')]
    },{
        'text': NO_QUESTIONS,
        'responses': [(4, OK)],
    },{
        'text': "You'll find a shovel in the toolshed. Dig the holes in the dirt patch in the east side of the river.",
        'responses': [(1, SURE), (2, WHY)],
    },{
        'text': BYE,
        'responses': []
    }],
    # day 2
    'make lemonade': [{
        'text': 'Hello. Can you do me a favour. I need you to make some lemonade for the dedication ceremony. You can leave it in the kitchen when you are done.',
        'responses': [(1, SURE), (2, WHY), (3, HOW)],
    },{
        'text': 'I can always count on you!',
        'responses': [(4, 'Thanks')]
    },{
        'text': NO_QUESTIONS,
        'responses': [(4, OK)],
    },{
        'text': "Get some lemons, and sugar. Add them to water and heat, BOOM! Lemonade.",
        'responses': [(1, SURE), (2, WHY)],
    },{
        'text': BYE,
        'responses': []
    }],
    # day 3
    'wash the robes': [{
        'text': 'You, I have another task. Wash the dirty robes in the laundry room. They need to be sparkling white for the dedication ceremony.',
        'responses': [(1, SURE), (2, WHY), (3, HOW)],
    },{
        'text': 'I can always count on you!',
        'responses': [(4, 'Thanks')]
    },{
        'text': NO_QUESTIONS,
        'responses': [(4, OK)],
    },{
        'text': "Get some water, add soap, put the robes in and scrub, then leave them on the line to dry. Don't mix the colors though!",
        'responses': [(1, SURE), (2, WHY)],
    },{
        'text': BYE,
        'responses': []
    }],
    # day 4
    'make candles': [{
        'text': 'The dedication ceremony needs some black candles. Will you to make some',
        'responses': [(1, SURE), (2, WHY), (3, HOW)],
    },{
        'text': 'I can always count on you!',
        'responses': [(4, 'Thanks')]
    },{
        'text': NO_QUESTIONS,
        'responses': [(4, OK)],
    },{
        'text': "You'll need to get some wax from the beehives, melt it and combine it with black dye. Then use the bucket as a candle mold.",
        'responses': [(1, SURE), (2, WHY), (2, '... use the bucket as a mold?!?!?')],
    },{
        'text': BYE,
        'responses': []
    }],
    # day 5
    'edit the book': [{
        'text': "I've been working on a very important book, but I'm not very good at spelling. Go fix any errors for me.",
        'responses': [(1, SURE), (2, WHY), (3, HOW)],
    },{
        'text': 'I can always count on you!',
        'responses': [(4, 'Thanks')]
    },{
        'text': NO_QUESTIONS,
        'responses': [(4, OK)],
    },{
        'text': "Go to the library, you can find the book there.",
        'responses': [(1, SURE), (3, WHY)],
    },{
        'text': BYE,
        'responses': []
    }],
    # day 6
    'go to the church': [{
        'text': "I think you're needed at the church. The dedication ceremony is upon us",
        "responses": []
    }],
})

day_0_conversations = OrderedDict({
    'welcome the newcomers': [{
        'text': "Hello, newcomers! I've been tasked with showing you around. First I'm going to show you the kitchen. If I can remember where it is...",
        'responses': []
    }],
    'kitchen description': [{
        'text': "Ah, there it is! You can get any food from here. Help yourself! Next on our tour will be the toolshed. I could have sworn it was...",
        'responses': []
    }],
    'toolshed description': [{
        'text': "From here if you need to help me, the Gardener, you can get any tools you need. Next is our library. Knowledge is key to a good life! Hmm. It's around here somewhere...",
        'responses': []
    }],
    'library description': [{
        'text': "Aha! Yes now I remember. So here you can learn the basics of our community. Lastly is our church. Where in God's name is it..",
        'responses': []
    }],
    'church description': [{
        'text': "So we're a religious bunch so you may find yourself here from time to time.",
        'responses': []
    }],
    'end day 0': [{
        'text': "Well that's it for the tour now. This is all I had to do for the day so I'm going to find my bed. It should have been where I left it...",
        'responses': []
    }],
})
