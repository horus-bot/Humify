use axum::{Router, routing::get};
use std::net::SocketAddr;

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/hello", get(say_hello))
        .route("/bye", get(say_bye));

    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));

    println!("Server running at http://{}", addr);

    axum::serve(
        tokio::net::TcpListener::bind(addr).await.unwrap(),
        app,
    )
    .await
    .unwrap();
}

async fn say_hello() -> &'static str {
    "Hehehe it is working it seems"
}

async fn say_bye() -> &'static str {
    "bye bye"
}
