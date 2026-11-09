// Capstone Full-System Test: Runs Box.hack directly on Computer.hdl
// Student: Prachi Manwal (Roll No: 2501730365, K = 65)

load Computer.hdl,
ROM32K load Box.hack,

// Simulate pressing a key and running the Hack Computer (CPU + Memory + Screen + Keyboard)
repeat 1000 {
    tick, tock;
}
