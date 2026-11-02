#if !RIG_STACK || !STACK_RUNNER_FIXTURE_LIB
#error Required sibling compile guards are absent
#endif
#warning declared fixture stack warning
public class Tests {
 [Xunit.Fact] public void CompilesSiblingSource() { Xunit.Assert.Equal("sibling-source", Runner.Fixture.Source.Unreleased()); }
}
