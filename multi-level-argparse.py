#!/usr/bin/env python


#
# Based on Chase Seibert Blog post,
# https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
#
# Multi-level argparse
#
# It’s a common pattern for command line tools to have multiple subcommands that run off of a single executable,
# where each subcommand has its own set of required and optional parameters.
# This pattern is fairly easy to implement in your own Python command-line utilities using argparse.
#
# Testing your command line tool?
# Make sure your Python script is executeable by using the command `chmod +x myscript.py`.
# You can also drop the .py extension now, to do this use the command `mv myscript.py myscript`.
# Now that your Python script is executeable, run it using the command `./myscript`.
#
# Finally (optional)
# If you want your command line tool to behave like an actual shell command or system tool, you need to add it to your PATH.
# First, create a ~/bin directory in your user's home directory.
# Next, copy your Python script to ~/bin, to do this use the command `cp myscript ~/bin`
# Lasty, add the ~/bin directory to your PATH using the command `export PATH=~/bin:$PATH` (only temporary). 
# If you want your command line tool permanently available on your system, add the export command to your .zshrc or .bash_profile
#


import argparse
import sys
import subprocess


class MultiLevelArgparse:


    def __init__(self):
        parser = argparse.ArgumentParser(
            usage='''multi-level-argparse <command> [<args>]

The most commonly used multi-level-argparse commands are:
  command_a   Example command with optional arguments (flags)
  command_b   Example command positional/required arguments and flags
  command_c   Example command with another layer of subcommands
  brewups     Runs brew update, brew upgrade, and brew cask upgrade
''',
            description='Multi-level argparse in Python',
            epilog='Based on Chase Seibert Blog post, https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html')
        parser.add_argument('command', help='Command to run')

        # parse_args defaults to [1:] for args (from sys.argv), but we only need the second args to create the next parser
        # for now we will also exclude the rest of the args, otherwise the validation will fail
        args = parser.parse_args(sys.argv[1:2])
        
        # validate command, print error message if the command is unrecognized
        if not hasattr(self, args.command):
            print(f"multi-level-argparse: '{args.command}' is not a multi-level-argparse command. See 'multi-level-argparse --help'")
            exit(1)

        # getattr(self, 'x') is equivalent to self.x
        # use dispatch pattern to invoke method with same name of the command
        getattr(self, args.command)()

        # if there is no command specified, print the parser's help message
        if len(sys.argv) == 1:
            parser.print_help()
            exit(1)


    # example command with optional arguments (flags)
    def command_a(self):
        parser = argparse.ArgumentParser(
            description = '<insert description for command_a here>'
        )

        # add additional required and/or optional arguments here
        # prefixing the argument with '--' means it is optional
        # NOT prefixing the argument with '--' means it is not optional and required (positional)
        parser.add_argument('-f', '--foo', action='store_true', help='<insert description for foo here>')
        parser.add_argument('-b', '--bar', action='store_true', help='<insert description for bar here>')

        # now that we are inside a command, ignore the first argv and get the rest of the arguments
        args = parser.parse_args(sys.argv[2:])
        print(f'Running multi-level-argparse command_a, foo={args.foo}, bar={args.bar}')


    # example command with positional/required arguments and flags
    def command_b(self):
        parser = argparse.ArgumentParser(
            description = '<insert description for command_b here>'
        )
        parser.add_argument('subcommand', help='Subcommand to run')


    # TODO: 
    # example command with another layer of subcommands
    # def command_c(self):


    def brewups(self):
        parser = argparse.ArgumentParser(
            description='Runs brew update, brew upgrade, and brew cask upgrade'
            )
        parser.add_argument('-n', '--dry-run', action='store_true', help='Show what would be upgraded, but do not actually upgrade anything')

        args = parser.parse_args(sys.argv[2:])


        # EAFP (Easier to Ask for Forgiveness than Permission)
        # try:
        #     subprocess.call([], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # except OSError:
        #     pass
        try:
            if True: # if args.dry-run
                subprocess.call(['brew', 'update'], stderr=subprocess.DEVNULL)
                subprocess.call(['brew', 'upgrade', '--dry-run'], stderr=subprocess.DEVNULL)
                subprocess.call(['brew', 'cask', 'upgrade', '--dry-run'], stderr=subprocess.DEVNULL)
            else:
                subprocess.call(['brew', 'update'], stderr=subprocess.DEVNULL)
                subprocess.call(['brew', 'upgrade'], stderr=subprocess.DEVNULL)
                subprocess.call(['brew', 'cask', 'upgrade'], stderr=subprocess.DEVNULL)
        except OSError:
            print('multi-level-argparse: Error when trying to use homebrew-Cask (brew). Check if homebrew is installed and working correctly.')


def main():
    MultiLevelArgparse()


if __name__ == '__main__':
    main()
