<div style="display: flex; justify-content: center; align-items: center; height: 100vh; text-align: center;">
    <h1 style="margin: 0;">
        Quick Connect 
        ![alt text](logo.svg)
    </h1>
</div>



**Quick Connect** is an application that allows you to create chat rooms instantly from anywhere and connect with anyone. It's simple, fast, and designed to give users a quick and seamless communication experience.

## Features

- **Instant Chat Rooms**: Create a chat room on the fly with a unique timestamp-based identifier.
- **Seamless Connections**: Join or invite others to chat rooms from any device.
- **Lightweight and Fast**: Optimized for fast performance and instant messaging.
- **No Signups Needed**: No need for users to sign up; start chatting right away.

## Installation

To install the dependencies and run the project, follow the steps below:

### Using `pyenv` and `pipenv`:

1. Install [pyenv](https://github.com/pyenv/pyenv) to manage Python versions:
   ```bash
   pyenv install 3.10.10
   pyenv local 3.10.10
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/taha2samy/QuickConnect.git
   cd quick-connect
   ```

3. Install [pipenv](https://pipenv.pypa.io/en/latest/) to manage the environment and packages:
   ```bash
   pipenv install
   ```

4. Activate the virtual environment:
   ```bash
   pipenv shell
   ```
5. Build the project Database:
   ```bash
   pipenv run python manage.py migrate
   ``` 
6. Run the application:
   ```bash
   pipenv run python manage.py runserver
   ```

## Usage

1. Open the application.
2. Create a chat room by pressing the **Create Chat Room** button.
3. Share the unique chat room identifier with the person you want to connect with.
4. Start chatting instantly.

## Project Structure

```plaintext
|   .gitignore
|   .python-version
|   db.sqlite3
|   manage.py
|   Pipfile
|   Pipfile.lock
|   readme.md
|
+---QuickConnect
|       asgi.py
|       settings.py
|       urls.py
|       wsgi.py
|       __init__.py
|
\---rooms
    |   admin.py
    |   apps.py
    |   consumers.py
    |   models.py
    |   routing.py
    |   tests.py
    |   views.py
    |   __init__.py
    |
    +---migrations
    |       __init__.py
    |
    \---templates
            Home.html
            room.html
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Quick Connect** – Instant connections, anywhere, anytime.
```

Feel free to modify the structure or the content based on your specific project details.