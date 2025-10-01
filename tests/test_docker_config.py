import pathlib


def test_docker_files_exist_and_have_expected_bits():
    root = pathlib.Path(__file__).resolve().parents[1]
    dockerfile = (root / "Dockerfile").read_text(encoding="utf-8")
    compose = (root / "docker-compose.yml").read_text(encoding="utf-8")

    # Dockerfile sanity
    assert "EXPOSE 7860" in dockerfile
    assert "ENV APP_PATH=app/demo_gradio.py" in dockerfile
    assert "GRADIO_SERVER_NAME" in dockerfile

    # Compose sanity: all services + distinct ports
    for svc, port in {
        "demo": "7860:7860",
        "docqa": "7861:7861",
        "chatbot": "7862:7862",
        "resume": "7863:7863",
        "reporting": "7864:7864",
    }.items():
        assert svc in compose, f"Service {svc} missing"
        assert port in compose, f"Port mapping {port} missing"
    assert "GRADIO_SERVER_NAME=0.0.0.0" in compose
