
import os, sys

os.environ["PyPI_REQUIREMENTS_OUTPUT"] = "ON"

os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))


try:
    import winput
    import PIL
    
    assert hasattr(winput, "set_DPI_aware")
        
except:
    sys.exit(-1)


argv_short_to_long_dict = { "h" : "help", "?" : "help" }

kwargs_with_argments = ()

HELP_STRING = """Input Recorder.
Records and plays back macros.

Currently only supports GUI mode.

Usage: irec
"""

def start_command_line_mode(*args, **kwargs):
    pass

def start_windowed_mode():
    import irec_module.window
    

def main(*args, **kwargs):
    if kwargs.get("help", False):
        print(HELP_STRING)
        return

    if kwargs or args:
        start_command_line_mode(*args, **kwargs)

    start_windowed_mode()

def process_argv():
    argv = sys.argv

    kwargs = {}
    args = []

    if len(argv) > 1:
        last_command = None
        
        for arg in argv[1:]:
            if len(arg) == 2 and (arg[0] == "-" or arg[0] == "/"):
                command_alias = arg[1]
                
                if not command_alias in argv_short_to_long_dict:
                    raise KeyError("Unknown command line argument {}. Try -h for a list of commands.".format(arg))

                if last_command:
                    raise ValueError("Argument '{}' has no value.".format(last_command))

                command = argv_short_to_long_dict[command_alias]

                if command in kwargs_with_argments:
                    last_command = command

                else:
                    kwargs[command] = True

            elif len(arg) > 2 and arg.startswith("--"):
                command = arg[2:]
                
                if not command in argv_short_to_long_dict.values():
                    raise KeyError("Unknown command line argument {}. Try -h for a list of commands.".format(arg))

                if last_command:
                    raise ValueError("Argument '{}' has no value.".format(last_command))

                if command in kwargs_with_argments:
                    last_command = command

                else:
                    kwargs[command] = True

            else:
                if last_command:
                    kwargs[last_command] = arg
                    last_command = None

                else:
                    args.append(arg)

        if last_command:
            raise ValueError("Argument '{}' has no value.".format(last_command))

    return (args, kwargs)
                

if __name__ == "__main__":
    args, kwargs = process_argv()
    main(*args, **kwargs)

