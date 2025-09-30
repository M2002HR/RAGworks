import pathlib

def test_docker_files_exist_and_have_expected_bits():
    root = pathlib.Path(__file__).resolve().parents[1]
    dockerfile = (root / "Dockerfile").read_text(encoding="utf-8")
    compose = (root / "docker-compose.yml").read_text(encoding="utf-8")

    assert "EXPOSE 7860" in dockerfile
    assert "app/demo_gradio.py" in dockerfile
    assert "7860:7860" in compose
    assert "GRADIO_SERVER_NAME=0.0.0.0" in compose
