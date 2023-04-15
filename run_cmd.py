import struct, fcntl, termios, signal, sys
import shutil
import subprocess
import shlex
from functools import partial
import pexpect


def run_cmd(cmd):
    cmd = shlex.split(cmd)
    output = subprocess.check_output(cmd, timeout=120)
    output = output.decode().strip()
    return output


def run_cmd_popen(cmd):
    print(cmd)
    cmd = shlex.split(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = p.stdout.readline()
        if p.poll() is not None:
            break
        if output:
            print(output.decode().strip())
    rc = p.poll()
    if rc != 0:
        raise subprocess.CalledProcessError


def get_terminal_size():
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack("hhhh", fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s))
    return a[0], a[1]


def sigwinch_passthrough(p, sig, data):
    if not p.closed:
        p.setwinsize(*get_terminal_size())


def pexpect_spawn(cmd):
    p = pexpect.spawnu(cmd, timeout=None, logfile=sys.stdout)
    # p.setwinsize(*get_terminal_size())
    # signal.signal(signal.SIGWINCH, partial(sigwinch_passthrough, p))
    output = ""
    while True:
        line = p.readline()
        if not line:
            p.close()
            return p.exitstatus, output
        output += line


def run_cmd_pexpect(cmd):
    exit_code, output = pexpect_spawn(cmd)
    if exit_code != 0:
        error = "'%s' - command returned non-zero exit code" % cmd
        raise Exception(error)
    return output
