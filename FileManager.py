import os


class CommandException(Exception):
    def __init__(self, message):
        self.message = message


class CommandFormatException(CommandException):
    pass


class CommandExecutionException(CommandException):
    pass


class FileUtils:
    @staticmethod
    def copy(args):
        source = os.path.join(os.getcwd(), args[0])
        destination = os.path.join(os.getcwd(), args[1])

        if not os.path.exists(source):
            raise CommandExecutionException("Source doesn't exist")
        if not os.path.exists(destination) and os.path.isdir(destination):
            raise CommandExecutionException("Destination doesn't exist")

        if os.path.isfile(source):
            if os.path.isdir(destination):
                FileUtils.__copy_file_to_folder(source, destination)
            else:
                FileUtils.__copy_file_to_file(source, destination)
        else:
            if os.path.isfile(destination):
                raise CommandExecutionException("Source is a folder, but destination is a file")
            else:
                FileUtils.__copy_folder_to_folder(source, destination)
                os.removedirs(source)

    @staticmethod
    def print_working_directory(args):
        print(os.getcwd())

    @staticmethod
    def change_directory(args):
        try:
            os.chdir(args[0])
        except Exception as e:
            raise CommandExecutionException(str(e))

    @staticmethod
    def make_directory(args):
        path = os.path.join(os.getcwd(), args[0])
        if os.path.exists(path):
            raise CommandExecutionException("Path already exists")
        os.mkdir(os.path.join(os.getcwd(), args[0]))

    @staticmethod
    def list_files(args):
        print(os.listdir(os.getcwd()))

    @staticmethod
    def remove(args):
        path = os.path.join(os.getcwd(), args[0])
        if not os.path.exists(path):
            raise CommandExecutionException("Path doesn't exist")
        if os.path.isfile(path):
            os.remove(path)
        else:
            os.removedirs(path)

    @staticmethod
    def move(args):
        source = os.path.join(os.getcwd(), args[0])
        destination = os.path.join(os.getcwd(), args[1])

        if not os.path.exists(source):
            raise CommandExecutionException("Source doesn't exist")
        if not os.path.exists(destination):
            raise CommandExecutionException("Destination doesn't exist")

        if os.path.isfile(source):
            if os.path.isdir(destination):
                FileUtils.__copy_file_to_folder(source, destination)
                FileUtils.remove([source])
            else:
                if os.path.dirname(source) == os.path.dirname(destination):
                    os.rename(source, destination)
                else:
                    FileUtils.__copy_file_to_file(source, destination)
                    FileUtils.remove([source])
        else:
            if os.path.isfile(destination):
                raise CommandExecutionException("Source is a folder, but destination is a file")
            else:
                FileUtils.__copy_folder_to_folder(source, destination)
                os.removedirs(source)

    @staticmethod
    def __copy_file_to_folder(source, destination):
        try:
            new_file = os.path.join(destination, os.path.basename(source))
            FileUtils.__copy_file_to_file(source, new_file)
        except Exception as e:
            raise CommandExecutionException(str(e))

    @staticmethod
    def __copy_file_to_file(source, destination):
        try:
            with open(destination, 'w') as nf:
                with open(source, 'r') as src:
                    nf.write(src.read())
        except Exception as e:
            raise CommandExecutionException(str(e))

    @staticmethod
    def __copy_folder_to_folder(source, destination):
        try:
            new_folder = os.path.join(destination, os.path.basename(source))
            os.mkdir(new_folder)
            for file in os.listdir(source):
                if os.path.isfile(file):
                    FileUtils.__copy_file_to_folder(file, destination)
                else:
                    FileUtils.__copy_folder_to_folder(file, new_folder)
        except Exception as e:
            raise CommandExecutionException(str(e))


class Shell:
    def __init__(self):
        self.current_directory = os.getcwd()
        self.commands = {'cp': (FileUtils.copy, 2), 'exit': (self._exit, 0), 'pwd': (FileUtils.print_working_directory, 0),
                         'cd': (FileUtils.change_directory, 1), 'mkdir': (FileUtils.make_directory, 1),
                         'ls': (FileUtils.list_files, 0), 'rm': (FileUtils.remove, 1), 'mv': (FileUtils.move, 2)}
        self.exit_flag = False

    def _exit(self, args):
        self.exit_flag = True


shell = Shell()
while not shell.exit_flag:
    try:
        commandLine = input().split(' ')
        if len(commandLine) == 0:
            continue

        command = commandLine[0]
        if command in shell.commands.keys():
            if len(commandLine) != 1 + shell.commands[command][1]:
                raise CommandFormatException('Invalid number of arguments')

            args = commandLine[1:] if len(commandLine) > 1 else 0
            shell.commands[command][0](args)
        else:
            raise CommandFormatException('Invalid command')
    except CommandException as e:
        print(e.message)