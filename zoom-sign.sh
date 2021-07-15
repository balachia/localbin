#!/bin/sh

# https://github.com/johnboiles/obs-mac-virtualcam/issues/4

APPLICATION=/Applications/zoom.us.app && codesign -d --entitlements :- $APPLICATION | { xml2; echo "/plist/dict/key=com.apple.security.cs.disable-library-validation"; echo "/plist/dict/true"; } | 2xml > entitlements.xml && sudo codesign --sign - $APPLICATION --force --preserve-metadata=identifier,resource-rules,flags --entitlements=entitlements.xml && rm entitlements.xml
