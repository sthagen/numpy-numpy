import os
import sys
import subprocess
from argparse import ArgumentParser
from git import Repo, exc

CWD = os.path.abspath(os.path.dirname(__file__))


class DiffLinter:
    def __init__(self):
        self.repository_root = os.path.realpath(os.path.join(CWD, '..'))

    def run_ruff(self):
        """
            Original Author: Josh Wilson (@person142)
            Source:
              https://github.com/scipy/scipy/blob/main/tools/lint_diff.py
            Unlike pycodestyle, ruff by itself is not capable of limiting
            its output to the given diff.
        """
        res = subprocess.run(
            ['ruff', 'check', '--statistics'],
            stdout=subprocess.PIPE,
            cwd=self.repository_root,
            encoding='utf-8',
        )
        return res.returncode, res.stdout

    def run_lint(self):
        retcode, errors = self.run_ruff()

        errors and print(errors)

        sys.exit(retcode)


if __name__ == '__main__':
    parser = ArgumentParser()
    args = parser.parse_args()

    DiffLinter().run_lint()
