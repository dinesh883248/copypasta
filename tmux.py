import shutil
import time
import uuid
import subprocess
from pathlib import Path


def run_cmd(cmd, attach=True):
    # create session
    session = uuid.uuid4().hex
    subprocess.run(["tmux", "new-session", "-d", "-s", session])

    # init files
    cwd = Path().resolve()
    work_dir = f"{cwd}/.pysh/{uuid.uuid4().hex}"
    Path(work_dir).mkdir(parents=True, exist_ok=True)
    output_file = f"{work_dir}/output"
    exit_code = f"{work_dir}/exit_code"

    # setup logging and execute cmd
    cmd = f"{cmd}; echo $? > {exit_code}; exit"
    subprocess.run(["tmux", "pipe-pane", "-t", session, f"cat > {output_file}"])
    subprocess.run(["tmux", "send-keys", "-t", session, cmd, "C-m"])

    if attach:
        subprocess.run(["tmux", "attach", "-t", session])
    else:
        # wait for cmd to complete
        while True:
            if Path(exit_code).is_file():
                break
            time.sleep(0.5)

    # remove session
    subprocess.run(["tmux", "pipe-pane", "-t", session])
    subprocess.run(["tmux", "kill-session", "-t", session])

    # extract results
    with open(exit_code, "r") as f:
        exit_code = f.read()
    with open(output_file, "r") as f:
        output = f.readlines()
    output = "".join(output[2:-1])

    # cleanup files
    shutil.rmtree(work_dir)

    return exit_code.strip(), output.rstrip()
