from colorama import Fore, Style, init
from termcolor import colored

init()

def create_banner():
    ascii_art = '''
███╗   ███╗███████╗██╗     ██╗ ██████╗ ██████╗  █████╗ ███████╗
████╗ ████║██╔════╝██║     ██║██╔═████╗██╔══██╗██╔══██╗██╔════╝
██╔████╔██║█████╗  ██║     ██║██║██╔██║██║  ██║███████║███████╗
██║╚██╔╝██║██╔══╝  ██║     ██║████╔╝██║██║  ██║██╔══██║╚════██║
██║ ╚═╝ ██║███████╗███████╗██║╚██████╔╝██████╔╝██║  ██║███████║
╚═╝     ╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
'''
    
    colors = [Fore.RED, Fore.LIGHTRED_EX, Fore.YELLOW, Fore.LIGHTYELLOW_EX]

    lines = ascii_art.splitlines()

    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(color + line + Style.RESET_ALL)

def show():
    create_banner()
    print('')

if __name__ == '__show__':
    show()