#!/usr/bin/env python3
"""
Create the file stan.plist for BBEdit from `stan_lang.json`.
"""
import json
import sys

template_start = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<!--
	Stan language module for BBEdit (https://mc-stan.org)
	Joey Reid
	
	Stan language definitions: https://github.com/jrnold/stan-language-definitions
	Version {!s}
-->
<dict>
	<key>BBEditDocumentType</key>
	<string>CodelessLanguageModule</string>
	<key>BBLMColorsSyntax</key>
	<true/>
	<key>BBLMIsCaseSensitive</key>
	<true/>
	<key>BBLMLanguageCode</key>
	<string>Stan</string>
	<key>BBLMLanguageDisplayName</key>
	<string>Stan</string>
	<key>BBLMScansFunctions</key>
	<true/>
	<key>BBLMCommentLineDefault</key>
	<string>//</string>
	<key>BBLMSuffixMap</key>
	<array>
		<dict>
			<key>BBLMLanguageSuffix</key>
			<string>.stan</string>
		</dict>
	</array>
	<key>Language Features</key>
	<dict>
		<key>Open Line Comments</key>
		<string>//</string>
		<key>Open Line Comments</key>
		<string>#</string>
		<key>Open Block Comments</key>
		<string>/*</string>
		<key>Close Block Comments</key>
		<string>*/</string>
		<key>Open Strings 1</key>
		<string>"</string>
		<key>Close Strings 1</key>
		<string>"</string>
		<key>End-of-line Ends Strings 1</key>
		<false/>
		<key>Escape Char in Strings 1</key>
		<string>\</string>
		<key>Identifier and Keyword Characters</key>
		<string>1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz.</string>
		<key>Prefix for Functions</key>
		<string/>
		<key>Open Parameter Lists</key>
		<string>(</string>
		<key>Close Parameter Lists</key>
		<string>)</string>
		<key>Open Statement Blocks</key>
		<string>{{</string>
		<key>Close Statement Blocks</key>
		<string>}}</string>
		<key>Prefix for Procedures</key>
		<string/>
		<key>Terminator for Prototypes 1</key>
		<string/>
		<key>Terminator for Prototypes 2</key>
		<string/>
		<key>String Pattern</key>
		<string><![CDATA[
		(?x:("(\\"|[^"\\r\\n]|[\\n\\r])*"))
		]]></string>
		<key>Comment Pattern</key>
		<string><![CDATA[
		(//.*$)|(#.*$)|(?s:/\*.*?\*/)
		]]></string>
		<key>Skip Pattern</key>
		<string><![CDATA[
		(?P>comment) | (?P>string)
		]]></string>
		<key>Function Pattern</key>
		<string><![CDATA[
		(?:.*?)?(?:\[.*?\])?\s+(?P<function_name>[A-Za-z][A-Za-z0-9_]+)(?P<parens>\((?>(?>[^()]+)|(?P>parens))*\))[\s\\n\\r]*?(?P<function>(?>(?P<braces>{{(?>(?>[^{{}}]+)|(?P>braces))*}})))
		]]></string>
	</dict>
	<key>BBLMKeywordList</key>
	<array>"""
template_end = """	</array>
</dict>
</plist>
"""

template_mid = """	</array>
	<key>BBLMPredefinedNameList</key>
	<array>"""

def tostr(x):
    return [str(y) for y in x]

def read_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        
    keywords = set()
    for k in data['keywords']:
        if k == "range_constraints":
            continue
        for x in data['keywords'][k]:
            # handle target separately
            if x == "target":
                continue
            keywords.add(x)
    
    blocks = {k for k in data['blocks']}
    
    reserved = set()
    for k in data['reserved']:
        for x in data['reserved'][k]:
            reserved.add(x)
    
    types = set()
    for k in data['types']:
        for x in data['types'][k]:
            types.add(x)
    
    functions = {k for k, v in data['functions'].items() if not v['operator']}
    distributions = {v['sampling'] for k, v in data['functions'].items() if v['sampling']}
    return {
        'distributions': distributions,
        'functions': functions,
        'keywords': keywords,
        'reserved': reserved,
        'types': types,
        'version': data['version'],
        'blocks': set(data['blocks']),
    }

def create_code(data):
    keywordlist = '\n'.join(['\t\t<string>{!s}</string>'.format(kw) for kw in data['keywords'] | data['reserved']])
    namelist = '\n'.join(['\t\t<string>{!s}</string>'.format(kw) for kw in data['distributions'] | data['functions'] | data['types'] | data['blocks']])
    template = '\n'.join([template_start.format(data['version']), keywordlist, template_mid, namelist, template_end])
    
    print(template)

if __name__ == '__main__':
    data = read_json(sys.argv[1])
    create_code(data)
