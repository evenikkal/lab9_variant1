use pyo3::prelude::*;

fn xor_encrypt_impl(text: &str, key: &str) -> String {
    let key_bytes = key.as_bytes();
    let key_len = key_bytes.len();

    text.as_bytes()
        .iter()
        .enumerate()
        .map(|(i, &b)| format!("{:02x}", b ^ key_bytes[i % key_len]))
        .collect::<Vec<_>>()
        .join("")
}

fn xor_decrypt_impl(hex: &str, key: &str) -> PyResult<String> {
    let key_bytes = key.as_bytes();
    let key_len = key_bytes.len();

    let bytes: Result<Vec<u8>, _> = (0..hex.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&hex[i..i + 2], 16))
        .collect();

    let bytes = bytes.map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("invalid hex: {e}"))
    })?;

    let decrypted: Vec<u8> = bytes
        .iter()
        .enumerate()
        .map(|(i, &b)| b ^ key_bytes[i % key_len])
        .collect();

    String::from_utf8(decrypted).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("invalid utf8: {e}"))
    })
}

#[pyfunction]
fn xor_encrypt(text: &str, key: &str) -> PyResult<String> {
    if key.is_empty() {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "key must not be empty",
        ));
    }
    Ok(xor_encrypt_impl(text, key))
}

#[pyfunction]
fn xor_decrypt(hex_text: &str, key: &str) -> PyResult<String> {
    if key.is_empty() {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "key must not be empty",
        ));
    }
    xor_decrypt_impl(hex_text, key)
}

#[pymodule]
fn rustcrypto(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(xor_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(xor_decrypt, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encrypt_decrypt_roundtrip() {
        let text = "hello world";
        let key = "secret";
        let encrypted = xor_encrypt_impl(text, key);
        assert_ne!(encrypted, text);
        let key_bytes = key.as_bytes();
        let key_len = key_bytes.len();
        let bytes: Vec<u8> = (0..encrypted.len())
            .step_by(2)
            .map(|i| u8::from_str_radix(&encrypted[i..i + 2], 16).unwrap())
            .collect();
        let decrypted: String = bytes
            .iter()
            .enumerate()
            .map(|(i, &b)| (b ^ key_bytes[i % key_len]) as char)
            .collect();
        assert_eq!(decrypted, text);
    }

    #[test]
    fn test_encrypt_produces_hex() {
        let result = xor_encrypt_impl("a", "k");
        assert!(result.chars().all(|c| c.is_ascii_hexdigit()));
        assert_eq!(result.len(), 2);
    }

    #[test]
    fn test_different_keys_produce_different_output() {
        let text = "test";
        let enc1 = xor_encrypt_impl(text, "key1");
        let enc2 = xor_encrypt_impl(text, "key2");
        assert_ne!(enc1, enc2);
    }

    #[test]
    fn test_empty_string_encrypts_to_empty() {
        let result = xor_encrypt_impl("", "key");
        assert_eq!(result, "");
    }
}