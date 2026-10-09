import SwiftUI

/// md3's entry point: a menu bar item only (no Dock icon, LSUIElement, #35).
@main
struct md3App: App {
    var body: some Scene {
        MenuBarExtra {
            Text("md3")
            Divider()
            Button("Quit md3") { NSApplication.shared.terminate(nil) }
                .keyboardShortcut("q")
        } label: {
            Text("md3")
        }
    }
}
