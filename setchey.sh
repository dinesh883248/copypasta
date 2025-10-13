#!/bin/bash
set -e

# ====================================================================
# INSTALL COMMON PKGS
# ====================================================================
sudo apt-get update
sudo apt-get install -y neovim wget curl net-tools dnsutils dig socat netcat-openbsd tree python3-venv git zip unzip fzf ripgrep

# ====================================================================
# SETUP BASHRC
# ====================================================================
cat <<'BASHRC' > ~/.bashrc
# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

# User specific aliases and functions
if [ -d ~/.bashrc.d ]; then
	for rc in ~/.bashrc.d/*; do
		if [ -f "$rc" ]; then
			. "$rc"
		fi
	done
fi

unset rc

set -o vi
alias vim=nvim

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

export PATH=$PATH:/usr/local/go/bin

[ -f ~/.fzf.bash ] && source ~/.fzf.bash

_fzf_nvim() {
  local file
  file="$(fzf)"
  if [[ -n "$file" ]]; then
    nvim "$file"
  fi
}
bind -x '"\C-p": _fzf_nvim'

mkcd () { mkdir -p -- "$1" && cd -- "$1"; }
BASHRC

# ====================================================================
# SETUP BASH PROFILE
# ====================================================================
cat <<'BASHPROFILE' > ~/.bash_profile
# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi
BASHPROFILE

# ====================================================================
# SETUP NVIM CONFIG
# ====================================================================
mkdir -p ~/.config/nvim
cat <<'NVIMINITSTUFF' > ~/.config/nvim/init.lua
-- Set leader key
vim.g.mapleader = " "

-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    lazypath
  })
end
vim.opt.rtp:prepend(lazypath)

-- Load plugins
require("lazy").setup({
  -- Finder
  {
    "ibhagwan/fzf-lua",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      local fzf = require("fzf-lua")
      fzf.setup({
        winopts = {
          height = 0.30,
          width  = 1.00,
          row    = 1,
          col    = 0,
          border = "none",
          preview = { hidden = "hidden" },
        },
        fzf_opts = {
          ["--layout"] = "default",
        },
        files = { fd_opts = "--hidden --follow --exclude .git" },
      })
      vim.keymap.set("n", "<C-p>", fzf.files, { desc = "Find files" })
      vim.keymap.set("n", "<leader>f", fzf.files, { desc = "Find files" })
      vim.keymap.set("n", "<leader>g", fzf.live_grep, { desc = "Live grep" })
    end,
  },

  -- GitHub Copilot
  {
    "github/copilot.vim",
    config = function()
      vim.cmd("Copilot enable")
    end,
  },

  -- Formatter orchestrator
  {
    "stevearc/conform.nvim",
    event = { "BufWritePre" },
    cmd = { "ConformInfo" },
    config = function()
      require("conform").setup({
        formatters_by_ft = {
          javascript        = { "prettier" },
          javascriptreact   = { "prettier" },
          typescript        = { "prettier" },
          typescriptreact   = { "prettier" },
          json              = { "prettier" },
          html              = { "prettier" },
          css               = { "prettier" },
          scss              = { "prettier" },
          markdown          = { "prettier" },
          yaml              = { "prettier" },

          python            = { "black", "isort" },
          lua               = { "stylua" },
          go                = { "gofmt" },
          rust              = { "rustfmt" },
          sh                = { "shfmt" },
          terraform         = { "terraform_fmt" },

          c                 = { "clang_format" },
          cpp               = { "clang_format" },
          java              = { "google-java-format" },
        },
        format_on_save = {
          lsp_fallback = true,
          timeout_ms = 1000,
        },
      })
    end,
  },

  -- Auto-detect indentation from existing files
  { "tpope/vim-sleuth" },
  -- Honor .editorconfig when present
  { "editorconfig/editorconfig-vim" },
})

-- =====================
-- Basic Vim Configuration
-- =====================
vim.opt.cursorline = true
vim.opt.termguicolors = true
vim.opt.smartindent = true
vim.opt.laststatus = 0

-- Search
vim.opt.ignorecase = true

-- Navigation
vim.opt.scrolloff = 8
vim.opt.sidescrolloff = 8

-- Performance
vim.opt.updatetime = 250
vim.opt.timeoutlen = 400

-- Folding
vim.opt.foldenable = true
vim.opt.foldmethod = "indent"
vim.opt.foldlevel = 99
vim.opt.foldnestmax = 3

-- Clipboard
vim.opt.clipboard = { "unnamed", "unnamedplus" }

-- =====================
-- Indentation: sensible globals + overrides
-- =====================
-- Global soft-indentation defaults (apply while typing in new/adhoc files)
vim.opt.expandtab   = true
vim.opt.shiftwidth  = 2
vim.opt.softtabstop = 2
vim.opt.tabstop     = 2

-- Helper to set buffer-local options for specific filetypes
local function set_indent(fts, opts)
  vim.api.nvim_create_autocmd("FileType", {
    pattern = fts,
    callback = function()
      -- Defer to ensure we run after ftplugins/sleuth/editorconfig
      vim.defer_fn(function()
        for k, v in pairs(opts) do
          vim.opt_local[k] = v
        end
      end, 0)
    end,
  })
end

-- Web stack: 2 spaces
set_indent({ "javascript", "javascriptreact", "typescript", "typescriptreact", "json", "html", "css", "scss", "yaml", "yml", "markdown" }, {
  expandtab = true, shiftwidth = 2, softtabstop = 2, tabstop = 2,
})

-- Python: 4 spaces
set_indent({ "python" }, { expandtab = true, shiftwidth = 4, softtabstop = 4, tabstop = 4 })

-- Go: tabs (gofmt)
set_indent({ "go" }, { expandtab = false, shiftwidth = 8, tabstop = 8, softtabstop = 0 })

-- Makefiles: must be hard tabs
set_indent({ "make" }, { expandtab = false, tabstop = 8, shiftwidth = 8, softtabstop = 0 })

-- C-family, Java, C#, Rust, Kotlin, Scala: 4 spaces
set_indent({ "c", "cpp", "objc", "objcpp", "java", "cs", "rust", "kotlin", "scala" }, {
  expandtab = true, shiftwidth = 4, softtabstop = 4, tabstop = 4,
})
NVIMINITSTUFF

# ====================================================================
# SETUP NODEJS
# ====================================================================
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
\. "$HOME/.nvm/nvm.sh"
nvm install 22

npm install --global @ast-grep/cli
