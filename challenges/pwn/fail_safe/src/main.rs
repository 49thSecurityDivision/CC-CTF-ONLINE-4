use std::io::{stdin, stdout, Write};
use std::{fs, io, mem};

use fail_safe::construct_fake_string;

const CRED_LEN: usize = 16;

fn read_flag() {
    let contents = fs::read_to_string("/flag.txt").expect("Failed to find flag.txt. Contact an admin");
    println!("{contents}");
}

#[inline(never)]
pub fn main() -> io::Result<()> {
    use std::hint::black_box;

    let user: String = String::from("vr0n_the_internz");
    let pass: &[u8; CRED_LEN] = b"let_me_in_please";

    #[repr(C)]
    #[derive(Default)]
    struct Authentication {
        name_buf: [u8; CRED_LEN],
        password: [u8; CRED_LEN],
    }

    let mut auth = black_box(Authentication::default());

    let mut name = construct_fake_string(auth.name_buf.as_mut_ptr(), 1024usize, 0usize);

    println!("*---------------------------------------------------------*");
    println!("   Welcome to my Intern Project!!");
    println!("   I wrote a login function in memory");
    println!("   safe Rust!\n");
    println!("   The only problem is that it keeps segfaulting...\n");
    println!("   Also, I haven't finished the 'password' part of the code");
    println!("   so, you can only enter the username...\n");
    println!("   Enjoy!");
    println!("*---------------------------------------------------------*\n\n");

    println!("*---------------------------------------------------------*");
    print!("   Enter your username: ");
    stdout().flush()?;
    stdin().read_line(&mut name)?;
    println!("*---------------------------------------------------------*");

    if !(user.eq(&name)) {
        println!("*---------------------------------------------------------*");
        println!("   WRONG USER!");
        println!("*---------------------------------------------------------*\n\n");
        // TODO: Once we have completed the password code, add an 'exit' here
    } else {
        println!("*---------------------------------------------------------*");
        println!("   CORRECT USER!");
        println!("*---------------------------------------------------------*\n\n");
    }

    mem::forget(name);

    // Nothing after this works, since we don't populate password anywhere :)
    let password = &auth.password[0..CRED_LEN];

    println!("*---------------------------------------------------------*");
    println!("   Enter your password: ");
    println!("*---------------------------------------------------------*");
    if &password == pass {
        println!("*---------------------------------------------------------*");
        println!("   CORRECT PASSWORD!");
        println!("*---------------------------------------------------------*\n\n");

        read_flag();
    } else {
        println!("*---------------------------------------------------------*");
        println!("   WRONG PASSWORD!");
        println!("*---------------------------------------------------------*");
    }

    black_box(auth);

    Ok(())
}
