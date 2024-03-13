use tokio::net::{TcpListener, TcpStream};
use std::io::{Read, Write};

const PORT: u16 = 8080; // Puerto elegido

async fn handle_connection(mut stream: TcpStream) {
  // Leer datos del stream
  let mut buffer = [0; 1024];
  let n = stream.read(&mut buffer).await?;

  // Procesar datos (reemplazar con tu lógica)
  let respuesta = format!("¡Hola desde el servidor Rust! Enviaste: {}", &buffer[..n]);

  // Escribir respuesta
  stream.write_all(respuesta.as_bytes()).await?;
}

async fn start_server() -> Result<(), std::io::Error> {
  let listener = TcpListener::bind(format!("0.0.0.0:{}", PORT)).await?;
  println!("Servidor escuchando en el puerto {}", PORT);

  loop {
    let (stream, _) = listener.accept().await?;
    tokio::spawn(handle_connection(stream));
  }
}

#[tokio::main]
async fn main() -> Result<(), std::io::Error> {
  start_server().await
}
