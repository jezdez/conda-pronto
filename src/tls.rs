#[cfg(feature = "rustls-tls")]
pub(crate) fn install_default_provider() {
    let _ = rustls::crypto::ring::default_provider().install_default();
}

#[cfg(not(feature = "rustls-tls"))]
pub(crate) fn install_default_provider() {}
