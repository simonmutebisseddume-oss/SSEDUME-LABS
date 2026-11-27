#!/usr/bin/env python3
"""Patch the generated android/ shell. Safe to run repeatedly.

- adds INTERNET / network-state / CAMERA permissions (flutter create only adds INTERNET for debug builds)
- marks the camera as optional so the app still installs on camera-less devices
- sets the launcher label
"""
import pathlib
import sys

manifest = pathlib.Path("android/app/src/main/AndroidManifest.xml")
if not manifest.exists():
    sys.exit("android/app/src/main/AndroidManifest.xml not found - run `flutter create . --platforms=android` first")

text = manifest.read_text(encoding="utf-8")

wanted = [
    '<uses-permission android:name="android.permission.INTERNET" />',
    '<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />',
    '<uses-permission android:name="android.permission.CAMERA" />',
    '<uses-feature android:name="android.hardware.camera" android:required="false" />',
]
missing = [w for w in wanted if w not in text]
if missing:
    block = "".join(f"    {w}\n" for w in missing)
    if "<application" not in text:
        sys.exit("No <application> tag found in manifest")
    text = text.replace("<application", block + "    <application", 1)

import re
text = re.sub(r'android:label="[^"]*"', 'android:label="SSEDDUME POS"', text, count=1)

manifest.write_text(text, encoding="utf-8")
print("AndroidManifest patched:", ", ".join(w.split('"')[1] for w in missing) or "nothing to do")
