# CT-477 Complex Computing Activity: Secure Software Design

This repository demonstrates the principles of secure software design and development by providing a Python Flask web application with intentionally placed security vulnerabilities, alongside a secure, fixed version of the same application. 

This project fulfills the requirements for the CT-477 Secure Software Design & Development Complex Computing Activity.

## Project Structure

* `app_vulnerable.py`: The vulnerable version of the application containing 3 distinct security flaws.
* `app_fixed.py`: The secured version of the application where all vulnerabilities have been mitigated.
* `test_security.py`: An automated test suite using `pytest` that demonstrates the exploits succeeding on the vulnerable app and failing on the secure app.

## Implemented Vulnerabilities

1. **SQL Injection (SQLi):** Located in the `/login` endpoint. The vulnerable app uses unsafe string concatenation, allowing authentication bypass. The fixed app uses parameterized queries.
2. **Cross-Site Scripting (XSS):** Located in the `/greet` endpoint. The vulnerable app reflects user input directly into the HTML response. The fixed app sanitizes and escapes the output using `markupsafe`.
3. **Command Injection:** Located in the `/ping` endpoint. The vulnerable app executes an OS command directly with user input. The fixed app uses `shlex` escaping and avoids direct shell execution.

## Prerequisites

Before running the servers or tests, ensure you have Python 3 installed along with the required libraries:

```bash
pip install Flask pytest