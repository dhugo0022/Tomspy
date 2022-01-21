from prompt_toolkit.shortcuts import button_dialog

result = button_dialog(
    title='Button dialog example',
    text='Do you want to confirm?',
    buttons=[
        ('1337x', '1337x'),
        ('Torrent', "Torrent"),
        ('Maybe...', None)
    ],
).run()

print(result)