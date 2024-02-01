title = 'Python for Beginners'
tokens = title.split(' ')
if 'Chapter 1' not in tokens:
        tokens.append('Chapter 1')
new_title = ' '.join(tokens)