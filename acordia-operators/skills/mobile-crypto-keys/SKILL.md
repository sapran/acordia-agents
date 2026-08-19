---
name: mobile-crypto-keys
description: Judge a mobile app's cryptography and recover its key material — weak primitives and modes in decompiled code, hardcoded and predictably derived keys, Keystore and Keychain protection classes, and live key capture by hooking Cipher and CommonCrypto. Reach for it once ciphertext or a protected blob is in hand and the question is which algorithm produced it and where the key lives.
metadata:
  acordia:
    family: mobile
---

# Mobile Cryptography and Key Material

Client-side cryptography in a mobile app is only as strong as the key the client holds, and the client holds every key it uses. This skill answers two questions about any encrypted value on the device: was a sound algorithm used, and can the key be recovered — statically from the binary, or at runtime by hooking the moment the key reaches the crypto API.

## Prerequisites

- Decompiled source for static review — see `mobile-instrumentation` for `jadx` and `apktool`
- A running instance with Frida attached for the runtime path: `objection -g <pkg-or-bundle-id> explore`

## Static review of the decompiled code

Search the decompiled tree for primitives that fail outright and for key material committed into it.

```bash
grep -rn "password\|secret\|api_key\|token" jadx-output/ --include="*.java"
grep -rniE "AES/ECB|DES|3DES|RC4|MD5|SHA1\b" jadx-output/ --include="*.java"
grep -rn "SecretKeySpec\|IvParameterSpec\|PBEKeySpec\|SecureRandom\|setSeed" jadx-output/ --include="*.java"
```

What each hit means:

| Finding | Why it fails |
|---------|--------------|
| `Cipher.getInstance("AES/ECB/...")` | ECB leaks plaintext structure; identical blocks encrypt identically |
| `DES`, `3DES`, `RC4` | Broken or deprecated primitives |
| `MD5`, `SHA-1` for integrity or password hashing | Collision-prone; unsuitable as a password KDF at any iteration count |
| `new SecretKeySpec("literal".getBytes(), "AES")` | Hardcoded key — the whole scheme is decorative |
| A fixed `IvParameterSpec`, or an IV derived from the key | Reused IV destroys CBC/GCM security |
| `SecureRandom.setSeed(<constant>)` | Deterministic "random" key or IV |
| `PBEKeySpec` with a low iteration count or a constant salt | Key derivable by offline brute force |

On iOS, review the CommonCrypto call sites — `CCCrypt`, `CCCryptorCreate`, `kCCAlgorithmDES`, `kCCOptionECBMode` — and the SecItem attributes used when storing keys.

## Key storage: does the platform actually protect it

- Whether each Android Keystore alias is hardware-backed, which is the question that decides the finding: `objection` → `android keystore detail --json`. A software-backed key in a rooted-device threat model protects nothing. Listing the aliases in the first place is `mobile-data-storage`.
- Watch the app use the Keystore live, which shows which alias serves which operation: `objection` → `android keystore watch`
- iOS Keychain accessibility class per item — `kSecAttrAccessibleAlways` and `...AfterFirstUnlock` survive a locked device, `...WhenUnlockedThisDeviceOnly` is the defensible choice: `objection` → `ios keychain dump`
- A key material blob living in `shared_prefs/` or a plist rather than the platform store is a storage finding as well; record it in both places and see `mobile-data-storage` for retrieval

## Runtime key capture

Hooking beats reversing. The key is a plain byte array at the moment it enters the crypto API, whatever obfuscation produced it.

- Load a purpose-written hook against a spawned process: `frida -U -f <pkg> -l crypto-hook.js`
- Watch Android crypto entry points with arguments and returns dumped, no script needed:
  - `objection` → `android hooking watch class_method javax.crypto.spec.SecretKeySpec.$init --dump-args --dump-backtrace`
  - `objection` → `android hooking watch class_method javax.crypto.Cipher.doFinal --dump-args --dump-return`
  - `objection` → `android hooking watch class_method java.security.MessageDigest.digest --dump-args --dump-return`
- Find the app's own crypto wrapper before hooking blind: `objection` → `android hooking search methods encrypt`, and `android hooking list class_methods <class>`
- iOS CommonCrypto, monitored wholesale: `objection` → `ios monitor crypto`
- Force the interpreter when hooks fail to land against optimised code: `objection` → `android deoptimize`
- Recover a key that never touches a hooked API by searching process memory: `objection` → `memory dump all <file>`, then `memory search "<known-plaintext-or-prefix>" --string`

Where a boolean integrity or signature check gates the crypto path, `android hooking set return_value` flips it; that is bypass work and belongs to `mobile-resilience-bypass`.

## Evidence

A crypto finding is the recovered key or the decrypted plaintext, with the hook output or code reference that produced it, plus the ciphertext it opens. "Uses ECB" alone is a code-quality observation; pair it with a decrypted value to make it a finding.

## Boundary

This skill owns how data was encrypted and where the key came from. What is written to disk, and how it is pulled, is `mobile-data-storage`. The Frida, objection and jadx mechanics behind every command above are `mobile-instrumentation`. Detection or anti-debug that stops you attaching is `mobile-resilience-bypass`. Transport cryptography — TLS configuration and certificate pinning — is not here; nor are token contents, which are `attack-jwt`.
