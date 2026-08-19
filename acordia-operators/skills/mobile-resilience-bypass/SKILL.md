---
name: mobile-resilience-bypass
description: Defeat a mobile app's self-protection so testing can begin — root and jailbreak detection, Frida and debugger detection, emulator checks, signature and integrity verification, and obfuscated control flow — then patch or repackage to make the bypass durable. Reach for it when the app refuses to launch, crashes on attach, or silently degrades once it decides the device is untrusted.
metadata:
  acordia:
    family: mobile
---

# Mobile Resilience Bypass

Resilience controls are not vulnerabilities in themselves; they are the obstacle between you and every other test. An app that exits on a rooted device, kills itself when Frida attaches, or refuses to run once resigned will block storage, crypto and IPC work entirely. This skill removes those checks, and then records how weak they were, because under MASVS-RESILIENCE their weakness is itself the finding.

## Prerequisites

- The app installed on a rooted Android device or jailbroken iOS device, or a repackaged build
- `objection` / `frida` reachable — see `mobile-instrumentation`
- Decompiled output for locating the check — see `mobile-instrumentation`

## Recognising which control fired

| Symptom | Likely control |
|---------|----------------|
| Dialog then clean exit at launch | Root/jailbreak detection |
| Crash the instant Frida attaches, launch fine otherwise | Frida/instrumentation detection |
| Works spawned, dies when attached later | Debugger or `ptrace` self-attach check |
| Runs, but a feature silently fails | Integrity or signature check with a soft response |
| Runs on hardware, refuses on emulator | Emulator fingerprinting |
| Resigned build won't start | Signature verification, or iOS entitlement mismatch |

Distinguish before bypassing. Bypassing root detection when the real check was on the signature wastes the whole session.

## Root and jailbreak detection

- First attempt, which covers the common libraries: `objection -g <pkg> explore` → `android root disable`, or `ios jailbreak disable`
- Run the bypass before the app finishes initialising, since most checks fire at launch: `objection -g <pkg> explore --startup-command "<bypass command>"`
- Where the check is bespoke, find it rather than guessing: `objection` → `android hooking search methods root`, `android hooking search methods jailbreak`, then `android hooking list class_methods <class>`
- Flip a boolean check without writing a script: `objection` → `android hooking set return_value <class>.<method> false`
- Observe the check to confirm you have the right one before flipping it: `objection` → `android hooking watch class_method <class>.<method> --dump-args --dump-backtrace --dump-return`
- Typical Android probes to grep for in the decompiled tree: `/system/bin/su`, `/system/xbin/su`, `test-keys` in `Build.TAGS`, `Runtime.getRuntime().exec("su")`, package names `com.topjohnwu.magisk` and `eu.chainfire.supersu`, and `PackageManager.getInstalledPackages`
- Typical iOS probes: `/Applications/Cydia.app`, `/bin/bash`, `/etc/apt`, a `fork()` that succeeds, and a write test outside the sandbox
- Simulating rather than hiding is sometimes the faster path when the app branches on the result: `android root simulate`, `ios jailbreak simulate`

## Anti-debugging and instrumentation detection

- Android: `Debug.isDebuggerConnected()`, `android:debuggable` in the manifest, and `TracerPid` read from `/proc/self/status`
- Native: a `ptrace(PTRACE_TRACEME)` self-attach so no debugger can attach afterwards
- Frida-specific: a scan of `/proc/self/maps` for `frida-agent`, a connect attempt against port 27042, and a check for the `re.frida.server` thread name
- Counters: rename the Frida server binary and run it on a non-default port with `frida-server -l 127.0.0.1:<port>`; use Gadget embedded in a repackaged APK instead of a server; hook the detection function itself with `android hooking set return_value`; hook the native reader before it fires with a `frida` script over `Interceptor.attach` on `open`/`fopen`
- Force the interpreter when hooks will not bind against optimised code: `objection` → `android deoptimize`

## Integrity, signature and tamper checks

- Where they live in the decompiled source: `PackageManager.getPackageInfo(..., GET_SIGNATURES)` and `GET_SIGNING_CERTIFICATES`, a hardcoded certificate hash compared at startup, a CRC over `classes.dex`, and Play Integrity / SafetyNet attestation calls
- On iOS: a check that the embedded provisioning profile matches, and a code-signature validation over the main binary
- Each is a boolean in the end. Locate it, watch it, then set its return value — the same three objection commands as above.
- Attestation performed *server-side* cannot be hooked away on the device; note it as a control that held rather than forcing it

## Repackaging for a durable bypass

Runtime hooks last one session. When the bypass must survive a restart, patch the app.

```bash
apktool d app.apk -o output/                    # decode to smali and resources
# edit output/AndroidManifest.xml: android:debuggable="true" on <application>,
# and/or patch the detection method in output/smali/... to return false
apktool b output/ -o patched.apk                # rebuild
zipalign -p -f 4 patched.apk aligned.apk
apksigner sign --ks debug.keystore aligned.apk  # resign; the original signature is gone
adb install -r aligned.apk
```

Two consequences to expect: a resigned build fails any signature check that is still live, so patch that check in the same pass; and `android:networkSecurityConfig` may need a user-CA trust anchor added for proxying to work afterwards.

An alternative that avoids resigning entirely is embedding Frida Gadget as a library in the repackaged APK, which gives you a hook point at process start without a running Frida server.

## Recording the finding

The bypass is a means, but the ease of it is the result. Record which controls existed, which single command defeated each, how long it took, and whether any check was enforced server-side. "Root detection present, defeated by `android root disable` in one command, no server-side attestation" is a MASVS-RESILIENCE finding in its own right.

## Boundary

This skill owns the self-protection controls and the patching that removes them. The instrumentation and repackaging toolchain itself is `mobile-instrumentation`. What you go on to read once the app runs is `mobile-data-storage`; the keys behind it are `mobile-crypto-keys`; the component surface is `mobile-platform-ipc`. Certificate pinning is a network control rather than a resilience one, and the traffic testing it unlocks is web and API work — the `wstg-*` bundles, `attack-jwt` and `attack-idor-automation`.
