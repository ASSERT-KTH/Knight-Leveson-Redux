//! JSON-lines harness: one `DecideInput` JSON per stdin line, one `DecideOutput` per stdout line.

mod decide;
mod types;

use std::io::{self, BufRead, Write};

use types::{DecideInput, DecideOutput};

fn main() {
    let stdin = io::stdin();
    let mut stdout = io::stdout();
    for line in stdin.lock().lines() {
        let line = match line {
            Ok(l) => l,
            Err(_) => break,
        };
        if line.trim().is_empty() {
            continue;
        }
        let input: DecideInput = match serde_json::from_str(&line) {
            Ok(v) => v,
            Err(e) => {
                eprintln!("json input error: {e}");
                continue;
            }
        };
        let out: DecideOutput = decide::decide(&input);
        match serde_json::to_string(&out) {
            Ok(s) => {
                let _ = writeln!(stdout, "{s}");
                let _ = stdout.flush();
            }
            Err(e) => eprintln!("json output error: {e}"),
        }
    }
}
