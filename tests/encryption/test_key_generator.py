from password_manager.encryption.key_generator import KeyGenerator


def test_generate():
    generator = KeyGenerator("password")
    key, metadata = generator.generate()
    assert len(key) == 32
    assert metadata.iterations == 1000_000
    assert metadata.hmac == 'SHA512'
