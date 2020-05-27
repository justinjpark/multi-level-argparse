#!/usr/bin/env python


import argparse
import sys
import subprocess


class MultiLevelArgparse:

    def __init__(self):
        parser = argparse.ArgumentParser(
            usage='''multi-level-argparse <command> [<args>]

Multi-level argparse in Python

The most commonly used multi-level-argparse commands are:
  foo         Example command with optional arguments (flags)
  bar         Example command with positional/required arguments and flags
  baz         Example command with another layer of subcommands
  brewups     Runs brew update, brew upgrade, and brew cask upgrade
''',
            # description='Multi-level argparse in Python',
            epilog='Based on Chase Seibert Blog post, https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html'
        )
        parser.add_argument('command', help='Command to run')

        # if there is no command specified, print the parser's help message
        if len(sys.argv) == 1:
            parser.print_help()
            exit(1)

        # parse_args defaults to [1:] for args (from sys.argv), but we only need the second argument to create the next parser
        # for now we will also exclude the rest of the args, otherwise the validation will fail
        args = parser.parse_args(sys.argv[1:2])

        # LBYL (Look Before You Leap)
        # validate command using dispatch list, print error message if the command is unrecognized
        dispatch = ['foo', 'bar', 'baz', 'brewups']
        if args.command not in dispatch: # if not hasattr(self, args.command):
            print(f"multi-level-argparse: '{args.command}' is not a multi-level-argparse command. See 'multi-level-argparse --help'")
            exit(1)

        # getattr(self, 'x') is equivalent to self.x
        # use dispatch pattern to invoke method with same name of the command
        getattr(self, args.command)()

    # example command with optional arguments (flags)
    def foo(self):
        parser = argparse.ArgumentParser(
            description='Example command with optional arguments (flags)'
        )
        # add additional required and/or optional arguments here
        # prefixing the argument with '--' means it is optional
        # NOT prefixing the argument with '--' means it is not optional and required (positional)
        parser.add_argument('-b', '--blue', action='store_true', help='<insert description for blue here>')
        parser.add_argument('-g', '--green', action='store_true', help='<insert description for green here>')

        # now that we are inside a command, ignore the first argv and get the rest of the arguments
        args = parser.parse_args(sys.argv[2:])

        # --> command behavior goes here
        print(f'Running multi-level-argparse foo, blue={args.blue}, green={args.green}')


    # example command with positional/required arguments and flags
    def bar(self):
        parser = argparse.ArgumentParser(
            description='Example command positional/required arguments and flags'
        )
        parser.add_argument('input', help='User input to read in')
        parser.add_argument('-b', '--blue', action='store_true', help='<insert description for blue here>')
        parser.add_argument('-g', '--green', action='store_true', help='<insert description for green here>')

        args = parser.parse_args(sys.argv[2:])

        print(f'Running multi-level-argparse bar, input={args.input}, blue={args.blue}, green={args.green}')


    # using an inner/nested class to encapsulate baz methods
    # why? in addition to encapsulation, to logically group baz methods and increase code readability
    class Baz:

        def __init__(self):
            parser = argparse.ArgumentParser(
                usage='''multi-level-argparse baz <command> [<args>]

Example command with another layer of subcommands

The most commonly used baz commands are:
  one         <insert description here>
  two         <insert description here>
'''
            )
            parser.add_argument('command', help='Command to run')

            if len(sys.argv) == 2:
                parser.print_help()
                exit(1)
            
            # in this case, we only need the third argument to create the next parser
            args = parser.parse_args(sys.argv[2:3])

            # validate command using dispatch list, print error message if the command is unrecognized
            dispatch = ['one', 'two']
            if args.command not in dispatch:
                print(f"multi-level-argparse: '{args.command}' is not a multi-level-argparse baz command. See 'multi-level-argparse baz --help'")
                exit(1)
            getattr(self, args.command)()


        def one(self):
            # parser = argparse.ArgumentParser()
            # parser.add_argument()
            # args = parser.parse_args(sys.argv[3:])

            print(f'Running multi-level-argparse baz one')


        def two(self):
            # parser = argparse.ArgumentParser()
            # parser.add_argument()
            # args = parser.parse_args(sys.argv[3:])

            print(f'Running multi-level-argparse baz two')


    # example command with another layer of subcommands
    def baz(self):
        self.Baz()


    # example command that uses subprocess.run() to execute shell/terminal commands
    # runs brew update, brew upgrade, and brew cask upgrade
    def brewups(self):
        parser = argparse.ArgumentParser(
            description='Runs brew update, brew upgrade, and brew cask upgrade'
        )
        parser.add_argument('-n', '--dry-run', action='store_true', help='Show what would be upgraded, but do not actually upgrade anything')

        args = parser.parse_args(sys.argv[2:])

        # EAFP (Easier to Ask for Forgiveness than Permission)
        # try:
        #     completed_process = subprocess.call([], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # except OSError:
        #     pass
        try:
            if True: # if args.dry-run
                subprocess.run(['brew', 'update']) 
                subprocess.run(['brew', 'upgrade', '--dry-run'])
                subprocess.run(['brew', 'cask', 'upgrade', '--dry-run'])
            else:
                subprocess.run(['brew', 'update'])
                subprocess.run(['brew', 'upgrade'])
                subprocess.run(['brew', 'cask', 'upgrade'])
        except OSError:
            print('multi-level-argparse: Error when trying to use Homebrew (brew). Check if Homebrew is installed.')


def main():
    MultiLevelArgparse()


if __name__ == '__main__':
    main()
