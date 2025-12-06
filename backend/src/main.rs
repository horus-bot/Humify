use axum::{Router, http::Method, routing::get}; // this is the import part

#[tokio::main] // rust async suntime ... this lets me run the main function async 
async fn main() {
    // Create our router 
        let app = Router::new()
        .route("/hello", get(say_hello))
        .route("/bye", get(say_bye));

    println!("test server at http://127.0.0.1:3000");

    // Start the server
    axum::Server::bind(&"127.0.0.1:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn say_hello() -> &'static str {
    "Hehehe it is working it seems "
}

async fn say_bye() -> &'static str {
    "bye bye"
}