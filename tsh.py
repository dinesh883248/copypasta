import os
import atexit
import uuid
import subprocess


class TmuxBase:
    def __init__(self):
        self.unique_ps1 = f"tsh_{uuid.uuid4().hex}$ "
        self.id = self.create()
        self.pane_id = self.get_pane_id()
        subprocess.run(
            [
                "tmux",
                "send-keys",
                "-t",
                self.pane_id,
                f'PS1="{self.unique_ps1}"; clear',
                "C-m",
            ]
        )
        atexit.register(self.remove)

    def create(self):
        raise NotImplementedError

    def get_pane_id(self):
        raise NotImplementedError

    def exists(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    def remove_cmd(self, s):
        i = s.find("\n")
        if i != -1:
            return s[i + 1 :]
        return ""

    def capture_pane(self):
        captured_output = subprocess.check_output(
            ["tmux", "capture-pane", "-p", "-t", self.pane_id], text=True
        )
        return captured_output

    def get_recent_output(self, captured_output):
        pat = self.unique_ps1.strip()
        last_occurrence = captured_output.rfind(pat)
        second_last_occurrence = captured_output.rfind(pat, 0, last_occurrence)
        out = captured_output[
            second_last_occurrence + len(pat) : last_occurrence
        ].strip()
        return self.remove_cmd(out)

    def run(self, cmd, wait=True):
        signal_name = f"{uuid.uuid4().hex}"
        wrapped_command = f"{cmd}; tmux wait-for -S {signal_name}"
        subprocess.run(
            ["tmux", "send-keys", "-t", self.pane_id, wrapped_command, "C-m"]
        )
        if not wait:
            return

        subprocess.run(["tmux", "wait-for", signal_name])
        captured_output = self.capture_pane()
        recent_output = self.get_recent_output(captured_output)
        return recent_output


class TmuxSession(TmuxBase):
    def create(self):
        session_id = uuid.uuid4().hex
        subprocess.check_call(
            ["tmux", "new-session", "-x", "200", "-d", "-s", session_id]
        )
        return session_id

    def get_pane_id(self):
        return f"{self.id}:0.0"

    def exists(self):
        res = subprocess.run(["tmux", "has-session", "-t", self.id])
        return res.returncode == 0

    def remove(self):
        subprocess.run(
            ["tmux", "kill-session", "-t", self.id], stderr=subprocess.DEVNULL
        )


class TmuxPane(TmuxBase):
    def create(self):
        pane_id = subprocess.check_output(
            ["tmux", "split-window", "-hdP", "-F", "#{pane_id}"], text=True
        ).strip()
        return pane_id

    def get_pane_id(self):
        return self.id

    def exists(self):
        res = subprocess.run(["tmux", "list-panes", "-t", self.id])
        return res.returncode == 0

    def remove(self):
        subprocess.run(["tmux", "kill-pane", "-t", self.id], stderr=subprocess.DEVNULL)


def get_shell():
    tmux = "TMUX" in os.environ
    if tmux:
        sh = TmuxPane()
    else:
        sh = TmuxSession()
    return sh


def run_cmd(cmd):
    sh = get_shell()
    output = sh.run(cmd)
    sh.remove()
    return output
