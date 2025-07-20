import random
words = ['белокочанная', 'капуста', 'сладкий', 'болгарский', 'перец',
             'ягодки', 'граната', 'авокадо', 'консервированный', 'нут']
while words:
    random.shuffle(words)
    word = words.pop()
    print (word)