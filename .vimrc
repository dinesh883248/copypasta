syntax on
set laststatus=0
set expandtab
set autoindent
set ignorecase
set ruler
set mouse=
set ttyfast
set hidden
set foldenable
set foldmethod=indent
set nowrap
hi clear texItalStyle
highlight Search ctermbg=gray

set pastetoggle=<F10>
set clipboard=unnamed

filetype plugin indent on
set sts=2 sw=2
au FileType python setlocal tabstop=4
au FileType python setlocal softtabstop=4
au FileType html setlocal tabstop=2
au FileType html setlocal shiftwidth=2
au FileType javascript setlocal tabstop=2
au FileType javascript setlocal shiftwidth=2
au FileType css setlocal tabstop=2
au FileType css setlocal shiftwidth=2
autocmd FileType go setlocal noexpandtab
autocmd FileType go setlocal sts=8
autocmd FileType go setlocal sw=8
autocmd FileType make setlocal noexpandtab
autocmd FileType make setlocal sts=8
autocmd FileType make setlocal sw=8
