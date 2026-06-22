//! Agent replaces this file with the full Launch Interceptor implementation.

use crate::types::{DecideInput, DecideOutput};

pub fn decide(_input: &DecideInput) -> DecideOutput {
    DecideOutput::from_fixed([false; 15], [[false; 15]; 15], [false; 15], false)
}
