# COMMAND EXECUTION USING SEND-KEYS
1. You are in tmux session, there are 2 panes running, always use 2nd pane and send-keys to run a command.
2. Use capture-ouptut on 2nd pane to get the output.

# CODING STYLE FOR ALL LANGUAGES:
1. **Single-file, linear control flow**
   * no cross-file imports.
   * Inline, commented blocks are preferred over helper functions (create one only if you'd repeat ≥10 lines verbatim).

2. **Fail fast and loudly**
   * Don't wrap core logic in `try/except` unless you'll handle the error and then `sys.exit(1)`.
   * Let missing config, bad CLI calls, etc. raise their native exceptions.
   * Reserve `sys.exit(1)` for deliberate termination points that won't already raise.

3. **Configuration as mandatory ALL\_CAPS constants**
   * Immediately read `config.ini` with `configparser`.
   * Access each key directly (`cfg["SECTION"]["KEY"]`) so a missing key raises `KeyError`.
   * Promote every value to an ALL\_CAPS constant; never supply defaults.

4. **Prefer clarity over cleverness (WET > DRY)**
   * Duplicate straightforward statements instead of abstracting them away.
   * Keep syntax simple: moderate line lengths, no fancy comprehensions or decorators.
   * Use concise divider comments (`# ---- section ----`) for visual structure.

5. **Stay procedural: no classes, no type hints**
   * Script-style code only; skip OOP and type annotations.
   * A top-file docstring is fine; comments beat annotations elsewhere.

6. **Whitespace and comments are structural cues**
   * Use blank lines and block comments to create clear visual sections.
   * Target ≈88-character line length; wrap manually—avoid backslashes.

7. **Do the bare minimum**
   * Code should be bare minimum of our requirement, dont do extra stuff.
