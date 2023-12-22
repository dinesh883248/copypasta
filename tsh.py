import shutil
import os
import time
import uuid
import subprocess
from pathlib import Path
from textwrap import dedent


class TmuxSession:
    def __init__(self):
        self.session_id = self.create_session()
        self.pane_id = f"{self.session_id}:0.0"

    def create_session(self):
        session_id = uuid.uuid4().hex
        subprocess.check_call(["tmux", "new-session", "-d", "-s", session_id])
        return session_id

    def remove(self):
        subprocess.run(["tmux", "kill-session", "-t", self.session_id])

    def start_pipe(self, output_file):
        subprocess.run(
            ["tmux", "pipe-pane", "-t", self.pane_id, f"cat > {output_file}"]
        )

    def stop_pipe(self):
        subprocess.run(["tmux", "pipe-pane", "-t", self.session_id])

    def wait_for_completion(self, exit_code):
        while True:
            if Path(exit_code).is_file():
                return
            time.sleep(0.1)

    def extract_output(self, output, run_id):
        pivots = []
        for i, l in enumerate(output):
            if l.strip() == run_id:
                pivots.append(i)
        output = "".join(output[pivots[0] + 1 : pivots[1]])
        return output

    def run(self, cmd):
        cwd = Path().resolve()
        run_id = uuid.uuid4().hex
        work_dir = f"{cwd}/.pysh/{run_id}"
        Path(work_dir).mkdir(parents=True, exist_ok=True)
        script_file = f"{work_dir}/script.sh"
        exit_code = f"{work_dir}/exit_code"
        output_file = f"{work_dir}/output.txt"

        # setup logging and execute cmd
        cmd = f"echo {run_id}; {cmd}; echo $? > {exit_code}; echo {run_id}"
        with open(script_file, "w") as f:
            f.write(cmd)
        cmd = f"bash {script_file}"
        cmd = dedent(cmd)
        self.start_pipe(output_file)
        subprocess.run(["tmux", "send-keys", "-t", self.pane_id, cmd, "C-m"])
        self.wait_for_completion(exit_code)
        self.stop_pipe()

        # extract results
        with open(exit_code, "r") as f:
            exit_code = int(f.read().strip())
        with open(output_file, "r") as f:
            output = f.readlines()
        output = self.extract_output(output, run_id)

        # cleanup files
        shutil.rmtree(work_dir)

        return exit_code, output


class TmuxPane:
    def __init__(self):
        self.pane_id = self.create_pane()

    def create_pane(self):
        pane_id = subprocess.check_output(
            ["tmux", "split-window", "-hdP", "-F", "#{pane_id}"], text=True
        )
        pane_id = pane_id.strip()
        return pane_id

    def remove(self):
        subprocess.run(["tmux", "kill-pane", "-t", self.pane_id])

    def start_pipe(self, output_file):
        subprocess.run(
            ["tmux", "pipe-pane", "-t", self.pane_id, f"cat > {output_file}"]
        )

    def stop_pipe(self):
        subprocess.run(["tmux", "pipe-pane"])

    def wait_for_completion(self, exit_code):
        while True:
            if Path(exit_code).is_file():
                return
            time.sleep(0.1)

    def extract_output(self, output, run_id):
        pivots = []
        for i, l in enumerate(output):
            if l.strip() == run_id:
                pivots.append(i)
        output = "".join(output[pivots[0] + 1 : pivots[1]])
        return output

    def run(self, cmd):
        cwd = Path().resolve()
        run_id = uuid.uuid4().hex
        work_dir = f"{cwd}/.pysh/{run_id}"
        Path(work_dir).mkdir(parents=True, exist_ok=True)
        script_file = f"{work_dir}/script.sh"
        exit_code = f"{work_dir}/exit_code"
        output_file = f"{work_dir}/output.txt"

        # setup logging and execute cmd
        cmd = f"echo {run_id}; {cmd}; echo $? > {exit_code}; echo {run_id}"
        with open(script_file, "w") as f:
            f.write(cmd)
        cmd = f"bash {script_file}"
        cmd = dedent(cmd)
        self.start_pipe(output_file)
        subprocess.run(["tmux", "send-keys", "-t", self.pane_id, cmd, "C-m"])
        self.wait_for_completion(exit_code)
        self.stop_pipe()

        # extract results
        with open(exit_code, "r") as f:
            exit_code = int(f.read().strip())
        with open(output_file, "r") as f:
            output = f.readlines()
        output = self.extract_output(output, run_id)

        # cleanup files
        shutil.rmtree(work_dir)

        return exit_code, output


def get_shell():
    tmux = "TMUX" in os.environ
    if tmux:
        sh = TmuxPane()
    else:
        sh = TmuxSession()
    return sh


def run_cmd(cmd):
    sh = get_shell()
    e, o = sh.run(cmd)
    if "TMUX" in os.environ:
        print(f"Command failed with exit code: {exit_code}")
        print(f"ctrl-c to debug..")
        time.sleep(3)
    sh.remove()
    return e, o
