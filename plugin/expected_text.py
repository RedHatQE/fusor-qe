import pytest
import json

@pytest.fixture
def expected_text(request):
    text_file = request.config.getoption("--qci-expected-text")
    with open(text_file) as text:
        data = json.load(text)
    return data
