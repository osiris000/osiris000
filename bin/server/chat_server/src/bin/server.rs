use tokio::net::TcpListener;
use tokio_tungstenite::accept_async;
use futures_util::{StreamExt, SinkExt};
use tokio_tungstenite::tungstenite::Message;
use chrono::DateTime;
use chrono::Local;
use std::error::Error;


// Estructura para manejar mejor el error
#[derive(Debug)]
struct OsirisError {
    message: String,
}

impl std::fmt::Display for OsirisError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{}", self.message)
    }
}

impl Error for OsirisError {}



// Función para obtener la fecha y hora actual
fn get_current_date() -> String {
    let now: DateTime<Local> = Local::now();
    format!("Fecha y hora actual: {}", now.to_rfc3339()).to_string()
}

// Función para manejar comandos específicos
fn handle_command(command: &str) -> Result<String, OsirisError> {
    match command {
        "/date" => Ok(get_current_date()),
        "/hello" => Ok("Hola, cliente! 👋".to_string()),
        "/help" => Ok(
            "/date - Obtiene la fecha y hora actual.\n/hello - Saludo de bienvenida.\n/help - Muestra esta ayuda.".to_string()
        ),
        "" => Ok("".to_string()), // Comando vacío
        _ => Err(OsirisError { message: format!("Comando no reconocido: {} 🤔", command) }),
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let addr = "127.0.0.1:8180";
    let listener = TcpListener::bind(addr).await?;
    println!("Servidor WebSocket escuchando en {}", addr);

    while let Ok((stream, _)) = listener.accept().await {
        tokio::spawn(handle_connection(stream));
    }

    Ok(())
}

async fn handle_connection(stream: tokio::net::TcpStream) -> Result<(), Box<dyn Error>> {
    let ws_stream = accept_async(stream).await?;
    println!("Nuevo cliente WebSocket conectado.");

    let (mut write, mut read) = ws_stream.split();

    while let Some(Ok(msg)) = read.next().await {
        let response = match msg {
            Message::Text(text) => handle_command(&text)?,
            Message::Binary(_) => "Mensaje binario recibido".to_string(),
            _ => "Tipo de mensaje no soportado".to_string(),
        };

        if write.send(Message::Text(response)).await.is_err() {
            println!("Error al enviar mensaje al cliente");
            break;
        }
    }
    println!("Cliente WebSocket desconectado.");
    Ok(())
}

fn main() {
    // Este main se usa solo para verificar la funcion handle_command
    // El main del servidor webSocket está arriba
    let commands = vec!["/date", "/hello", "/help", "/unknown", ""];

    for command in commands {
        match handle_command(command) {
            Ok(response) => println!("Respuesta: {}", response),
            Err(error) => println!("Error: {}", error),
        }
    }
}
