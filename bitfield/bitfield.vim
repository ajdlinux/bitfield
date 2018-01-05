" Vim syntax file
"   Jeremy Kerr <jk@ozlabs.org>, 2005


" Setup
if version < 600
	syntax clear
"elseif exists("b:current_syntax")
"	finish
endif

syn match bitfComment	/;.*$/

syn match regID		/\[\S\+\]/
syn match regParam	/^\(name\|width\)/

syn match fieldName	/.*/			contained
syn match fieldRange	/\d\(\d\|[,\:]\)*/	contained nextgroup=fieldName
syn region fieldDef	start=/^field:/ end=/$/	contains=fieldRange keepend

syn match valueName	/.*/			contained
syn match valueNo	/\d\+/			contained nextgroup=valueName
syn region valueDef	start=/^value:/ end=/$/	contains=valueNo keepend

if !exists("did_bitfield_syntax_inits")
let did_bitfield_syntax_inits = 1
hi link bitfComment	Comment

hi link regID		Type
hi link regParam	Keyword

hi link fieldDef	Keyword
hi link fieldRange	Number
"hi link fieldName	Identifier

hi link valueDef	Keyword
hi link valueNo		Number
hi link valueName	Identifier
endif

let b:current_syntax = "bitfield"
