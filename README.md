# cybersecurity-proj1

This project has been created for the Cybersecurity MOOC Project I. The webpage will be similar to one exercise done during the Securing Software course where we had a webpage with quizzes and topics.

This project has intended security flaws but the fixes will be provided.

## Security flaws

The security flaws that this project has are chosen from the OWASP 2021 Top 10 List, except for Cross-Site Request Forgery (CSRF) which is not included in the list but is a fundamental flaw in web applications.

### SQL Injection

`A03:2021-Injection` - SQL Injection is a vulnerability that allows an attacker to execute SQL code in the server. This can be fixed by using parameterized queries.

I have made this flaw by hardcoding a SQL query in the code in the Quiz Edit, since with Django the default is sqlite and it doesn't allow to execute multiple queries at once it is not possible to drop the database, but for example it is possible to type `ivan' WHERE id = 1 or 1=1 --` and now all the quizzes will have the name ivan.

This can be fixed by using parameterized queries as the code commented below the query is.

### Broken Access Control

`A01:2021-Broken Access Control` - Broken Access Control is a vulnerability that allows an attacker to access resources that they should not have access to. This can be fixed by implementing proper access control.

To make recreate this flaw I have removed the `@login_required` decorator from the QuizDeleteView and also removed the owner check, this allows anyone to delete any quiz by going to the url `/quiz/<id>/delete`. For the sake of testing this I added to the main quiz list the IDs and the owner of the quiz, in a real scenario this would not be the case.

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
   cd cybersecurity-proj1/project
   ```

4. Populate the database

   ```bash
   make populate
   ```

   If this fails, reset the database and try again.

   ```bash
   make resetdb
   ```

5. Run the server:

   ```bash
   make run
   ```

6. Optional: Create a superuser:

   ```bash
   make superuser
   ```

### Other commands

Reset the database:

```bash
make resetdb
```

Create a superuser:

```bash
make superuser
```

Delete all migrations:

```bash
make delete_migrations
```

Migrate:

```bash
make migrate
```

Drop the database:

```bash
make dropdb
```

## Funcionalities

This website allows the users to register and login, when a user is logged in he can access his quizzes by going to the Edit Quizzes tab, there he can create new ones, modify the existing ones or delete them, right now empty quizzes and empty questions are allowed, the purpose is to learn about cybersecurity so I'd rather focus on the security flaws than the functionality of the website.

As with the example seen in the course one could fail a question, go back and change the answer, I fixed it but I didn't consider it a flaw of the OWASP Top 10 List since it is not a security flaw, but more a design one.

The users can see all the quizzes from the home/main page, there they can click on one and play it.
