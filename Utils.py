import os, os.path
import subprocess
import sys


def is_bundled():
    return getattr(sys, 'frozen', False)

def local_path(path=''):
    if local_path.cached_path is not None:
        return os.path.join(local_path.cached_path, path)

    if is_bundled():
        # we are running in a bundle
        local_path.cached_path = os.path.dirname(os.path.realpath(sys.executable))
    else:
        # we are running in a normal Python environment
        local_path.cached_path = os.path.dirname(os.path.realpath(__file__))

    return os.path.join(local_path.cached_path, path)

local_path.cached_path = None

def default_output_path(path):
    if path == '':
        path = os.path.join('.', 'Output')

    if not os.path.exists(path): 
        os.mkdir(path)
    return path


def open_file(filename):
    if sys.platform == 'win32':
        os.startfile(filename)
    else:
        open_command = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([open_command, filename])

def close_console():
    if sys.platform == 'win32':
        #windows
        import ctypes.wintypes
        try:
            ctypes.windll.kernel32.FreeConsole()
        except Exception:
            pass


def get_version_bytes(a):
    version_bytes = [0x00, 0x00, 0x00]
    if not a:
        return version_bytes;
    sa = a.replace('v', '').replace(' ', '.').split('.')

    for i in range(0,3):
        try:
            version_byte = int(sa[i])
        except ValueError:
            break
        version_bytes[i] = version_byte

    return version_bytes


# From the pyinstaller Wiki: https://github.com/pyinstaller/pyinstaller/wiki/Recipe-subprocess
# Create a set of arguments which make a ``subprocess.Popen`` (and
# variants) call work with or without Pyinstaller, ``--noconsole`` or
# not, on Windows and Linux. Typical use::
#   subprocess.call(['program_to_run', 'arg_1'], **subprocess_args())
def subprocess_args(include_stdout=True):
    # The following is true only on Windows.
    if hasattr(subprocess, 'STARTUPINFO'):
        # On Windows, subprocess calls will pop up a command window by default
        # when run from Pyinstaller with the ``--noconsole`` option. Avoid this
        # distraction.
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # Windows doesn't search the path by default. Pass it an environment so
        # it will.
        env = os.environ
    else:
        si = None
        env = None

    # ``subprocess.check_output`` doesn't allow specifying ``stdout``::
    # So, add it only if it's needed.
    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}

    # On Windows, running this from the binary produced by Pyinstaller
    # with the ``--noconsole`` option requires redirecting everything
    # (stdin, stdout, stderr) to avoid an OSError exception
    # "[Error 6] the handle is invalid."
    ret.update({'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env })
    return ret
