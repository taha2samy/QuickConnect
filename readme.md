<div style="display: flex; justify-content: center; align-items: center; height: 100vh; text-align: center;">
    <h1 style="margin: 0;">
        Quick Connect 
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512" width="70" height="50" style="vertical-align: middle;">
            <!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.-->
            <path fill="#003366" d="M208 352c114.9 0 208-78.8 208-176S322.9 0 208 0S0 78.8 0 176c0 38.6 14.7 74.3 39.6 103.4c-3.5 9.4-8.7 17.7-14.2 24.7c-4.8 6.2-9.7 11-13.3 14.3c-1.8 1.6-3.3 2.9-4.3 3.7c-.5 .4-.9 .7-1.1 .8l-.2 .2s0 0 0 0s0 0 0 0C1 327.2-1.4 334.4 .8 340.9S9.1 352 16 352c21.8 0 43.8-5.6 62.1-12.5c9.2-3.5 17.8-7.4 25.2-11.4C134.1 343.3 169.8 352 208 352zM448 176c0 112.3-99.1 196.9-216.5 207C255.8 457.4 336.4 512 432 512c38.2 0 73.9-8.7 104.7-23.9c7.5 4 16 7.9 25.2 11.4c18.3 6.9 40.3 12.5 62.1 12.5c6.9 0 13.1-4.5 15.2-11.1c2.1-6.6-.2-13.8-5.8-17.9c0 0 0 0 0 0s0 0 0 0l-.2-.2c-.2-.2-.6-.4-1.1-.8c-1-.8-2.5-2-4.3-3.7c-3.6-3.3-8.5-8.1-13.3-14.3c-5.5-7-10.7-15.4-14.2-24.7c24.9-29 39.6-64.7 39.6-103.4c0-92.8-84.9-168.9-192.6-175.5c.4 5.1 .6 10.3 .6 15.5z"/>
        </svg>
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