---
name: mobile-platform-ipc
description: Attack a mobile app through the platform's own component surface — exported activities, services, receivers and content providers, deep links and custom URL schemes, and unsafe WebView bridge settings. Reach for it when the entry point under test is another app or a URL the OS hands to the target, rather than the target's own user interface.
metadata:
  acordia:
    family: mobile
---

# Mobile Platform Interaction and IPC

An Android app is not one process boundary but many. Every exported component is an entry point any other installed app — or any web page, through a deep link — can invoke without holding a single credential. This skill enumerates that surface, drives each entry point with attacker-controlled input, and covers the WebView, which is the bridge that turns a rendered page into native execution.

## Prerequisites

- The decoded manifest — see `mobile-instrumentation` for the decode, then read `output/AndroidManifest.xml`
- A device with the target installed, and `adb` reachable
- The `drozer` agent installed and its console connected — see `mobile-instrumentation`
- On iOS, the `Info.plist` `CFBundleURLTypes` and `com.apple.developer.associated-domains` entitlement

## Enumerating the exposed surface

- The whole attack surface in one call: `drozer` → `run app.package.attacksurface <pkg>` — counts exported activities, services, receivers and providers
- Per component type: `run app.activity.info -a <pkg>`, `run app.service.info -a <pkg>`, `run app.broadcast.info -a <pkg>`, `run app.provider.info -a <pkg>`
- From the manifest directly: any component with `android:exported="true"`, or with an `<intent-filter>` and no explicit `exported` attribute on an older `targetSdkVersion`
- Live registration, which catches components added at runtime: `objection` → `android hooking list activities`, `android hooking list services`, `android hooking list receivers`
- Package-level view including permissions: `adb shell dumpsys package <pkg>`

A component protected by a `signature`-level permission is not reachable from an unrelated app. Check `android:permission` and `android:protectionLevel` before claiming exposure.

## Driving components

- Launch an exported activity, the classic authentication-screen bypass: `adb shell am start -n <pkg>/<pkg>.TargetActivity`
- With a crafted intent, extras included: `drozer` → `run app.activity.start --component <pkg> <pkg>.TargetActivity --action android.intent.action.VIEW --extra string user admin`
- From inside the app's own process, which sidesteps export restrictions and shows what the component does when reached: `objection` → `android intent launch_activity <pkg>/<activity>`, `android intent launch_service <pkg>/<service>`
- Broadcasts and services: `drozer` → `run app.broadcast.send --component <pkg> <receiver> --extra string key value`, `run app.service.start --component <pkg> <service>`
- Implicit intents the app itself sends, which may carry sensitive extras to any app that registers the filter: `objection` → `android intent implicit_intents --dump-backtrace`

## Content providers

- Enumerate reachable URIs: `drozer` → `run app.provider.finduri <pkg>`, and `run scanner.provider.finduris -a <pkg>`
- Read one: `drozer` → `run app.provider.query content://<authority>/<path> --vertical`, or `adb shell content query --uri content://<authority>/<path>`
- SQL injection in the provider's selection handling: `drozer` → `run scanner.provider.injection -a <pkg>`, and enumerate the schema with `run scanner.provider.sqltables -a <pkg>`
- Path traversal through a `FileProvider` or a custom `openFile` implementation: `drozer` → `run scanner.provider.traversal -a <pkg>`
- Write access where the provider grants it: `drozer` → `run app.provider.update` / `run app.provider.insert`

A provider that returns another user's rows is an authorisation failure on the device rather than in the API; the equivalent server-side test is `attack-idor-automation`.

## Deep links and custom schemes

- Fire a link with a payload in the parameter: `adb shell am start -a android.intent.action.VIEW -d "scheme://host/path?param=payload"`
- Enumerate registered schemes and hosts from the manifest's `<data>` elements, including App Links with `android:autoVerify="true"` — an unverified App Link can be claimed by another app
- Test what the handler trusts: an identifier in the path, a token in a query parameter, a target URL that becomes a redirect or a WebView load
- On iOS, drive a custom scheme from the device: `xcrun simctl openurl booted "scheme://host/path?param=payload"` on the simulator, or a link tapped from Notes on hardware
- Where the parameter reaches a redirect or a server-side fetch, the payload construction is `attack-open-redirect` and `attack-ssrf`; the finding remains a mobile one because the entry point is the OS

## WebView

Read every `WebSettings` call site in the decompiled source, and check each against what the WebView actually loads:

| Setting | Risk when enabled |
|---------|-------------------|
| `setJavaScriptEnabled(true)` | Any injected or remote content executes script in the WebView |
| `addJavascriptInterface(obj, "name")` | Script calls annotated native methods — with `setJavaScriptEnabled` and untrusted content, this is code execution in the app's context |
| `setAllowFileAccess(true)` | The WebView loads `file://` URLs; combined with a deep link that controls the URL, it reads the app sandbox |
| `setAllowFileAccessFromFileURLs(true)` | Script in a local file reads other local files |
| `setAllowUniversalAccessFromFileURLs(true)` | Script in a local file reads any origin — same-origin policy gone |
| `setJavaScriptCanOpenWindowsAutomatically`, missing `shouldOverrideUrlLoading` validation | The loaded origin is attacker-controllable |

Confirm dynamically rather than from the code alone: `objection` → `android hooking watch class_method android.webkit.WebView.loadUrl --dump-args --dump-backtrace` shows exactly which URLs are loaded and from where. Then reach a controlled URL through a deep link and test whether the bridge is callable from it.

## Boundary

This skill owns the component and URL-handling surface the operating system exposes, and the WebView bridge. Data at rest inside the sandbox that a provider happens to expose is `mobile-data-storage`; the encryption over it is `mobile-crypto-keys`. Installing the drozer agent, decompiling and attaching are `mobile-instrumentation`. Detection that blocks instrumentation is `mobile-resilience-bypass`. Authorisation logic enforced by the backend, not by the component, belongs to `wstg-auth-session` and `attack-idor-automation`.
