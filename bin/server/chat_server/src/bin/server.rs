use tokio::net::TcpListener;
use tokio_tungstenite::accept_async;
use futures_util::{StreamExt, SinkExt};
use tokio_tungstenite::tungstenite::Message;
use std::time::SystemTime;
use chrono::DateTime;
use chrono::Local;

#[tokio::main]
async fn main() -> tokio::io::Result<()> {
    let addr = "127.0.0.1:8080";
    let listener = TcpListener::bind(addr).await?;
    println!("Servidor WebSocket escuchando en {}", addr);

    while let Ok((stream, _)) = listener.accept().await {
        tokio::spawn(handle_connection(stream));
    }

    Ok(())
}

async fn handle_connection(stream: tokio::net::TcpStream) {
    let ws_stream = match accept_async(stream).await {
        Ok(ws) => ws,
        Err(e) => {
            eprintln!("Error durante el handshake WebSocket: {:?}", e);
            return;
        }
    };

    println!("Nuevo cliente WebSocket conectado.");

    let (mut write, mut read) = ws_stream.split();

    while let Some(message) = read.next().await {
        match message {
            Ok(msg) => {
                let response = match msg {
                    Message::Text(text) => handle_command(text),
                    Message::Binary(_) => "Mensaje binario recibido".to_string(),
                    _ => "Tipo de mensaje no soportado".to_string(),
                };

                if write.send(Message::Text(response)).await.is_err() {
                    println!("Error al enviar mensaje al cliente");
                    break;
                }
            }
            Err(e) => {
                println!("Error al recibir mensaje: {:?}", e);
                break;
            }
        }
    }
    println!("Cliente WebSocket desconectado.");
}

// Función para manejar comandos específicos
fn handle_command(command: String) -> String {
    match command.as_str() {
        "date" => get_current_date(),
        "hello" => "Hola, cliente!".to_string(),
        _ => format!("Comando no reconocido: {}", command),
    }
}

// Función para obtener la fecha y hora actual
fn get_current_date() -> String {
    let now = SystemTime::now();
    let datetime: DateTime<Local> = now.into();
    format!("Fecha y hora actual: {}", datetime.to_rfc3339())
}
