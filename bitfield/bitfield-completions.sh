# completion for bitfield program
_bitfield_list() {
	bitfield --list | awk '{print $1}'
}

_bitfield() {
	local cur prev

        COMPREPLY=()
        cur=${COMP_WORDS[COMP_CWORD]}
        prev=${COMP_WORDS[COMP_CWORD-1]}

	# help, search, list: no completions
	if [[ "$prev" == '-h' || "$prev" == '-s' || "$prev" == '-l' ]]
	then
		return 0
	fi

	opts="--help --search --list --non-zero"

	# complete -* with long options.
	if [[ "$cur" == -* ]]
	then
		COMPREPLY=($(compgen -W "$opts" -- $cur))
		return 0
	fi

	# first parameter on line - complete with options + list of bitfields
	# FIXME: presence of -n will disable this...
	if [ $COMP_CWORD -eq 1 ]
	then
		COMPREPLY=($(compgen -W "$opts $(_bitfield_list)" -- $cur))
		return 0
	fi
}

complete -F _bitfield filenames bitfield
