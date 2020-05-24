# multi-level-argparse
Multi-level argparse in Python

Based on Chase Seibert Blog [post](https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html)

It’s a common pattern for command line tools to have multiple subcommands that run off of a single executable,
where each subcommand has its own set of required and optional parameters.
This pattern is fairly easy to implement in your own Python command-line utilities using argparse.
