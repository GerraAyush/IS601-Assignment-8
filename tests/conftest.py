import time
import pytest
import requests
import subprocess
from playwright.sync_api import sync_playwright


@pytest.fixture(scope='session')
def fastapi_server():
    fastapi_process = subprocess.Popen(['python', 'main.py'])
    
    server_url = 'http://127.0.0.1:8000/'
    
    timeout = 30
    start_time = time.time()
    server_up = False
    
    print("Starting FastAPI server...")
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(server_url)
            if response.status_code == 200:
                server_up = True
                print("FastAPI server is up and running.")
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    
    if not server_up:
        fastapi_process.terminate()
        raise RuntimeError("FastAPI server failed to start within timeout period.")
    
    yield
    
    print("Shutting down FastAPI server...")
    fastapi_process.terminate()
    fastapi_process.wait()
    print("FastAPI server has been terminated.")

@pytest.fixture(scope="session")
def playwright_instance_fixture():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance_fixture):
    browser = playwright_instance_fixture.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()
