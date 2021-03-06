from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from .capture_subprocess import capture_subprocess
from testing import coverage_warnings_regex


def make_outputter():
    """Create the the outputter.py script, for the demonstration."""
    with open('outputter.py', 'w') as outputter:
        outputter.write('''\
from __future__ import print_function
from __future__ import division
from sys import stdout, stderr
from time import sleep
from random import random, seed
seed(0)  # unpredictable, but repeatable

# system should not deadlock for any given value of these parameters.
LINES = 4000
TIME = 0
WIDTH = 179
ERROR_RATIO = .20

for i in range(LINES):
    if random() > ERROR_RATIO:
        char = '.'
        file = stdout
    else:
        char = '%'
        file = stderr

    for j in range(WIDTH):
        print(char, file=file, end='')
        file.flush()
        sleep(TIME / LINES / WIDTH)
    print(file=file)
    file.flush()
''')


def test_capture_subprocess(tmpdir):
    tmpdir.chdir()
    make_outputter()

    cmd = ('python', 'outputter.py')
    stdout, stderr = capture_subprocess(cmd)

    stderr = coverage_warnings_regex.sub('', stderr)

    assert stdout.count('\n') == 3207
    assert stderr.count('\n') == 793

    assert stdout.strip('.\n') == ''
    assert stderr.strip('%\n') == ''


def test_cli():
    from venv_update import check_output
    from sys import executable
    from testing.capture_subprocess import __file__ as script
    output = check_output((executable, script, 'echo', 'ok'))
    assert output == 'ok\n'
