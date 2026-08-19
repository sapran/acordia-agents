---
name: mobile-data-storage
description: Recover what a mobile app has written into its own sandbox — SharedPreferences and plists, SQLite databases, cached and backed-up files, log spill, clipboard and screenshot residue — on Android and iOS. Reach for it once you can read or pull the app container and the question is which sensitive data persists unprotected on disk.
metadata:
  acordia:
    family: mobile
---

# Mobile Data Storage

Mobile apps leak more through what they leave behind than through what they transmit. Every credential, token, PII record or business secret an app holds ends up somewhere in its sandbox: a preferences file, a SQLite database, a cache directory, a log line, the clipboard, or a screenshot the OS took when the app went to background. This skill enumerates those locations, pulls their contents, and judges whether the storage protection claimed by the app actually holds.

## Prerequisites

- A rooted Android device / emulator, or a debuggable build, or `run-as` on a debuggable package
- A jailbroken iOS device, or an app container reachable through Frida Gadget
- `objection` attached to the target: `objection -g <pkg-or-bundle-id> explore`

## Locating the sandbox

| Platform | Location | How to reach it |
|----------|----------|-----------------|
| Android | `/data/data/<pkg>/` — `shared_prefs/`, `databases/`, `files/`, `cache/`, `no_backup/` | `adb shell run-as <pkg> ls -la /data/data/<pkg>/` on a debuggable build; `adb pull /data/data/<pkg>/databases/` with root |
| Android | External storage — world-readable historically, still weakly scoped | `adb shell ls -la /sdcard/Android/data/<pkg>/` |
| iOS | Data container — `Documents/`, `Library/Preferences/<bundle-id>.plist`, `Library/Caches/`, `tmp/` | `objection` → `env` prints every container path, then `ls` and `cd` |
| Both | Whatever the app actually opened | `objection` → `env`, then walk it rather than trusting the documented layout |

## Preferences and key–value stores

- Android SharedPreferences: `adb pull /data/data/<pkg>/shared_prefs/` — plain XML, frequently holding session tokens and "encrypted" values that are base64
- Android Keystore entries — aliases, and whether each is hardware-backed: `objection` → `android keystore list`, then `android keystore detail --json`
- iOS NSUserDefaults: `objection` → `ios nsuserdefaults get`
- iOS Keychain, the whole entitlement group with its accessibility attributes: `objection` → `ios keychain dump`, and `ios keychain dump_raw` when the processed view drops fields
- iOS URL credential store and shared cookies: `objection` → `ios nsurlcredentialstorage dump`, `ios cookies get`
- iOS plists anywhere in the container: `objection` → `ios plist cat <path>`

A Keystore alias or a Keychain item proves only that a key exists. Whether the key protects anything is `mobile-crypto-keys`.

## Databases and files

- Pull databases wholesale: `adb pull /data/data/<pkg>/databases/`
- Query in place without pulling: `objection` → `sqlite connect <path>` , then ordinary SQL
- Retrieve a single artefact: `objection` → `filesystem download <remote-path> <local-path>`, or `filesystem download --folder <dir> <local-dir>`
- Read a file inline: `objection` → `filesystem cat <path>`
- Check `android:allowBackup` in the decoded manifest — when true, the sandbox is extractable without root
- Realm, LevelDB and Core Data stores sit in `files/` or `Library/Application Support/`; treat any unrecognised binary in the container as a store until proven otherwise

## Runtime spill

- Log spill during a sensitive operation: `adb logcat | grep <pkg>`, or scope by PID with `adb logcat --pid=$(adb shell pidof -s <pkg>)`
- Clipboard: `objection` → `android clipboard monitor` / `ios pasteboard monitor`, then drive the copy path in the app
- Backgrounding screenshots — the OS snapshots the current view unless the app blocks it. Check with `objection` → `android ui FLAG_SECURE true` to confirm the flag is *not* already set, and `android ui screenshot` / `ios ui screenshot` to capture what would be written
- Whole-process memory, where a decrypted record often outlives its file: `objection` → `memory dump all <file>`, then `memory search "<pattern>" --string`

## Evidence

Every storage finding needs the artefact itself: the pulled file or database row, the path it came from, the build and platform version, and the app action that produced it. A preference key named `auth_token` is not a finding; the token value, its path and the request it authenticates is.

## Boundary

This skill owns what is written to disk and how it is retrieved. How that data was encrypted, and where the key came from, is `mobile-crypto-keys`. The tooling that gets you attached, decompiled or hooked in the first place is `mobile-instrumentation`. Data reachable by another app through a content provider or deep link is `mobile-platform-ipc`. If detection or anti-debug prevents you from attaching at all, clear that first with `mobile-resilience-bypass`. Data in flight to the backend is the network and API surface, covered by the `wstg-*` bundles and `attack-idor-automation`.
