use tokio::io::{ AsyncWriteExt, BufReader};
use tokio::net::TcpListener;
use tokio::task;

#[tokio::main]
async fn main() -> tokio::io::Result<()> {
    let addr = "127.0.0.1:8080";
    let listener = TcpListener::bind(addr).await?;
    println!("Servidor escuchando en {}", addr);

    loop {
        let (mut socket, _) = listener.accept().await?;
        println!("Nuevo cliente conectado.");

        let (reader, mut writer) = socket.split();
        let reader = BufReader::new(reader);

        task::spawn(async move {
            let mut buf = vec![0; 1024];
            loop {
                match reader.read(&mut buf).await {
                    Ok(0) => break, // Conexión cerrada
                    Ok(n) => {
                        let msg = String::from_utf8_lossy(&buf[..n]);
                        println!("Mensaje recibido: {}", msg);
                        if writer.write_all(&buf[..n]).await.is_err() {
                            break;
                        }
                    }
                    Err(e) => {
                        println!("Error al leer del cliente: {:?}", e);
                        break;
                    }
                }
            }
            println!("Cliente desconectado.");
        });
    }
}
