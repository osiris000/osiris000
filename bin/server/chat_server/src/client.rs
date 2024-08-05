use std::io::{self, Write};

fn main() {
    let mut input = String::new();

    loop {
        print!("Introduce un mensaje: ");
        io::stdout().flush().unwrap(); // Force output to be printed immediately

        match io::stdin().read_line(&mut input) {
            Ok(_) => {
                let input = input.trim(); // Remove trailing newline
                if input.is_empty() {
                    continue;
                }
                println!("Has dicho: {}", input);
                input.clear(); // Clear input for next iteration
            }
            Err(error) => {
                println!("Error: {}", error);
                break;
            }
        }
    }
}
