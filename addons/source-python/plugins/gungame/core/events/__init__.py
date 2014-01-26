for event_file in Path(__file__).parent.joinpath('included').files():
    __import__('gungame.core.events.' + event_file.namebase, fromlist=[''])
