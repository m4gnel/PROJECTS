## Short Document — What to submit

1) What is Flutter?

- Flutter is a UI toolkit by Google for building natively compiled applications for mobile, web, and desktop from a single codebase using the Dart language.

2) What is WebView?

- A WebView is a widget that embeds web content (HTML/CSS/JS) inside a native application. In Flutter, `webview_flutter` provides a WebView widget and controller to load and interact with web pages.

3) How the Mobile Container works

- The Flutter app acts as a container. It starts with a splash screen then navigates to a WebView screen that loads the remote website via `WebViewController`.

4) App startup flow

- App launch → `main.dart` → `SplashScreen` (3s) → `WebViewScreen` → remote website loads.

5) Website load lifecycle

- `onPageStarted` → show loading indicator; `onPageFinished` → hide loading; `onWebResourceError` → show error UI with Retry.
