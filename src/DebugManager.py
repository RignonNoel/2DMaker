class DebugManager(object):

    list_commands = {}

    def __init__(self):
        help_command = "This is the list of supported command for this " \
                       "debug console :\n" \
                       "\n " \
                       "- new_entity -> Create a new entity\n" \
                       "- help -> List all supported command"

        self.list_commands['help'] = help_command

        new_entity = "New entity created with success"
        self.list_commands['new_entity'] = new_entity

    def run(self):
        """thread worker function"""
        running = True
        while running:
            command = str(input("command$ "))

            if command in self.list_commands.keys():
                print(self.list_commands[command])

            else:
                print("Command not found. \n"
                      "Try 'help' command to have a list of command")
