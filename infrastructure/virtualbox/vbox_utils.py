import subprocess

VBOX = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

def run_vbox(*args):
    """Execute a VBoxManage command and return its result."""
    result = subprocess.run(
        [VBOX, *map(str, args)],
        capture_output=True,
        text=True,
    )

    if result.stdout:
        print(result.stdout.strip())

    if result.returncode != 0:
        print(f"VBoxManage command failed: {args}")
        if result.stderr:
            print(result.stderr.strip())

        raise subprocess.CalledProcessError(
            result.returncode,
            result.args,
            output=result.stdout,
            stderr=result.stderr,
        )

    return result
