package fixture_test
import ("testing"; fixture "github.com/rigsmith/stack-examples-lib/go")
func TestSiblingSource(t *testing.T) { if got:=fixture.Unreleased(); got!="sibling-source" { t.Fatalf("got %q",got) } }
