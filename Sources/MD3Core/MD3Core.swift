import MD3RealTime

/// Shared module code for the md3 app. Placeholder until B2.1.1 (record types).
public enum MD3Core {
    public static let version = 1

    /// Version of the C real-time module this build links.
    public static var realTimeVersion: Int { Int(md3_realtime_version()) }
}
