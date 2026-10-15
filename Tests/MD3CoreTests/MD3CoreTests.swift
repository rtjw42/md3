import Testing
@testable import MD3Core

@Test func coreLinksRealTimeModule() {
    #expect(MD3Core.version == 1)
    #expect(MD3Core.realTimeVersion == 1)
}
