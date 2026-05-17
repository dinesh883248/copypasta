### Aggresively reduce count_bytecode.py score as much as possible for python code.

- In each project, run `uv run count_bytecode.py <py_script>` on the py script that you create or change and it gives a score. We have to reduce this score aggresively.
- Do not put code in text and use 'exec' on it to reduce score, thats cheating.
- Record the score in score.md file.

### Python Module docstring

- Check that we must have 'MUST HAVE REQUIREMENTS' section at top of file.
- Code logic should never miss any 'MUST HAVE REQUIREMENTS'

## Tips to reduce bytecode score for python.

1. Remove unecssary instructions, like validations or checks, let it fail, thats ok because our priority is reducing bytecode score.
2. Using dictionary direct indexing rather than .get() attribute. For example dont use os.environ.get() or os.getenv() instead use os.environ["key"]
3. When in doubt whether to remove code or not always remove it, user can always ask you to put the code back if really needs it. Your goal is to aggresively lower the count_bytecode score.
4. Feel free to execute any piece of code with count_bytecode.py to check for its score. This helps to know whether score gets reduced or increased. Use below format if you just want to check score for adhoc pieces of code.
```py
uv run count_bytecode.py <<'PYCODE'
print("hi")
PYCODE
```
6. Do not compromise on naming convention because it doesn't contribute to bytecode score, having good naming is essential for code readability.

7. Favor literal definitions when possible—building lists/tuples/dicts in place avoids extra assignments.
8. Inline expressions and unpacking beats multiple temporary variables in tight loops; each additional instruction can raise the count.
10. Reject unused imports or helper functions; every definition creates more bytecode even if never executed.
s Comments should stay succinct; AGENTS.md already expects block separators, so only add them when they explain behavior necessary for understanding the lean code.
11. Dont access environment variables directly, either pass them as cmd line args or use django settings if inside django app.

### Using subprocess.
- we should prefer running subprocess without capture output, unless we strictly depend on output we should not capture output.
- Avoid capturing output just because you have to print or log the output for user info.

### Code readability and comments for python code.

1. Add more comments, especially block level comments that visually show what a particular block does.
2. Comments and blank lines do not add bytecode; feel free to use them so long as they stay focused and concise.
3. Use meaningful naming convention in code.
4. Add new lines where necessary to improve code readability.

### Logging
1. Implement logging from the outset. Provide real-time visibility into what’s happening, keeping output concise and information-dense without overwhelming the terminal.

## Python environment (uv)

- Use `uv init` to create `uv.lock` and a local `.venv/`.
- Install dependencies with `uv add <pkg>` (or project-appropriate `uv pip ...`).
- Run scripts/tools via `uv run ...` so the correct venv is used.

### Scripts should be run from project root directory.
- all the scripts are run from project root only, this is to reduce complexity and unecessary thinking.
- so with that in mind, we should always have relative paths in config.ini and scripts are expected to reach those files because we only run the scripts from project root only.
- no need to add guardrails like if file exists etc..let the script crash if it tries reading non existant file or if user runs the script for non project root where it can't then get hold of relative file.
- no need to resolve full path unless the specific remote transport absolutely requires it.
- use rsync not scp.
- if you have to create any temp files create them in relative tmp dir, create tmp dir if missing.
- make sure that systemd service files do change dir to project root and then run the scripts by relative path, no need to mention full path when it changes dir.
- dont create systemd serivce definitions in code, instead have .service files created and use those files rather than creating on demand via code.

### Standalone scripts design philosophy.
- prefer many small standalone scripts over shared helper modules.
- top-level command scripts must use meaningful action names like `submit_simulation.py`, not vague names like `controller.py` or `sync.py`.
- each script should do one clear job and be runnable on its own with `--config <path>`.
- scripts should not import other project scripts; keep each script self contained.
- if a script needs static files, keep them in a path relative to that script and reference them directly.
- favor explicit and linear flow over abstractions; readability is more important than deduplication.
- hardcoding and duplication are acceptable when they reduce branching and mental overhead.
- deterministic behavior is required; avoid hidden fallbacks and implicit magic.
- do not hide errors; raise/log errors close to the real culprit.
- prefer direct indexing like `dictionary["key"]` so missing keys raise `KeyError` naturally.
- use `.get()` only when allowing `None` is intentional behavior.
- naming should match role and intent clearly (cluster, node, worker, local).
- do not drift into helper-module webs for top-level command behavior.

### Simulator structure source of truth.
- `simulator/docs/fs_components.yaml` is the source of truth for the `simulator/components` structure.
- workflow yaml files under `simulator/components/extensions` are the source of truth for workflow execution order.
- Restructure code to match the yaml; do not change yaml casually to fit code drift.

### Git rules
- Don't do rebase

### SSH usage in python
- Always use paramiko for ssh connection, install it if not already installed using 'uv'
- Use paramiko with 'with' context.

