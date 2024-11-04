#![deny(unsafe_code)]

pub mod lifetime_expansion;
pub mod references;
pub mod transmute;

pub use lifetime_expansion::*;
pub use transmute::transmute;
pub use references::{not_alloc, null, null_mut};

#[inline(always)]
pub fn construct_fake_string(ptr: *mut u8, cap: usize, len: usize) -> String {
	let sentinel_string = crate::transmute::<_, String>([0usize, 1usize, 2usize]);

	let mut actual_buf = [0usize; 3];
	actual_buf[sentinel_string.as_ptr() as usize] = ptr as usize;
	actual_buf[sentinel_string.capacity()] = cap;
	actual_buf[sentinel_string.len()] = len;

	std::mem::forget(sentinel_string);

	crate::transmute::<_, String>(actual_buf)
}
