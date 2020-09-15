class Menu:

    """ Represents a set of menu options. Each option has a key or string the user
    should press to select it, a text description, and the function to be invoked for that choice.
    The keys the user presses are unique within a menu. """

    def __init__(self):
        self.text_descriptions = {}
        self.functions = {}
        self.original_keys = {}


    def add_option(self, key, description, func):
        """ Add or replaces an option to this menu.
        If another option with the same key is already present, it will be overwritten.
        :param key: the key the user should press to select this option. Can be a single character or a string
        :param description: a text description of the menu option
        :param func: the function that should be invoked when the user selects this option """
        original_key = key
        key = key.lower()
        self.text_descriptions[key] = description
        self.functions[key] = func
        self.original_keys[key] = original_key



    def is_valid(self, choice):
        """ Verifies if a choice is one of the menu options
        :param choice: the choice to check
        :returns: True if the choice is a key in the menu options, False otherwise  """
        return choice.lower() in self.text_descriptions


    def get_action(self, choice):
        """ :returns: the function to invoke for the menu choice, or None if not found """
        return self.functions.get(choice.lower())


    def __str__(self):
        """ :returns: all the menu options and their descriptions, one per line. """
        texts = [f'{self.original_keys[key]}: {self.text_descriptions[key]}' for key in self.text_descriptions.keys()]
        return '\n'.join(texts)

