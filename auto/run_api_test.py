import requests
import time
import os
import sys
import xml.etree.ElementTree as ET
import logging

# Configure debug logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Get token from environment
api_token = os.getenv("APICredentials")
if not api_token:
    logging.error("❌ APICredentials environment variable is not set.")
    sys.exit(1)

# Prepend "Bearer " if needed
AUTH_TOKEN = api_token if api_token.lower().startswith("bearer ") else f"Bearer {api_token}"

# Configurable values
RUNSCOPE_TRIGGER_URL = "https://api.runscope.com/radar/b06d52bf-15b0-472d-a9a5-cb9fe8d630f2/trigger?runscope_environment=a1adcdc6-5a43-413a-b8ec-f4e90f0e2a01"
RESULT_DIR = "test-results"
RESULT_FILE = os.path.join(RESULT_DIR, "runscope-result.xml")

HEADERS = {
    "Authorization": AUTH_TOKEN,
    "Content-Type": "application/json"
}


def trigger_test():
    logging.info("🔄 Triggering API Monitoring test...")
    try:
        response = requests.post(RUNSCOPE_TRIGGER_URL, headers=HEADERS)
        logging.debug(f"Response Code: {response.status_code}")
        logging.debug(f"Response Body: {response.text}")
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"❌ Request failed: {e}")
        sys.exit(1)

    data = response.json()

    try:
        run_info = data["data"]["runs"][0]
        api_test_run_url = run_info["api_test_run_url"]
        test_name = run_info["test_name"]
        test_id = run_info["test_id"]
        test_run_url = run_info["test_run_url"]
    except (KeyError, IndexError) as e:
        logging.error("❌ Failed to parse test run info from response.")
        logging.debug(data)
        sys.exit(1)

    if not api_test_run_url:
        logging.error("❌ No test run URL returned, cannot proceed.")
        sys.exit(1)

    logging.info(f"✅ Test triggered: {test_name} ({test_id})")
    logging.info(f"🔁 Polling test run at: {api_test_run_url}")
    return api_test_run_url, test_name, test_run_url


def poll_until_complete(api_test_run_url):
    status = "working"
    attempts = 0
    max_attempts = 60  # ~5 minutes

    while status in ("init", "working"):
        if attempts >= max_attempts:
            logging.error("⏱️ Timed out waiting for test to complete.")
            sys.exit(1)

        time.sleep(5)
        try:
            resp = requests.get(api_test_run_url, headers=HEADERS)
            logging.debug(f"Polling Response: {resp.text}")
            resp.raise_for_status()
            data = resp.json()
            status = data.get("data", {}).get("result", "unknown")
        except requests.RequestException as e:
            logging.error(f"❌ Error while polling: {e}")
            sys.exit(1)

        logging.info(f"⏳ Current status: {status}")
        attempts += 1

    return data


def generate_junit_xml(test_name, final_result, test_run_url, duration_seconds):
    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)

    testsuite = ET.Element(
        "testsuite",
        name="Runscope Test Suite",
        tests="1",
        failures="0" if final_result == "pass" else "1",
        errors="0",
        skipped="0",
        time=f"{duration_seconds:.3f}"
    )

    testcase = ET.SubElement(
        testsuite,
        "testcase",
        classname="Runscope",
        name=f"{test_name}",
        time=f"{duration_seconds:.3f}"
    )

    if final_result != "pass":
        ET.SubElement(testcase, "failure", message=f"API Monitoring test result: {final_result}")

    ET.SubElement(testcase, "system-out").text = f"Test Report URL: {test_run_url}"

    tree = ET.ElementTree(testsuite)
    tree.write(RESULT_FILE, encoding="utf-8", xml_declaration=True)
    logging.info(f"📄 JUnit result saved to {RESULT_FILE}")


def main():
    start_time = time.time()

    api_test_run_url, test_name, test_run_url = trigger_test()
    status_response = poll_until_complete(api_test_run_url)

    duration = time.time() - start_time
    final_result = status_response.get("data", {}).get("result", "unknown")

    logging.info(f"✅ Final result: {final_result}")
    logging.info(f"🕒 Duration: {duration:.2f} seconds")

    generate_junit_xml(test_name, final_result, test_run_url, duration)


if __name__ == "__main__":
    main()