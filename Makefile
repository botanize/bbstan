all: stan.plist

subs:
	git submodule update --remote stan-language-definitions

clean:
	rm stan.plist

cleanall:
	rm stan.plist

install: stan.plist
	cp stan.plist ~/Library/Application\ Support/BBEdit/Language\ Modules/

uninstall:
	rm ~/Library/Application\ Support/BBEdit/Language\ Modules/stan.plist

stan.plist: subs stan-language-definitions/stan_lang.json make_bbedit_clm_plist.py
	python3 make_bbedit_clm_plist.py stan-language-definitions/stan_lang.json > stan.plist

.PHONY: clean cleanall subs install uninstall
