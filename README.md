# cybersecurity-proj1

This project has been created for the Cybersecurity MOOC Project I. The webpage will be similar to one exercise done during the Securing Software course where we had a webpage with quizzes and topics.

This project has intended security flaws but the fixes will be provided.

## Security flaws

The security flaws that this project has are chosen from the OWASP 2021 Top 10 List, except for Cross-Site Request Forgery (CSRF) which is not included in the list but is a fundamental flaw in web applications.

### SQL Injection

`A03:2021-Injection` - SQL Injection is a vulnerability that allows an attacker to execute SQL code in the server. This can be fixed by using parameterized queries.

### Broken Access Control

`A01:2021-Broken Access Control` - Broken Access Control is a vulnerability that allows an attacker to access resources that they should not have access to. This can be fixed by implementing proper access control.

### Cryptographic Failures

`A02:2021-Cryptographic Failures` - Cryptographic Failures occurs when either cryptography is used incorrectly or the cryptography is not used at all. This can be fixed by using cryptography correctly.

### Server-Side Request Forgery

`A10:2021-Server-Side Request Forgery` - Server-Side Request Forgery is a vulnerability that allows an attacker to make requests from the server. This can be fixed by validating the requests.

### Cross-Site Request Forgery

`Cross-Site Request Forgery` - Cross-Site Request Forgery is a vulnerability that allows an attacker to make requests like if he was the user. This can be fixed by using CSRF tokens.

## Installation

1. Ensure you have Python and Django installed.

2. Clone this repository:

   ```bash
   git clone https://github.com/LittleHaku/cybersecurity-proj1
    ```

3. Enter the project directory:

   ```bash
   cd cybersecurity-proj1
   ```

4. Run the server:

   ```bash
   python manage.py runserver
   ```
