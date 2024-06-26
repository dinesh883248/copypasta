import shutil
import atexit
import os
import time
import uuid
import subprocess
from pathlib import Path
from textwrap import dedent


class Shell:
    def __init__(self):
        if not "TMUX" in os.environ:
            raise Exception("Not a tmux session")
        self.pane_id = self.create_pane()
        atexit.register(self.remove_pane)

    def create_pane(self):
        pane_id = subprocess.check_output(
            ["tmux", "split-window", "-hP", "-F", "#{pane_id}"], text=True
        )
        pane_id = pane_id.strip()
        return pane_id

    def remove_pane(self):
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
            time.sleep(0.5)

    def extract_output(self, output, run_id):
        pivots = []
        for i, l in enumerate(output):
            if l.strip() == run_id:
                pivots.append(i)
        output = "".join(output[pivots[0] + 1 : pivots[1]])
        return output

    def run(self, cmd):
        # init files
        cwd = Path().resolve()
        run_id = uuid.uuid4().hex
        work_dir = f"{cwd}/.pysh/{run_id}"
        Path(work_dir).mkdir(parents=True, exist_ok=True)
        script_file = f"{work_dir}/script.sh"
        exit_code = f"{work_dir}/exit_code"
        output_file = f"{work_dir}/output.txt"

        # setup logging and execute cmd
        cmd = f"echo {run_id}; {cmd}; echo {run_id}; echo $? > {exit_code}"
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
