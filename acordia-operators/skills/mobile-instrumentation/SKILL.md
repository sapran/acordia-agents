---
name: mobile-instrumentation
description: Operate the mobile testing toolchain itself — adb, frida, objection, drozer, jadx, apktool, MobSF and the iOS binary tools — to decompile a package, spawn or attach to a process, enumerate and hook classes, walk the heap and dump memory. Reach for it for the mechanics of getting a decompile or a hook in place; the sibling mobile-* skills say what to look for once you have one.
metadata:
  acordia:
    family: mobile
---

# Mobile Instrumentation

Every other mobile technique assumes you already have a decompiled tree or a live hook. This skill is how you get them: obtaining the package, decompiling it, attaching to the running process, and using the runtime primitives — class enumeration, method watching, heap search, memory dump — that the storage, crypto, IPC and resilience skills each build on.

## Tools

| Tool | Purpose |
|------|---------|
| adb | Android Debug Bridge — device shell, file transfer, package management, logs |
| apktool | APK decode to smali and resources, and rebuild |
| jadx | DEX → Java decompiler, CLI and GUI |
| frida | Dynamic instrumentation and hooking, Android and iOS |
| objection | Runtime mobile exploration built on Frida, no script required |
| drozer | Android IPC and component security testing |
| mitmproxy / Burp | Traffic interception and manipulation |
| MobSF | Automated static and dynamic analysis, first-pass triage |
| class-dump / jtool2 | iOS binary and Objective-C class analysis |

## Obtaining the package

```bash
adb shell pm list packages -3                    # third-party packages only
adb shell pm path <pkg>                          # APK paths, split APKs included
adb pull /data/app/<...>/base.apk                # retrieve it
adb install -r app.apk                           # install or reinstall
```

On iOS, pull the decrypted binary from a jailbroken device with a dump tool rather than the App Store IPA, which is FairPlay-encrypted and will not disassemble.

## Static: decompiling

```bash
apktool d app.apk -o output/                     # smali + decoded AndroidManifest.xml and resources
jadx -d jadx-output app.apk                      # Java source
jadx --deobf -d jadx-output app.apk              # rename obfuscated identifiers deterministically
jadx-gui app.apk                                 # interactive, for following call graphs
```

Read `output/AndroidManifest.xml` first — it names the package, the `targetSdkVersion`, every exported component, `android:debuggable`, `android:allowBackup` and `android:networkSecurityConfig`. MobSF over the same APK gives a fast triage list, but treat its output as leads to confirm, never as findings.

On iOS, `class-dump` over the decrypted binary reconstructs the Objective-C class interfaces, and `jtool2` reads the load commands, entitlements and encryption info.

## Dynamic: attaching

```bash
frida-ps -U                                      # processes on the USB device
frida-ps -Ua                                     # running applications, with identifiers
frida -U -f <pkg> -l script.js                   # spawn, inject at start, and hold
frida -U -n <process> -l script.js               # attach to a process already running
frida-trace -U -i "open" -f <pkg>                # auto-generate stubs for matching native functions
```

Spawning with `-f` matters whenever the interesting code runs before you could attach — startup checks, key derivation, first network call.

Objection wraps the same engine with a REPL:

```bash
objection -g <pkg-or-bundle-id> explore
objection -g <pkg> explore --startup-command "<command to run before the app initialises>"
```

Inside the REPL, `env` prints the app's paths, `ls`/`cd`/`pwd` walk the sandbox, `frida` reports the agent state, `jobs list` and `jobs kill <id>` manage running hooks, and `import <path>` loads a Frida script alongside them.

## Runtime primitives

Enumeration and hooking, Android:

- `android hooking list classes` — every loaded class; `android hooking list class_methods <class>` for its methods
- `android hooking search classes <pattern>` / `android hooking search methods <pattern>` — locate code by name
- `android hooking get current_activity` — where the UI actually is
- `android hooking watch class_method <class>.<method> --dump-args --dump-backtrace --dump-return` — the workhorse: arguments, caller and return for every invocation
- `android hooking set return_value <class>.<method> false` — boolean overrides
- `android hooking notify <class> --watch` — act the moment a lazily-loaded class appears
- `android hooking generate simple <class>` — emit a Frida script skeleton to extend by hand
- `android deoptimize` — force interpretation when hooks will not bind
- `android shell_exec <cmd>` — a shell in the app's own UID context

iOS equivalents: `ios hooking list classes`, `ios hooking list class_methods <class> --include-parents`, `ios hooking watch <pattern> --dump-args --dump-return`, `ios hooking set return_value`, `ios info binary`, `ios bundles list_frameworks`.

Heap and memory:

- `android heap search instances <class>` — find live objects, then `android heap print fields <handle>` to read their state and `android heap execute <handle> <method>` to call a method on an object that already holds initialised context
- `ios heap search instances <class>`, `ios heap print ivars <handle> --to-utf8`
- `memory list modules` / `memory list exports <module>` — the native surface
- `memory dump all <file>`, then `memory search "<pattern>" --string` — recover values that never pass through a hookable API
- `memory write` and `memory replace` — patch in place; disruptive, use last

Android component testing runs through drozer instead, over a forwarded port:

```bash
adb forward tcp:31415 tcp:31415
drozer console connect
run app.package.attacksurface <pkg>
```

## Proxying

Route the device through mitmproxy or Burp, install the CA into the user store, and set the proxy per app rather than device-wide where possible: `objection` → `android proxy set <host> <port>`. Certificate-pinning bypass is the mobile-application agent's own network step and is not restated here; where the pinning is bespoke, locate and hook it with the enumeration and watch commands above.

## Boundary

This skill owns the toolchain and the runtime primitives. What to look for with them lives elsewhere: files and stores in `mobile-data-storage`, algorithms and keys in `mobile-crypto-keys`, exported components and WebView in `mobile-platform-ipc`, detection and repackaging in `mobile-resilience-bypass`. Once traffic is flowing to the backend, the testing is web and API work — `recon-methodology`, the `wstg-*` bundles, `attack-jwt` and `attack-idor-automation`.
