import MD3Core
import SwiftUI

/// md3's entry point: a menu bar item only (no Dock icon, LSUIElement, #35).
@main
struct md3App: App {
    var body: some Scene {
        MenuBarExtra {
            Text("md3 (core \(MD3Core.version), real-time \(MD3Core.realTimeVersion))")
            Divider()
            Button("Quit md3") { NSApplication.shared.terminate(nil) }
                .keyboardShortcut("q")
        } label: {
            Text("md3")
        }
    }
}
