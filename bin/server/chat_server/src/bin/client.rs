use tokio::io::{self, AsyncBufReadExt, BufReader};
use tokio_tungstenite::{connect_async, tungstenite::Message};
use futures_util::{StreamExt, SinkExt};
use std::io::Write; // Importa Write para flush síncrono

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "ws://127.0.0.1:8080";
    let (ws_stream, _) = connect_async(addr).await?;
    println!("Conectado al servidor WebSocket en {}", addr);

    let (mut write, mut read) = ws_stream.split();
    let stdin = io::stdin();
    let mut stdin_reader = BufReader::new(stdin);

    loop {
        let mut input = String::new();

        print!("Introduce un mensaje: ");
        std::io::stdout().flush().unwrap(); // Uso de flush síncrono

        // Leer línea de entrada estándar
        if let Err(e) = stdin_reader.read_line(&mut input).await {
            eprintln!("Error al leer la entrada estándar: {}", e);
            break;
        }

        let input = input.trim(); // Remover salto de línea al final
        if input.is_empty() {
            continue;
        }

        // Enviar el mensaje al servidor
        if let Err(e) = write.send(Message::Text(input.to_string())).await {
            eprintln!("Error al enviar el mensaje: {}", e);
            break;
        }

        // Recibir la respuesta del servidor
        if let Some(message) = read.next().await {
            match message {
                Ok(Message::Text(text)) => println!("Respuesta del servidor: {}", text),
                Ok(msg) => println!("Respuesta del servidor: {:?}", msg),
                Err(e) => eprintln!("Error al recibir mensaje: {:?}", e),
            }
        }
    }

    Ok(())
}
