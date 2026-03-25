import glob
import os

files = glob.glob('*.html')
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if '<a href="chat.html">PawPal Chat</a>' not in content:
        # Avoid replacing inside chat.html itself if it doesn't have the standard nav
        # But chat.html does not have standard nav, it has a back button.
        if f != 'chat.html':
            content = content.replace('<a href="pets.html">Pets</a>', '<a href="pets.html">Pets</a>\n        <a href="chat.html">PawPal Chat</a>')
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f'Updated {f}')
