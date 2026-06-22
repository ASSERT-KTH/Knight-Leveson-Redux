//! Shared JSON wire types (must match `harnesses/json_protocol.py`).
//!
//! - JSON keys for parameters remain Pascal-style (`LENGTH1`, `Q_PTS`, …).
//! - Rust uses snake_case field names with serde rename (see `Parameters`).
//! - `numpoints` and discrete parameter counts are `usize` so typical loops
//!   `for i in 0..input.numpoints` produce `usize` indices for `input.x[i]`.
//! - `DecideOutput` uses `Vec` so JSON matches Python; build with `vec![...]` or
//!   call `.to_vec()` on fixed arrays (`[bool; 15]`, `[[bool; 15]; 15]`).

use serde::{Deserialize, Serialize};

pub const LT: &str = "LT";
pub const EQ: &str = "EQ";
pub const GT: &str = "GT";

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct Parameters {
    #[serde(rename = "LENGTH1")]
    pub length1: f64,
    #[serde(rename = "RADIUS1")]
    pub radius1: f64,
    #[serde(rename = "EPSILON")]
    pub epsilon: f64,
    #[serde(rename = "AREA1")]
    pub area1: f64,
    #[serde(rename = "Q_PTS")]
    pub q_pts: usize,
    #[serde(rename = "QUADS")]
    pub quads: usize,
    #[serde(rename = "DIST")]
    pub dist: f64,
    #[serde(rename = "N_PTS")]
    pub n_pts: usize,
    #[serde(rename = "K_PTS")]
    pub k_pts: usize,
    #[serde(rename = "A_PTS")]
    pub a_pts: usize,
    #[serde(rename = "B_PTS")]
    pub b_pts: usize,
    #[serde(rename = "C_PTS")]
    pub c_pts: usize,
    #[serde(rename = "D_PTS")]
    pub d_pts: usize,
    #[serde(rename = "E_PTS")]
    pub e_pts: usize,
    #[serde(rename = "F_PTS")]
    pub f_pts: usize,
    #[serde(rename = "G_PTS")]
    pub g_pts: usize,
    #[serde(rename = "LENGTH2")]
    pub length2: f64,
    #[serde(rename = "RADIUS2")]
    pub radius2: f64,
    #[serde(rename = "AREA2")]
    pub area2: f64,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct DecideInput {
    pub numpoints: usize,
    pub x: Vec<f64>,
    pub y: Vec<f64>,
    pub parameters: Parameters,
    pub lcm: Vec<Vec<String>>,
    pub pum_diag: Vec<bool>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct DecideOutput {
    pub cmv: Vec<bool>,
    pub pum: Vec<Vec<bool>>,
    pub fuv: Vec<bool>,
    pub launch: bool,
}

impl DecideOutput {
    /// Convenience when `cmv` / `pum` / `fuv` are built as fixed-size arrays.
    pub fn from_fixed(
        cmv: [bool; 15],
        pum: [[bool; 15]; 15],
        fuv: [bool; 15],
        launch: bool,
    ) -> Self {
        Self {
            cmv: cmv.to_vec(),
            pum: pum.iter().map(|row| row.to_vec()).collect(),
            fuv: fuv.to_vec(),
            launch,
        }
    }
}

/// Tolerance-based six-significant-digit comparison from the oracle.
pub fn realcompare(a: f64, b: f64) -> &'static str {
    let scale = a.abs().max(b.abs());
    if scale == 0.0 {
        return "EQ";
    }
    let eps = 0.5e-5 * scale;
    let diff = a - b;
    if diff > eps {
        "GT"
    } else if diff < -eps {
        "LT"
    } else {
        "EQ"
    }
}
