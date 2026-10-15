// swift-tools-version: 6.0
import PackageDescription

// md3's modules (#102). Third-party dependencies (#42) are added, pinned to
// exact versions, by the task that first needs them (#174, security rule 3).
let package = Package(
    name: "md3",
    platforms: [.macOS("14.2")],
    products: [
        .library(name: "MD3Core", targets: ["MD3Core"]),
    ],
    targets: [
        // Real-time code (#52): C, no allocation, locks or logging on the audio thread.
        .target(name: "MD3RealTime"),
        .target(name: "MD3Core", dependencies: ["MD3RealTime"]),
        .testTarget(name: "MD3CoreTests", dependencies: ["MD3Core"]),
        .testTarget(name: "MD3RealTimeTests", dependencies: ["MD3RealTime"]),
    ]
)
