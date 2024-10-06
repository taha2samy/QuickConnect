# ![alt text](logo.svg) Quick Connect



**Quick Connect** is an application that allows you to create chat rooms instantly from anywhere and connect with anyone. It's simple, fast, and designed to give users a quick and seamless communication experience.

## Features

- **Instant Chat Rooms**: Create a chat room on the fly with a unique timestamp-based identifier.
- **Seamless Connections**: Join or invite others to chat rooms from any device.
- **Lightweight and Fast**: Optimized for fast performance and instant messaging.
- **No Signups Needed**: No need for users to sign up; start chatting right away.

## Installation

To install the dependencies and run the project, follow the steps below:

### Using `pyenv` and `pipenv`:

To convert the setup instructions to use `virtualenv` instead of `pipenv`, follow these steps:

---

1. **Clone the repository:**
   ```bash
   git clone https://github.com/taha2samy/QuickConnect.git
   cd quick-connect
   ```

2 **Install [virtualenv](https://virtualenv.pypa.io/en/latest/) to manage the environment:**
   ```bash
   pip install virtualenv
   ```

3. **Create and activate the virtual environment:**
   ```bash
   virtualenv venv
   source venv/bin/activate  # On macOS/Linux
   # OR
   venv\Scripts\activate  # On Windows
   ```

4. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Build the project database:**
   ```bash
   python manage.py migrate
   ```

6. **Run the application:**
   ```bash
   python manage.py runserver
   ```
7. **Copy the Unit Files**: Use the `cp` command to copy the service and timer files to the systemd directory:
   ```bash
   sudo cp unit_files/cleanup.service /etc/systemd/system/
   sudo cp unit_files/cleanup.timer /etc/systemd/system/
   ```

8. **Reload Systemd Daemon**: After copying the files, reload the systemd daemon to recognize the new unit files:
   ```bash
   sudo systemctl daemon-reload
   ```

9. **Enable the Timer**: Enable the timer so that it starts automatically on boot:
   ```bash
   sudo systemctl enable cleanup.timer
   ```

10. **Start the Timer**: Start the timer immediately:
   ```bash
   sudo systemctl start cleanup.timer
   ```

## Checking the Status

To verify that the timer is running, use the following command:
```bash
sudo systemctl status cleanup.timer
```


---

This conversion replaces `pipenv` with `virtualenv` for managing the environment, using a `venv` folder and the `requirements.txt` file for package installation.

## Usage

1. Open the application.
2. Create a chat room by pressing the **Create Chat Room** button.
3. Share the unique chat room identifier with the person you want to connect with.
4. Start chatting instantly.

## Project Structure

```plaintext
│   .gitignore
│   .python-version
│   db.sqlite3
│   LICENSE
│   logo.svg
│   manage.py
│   Pipfile
│   Pipfile.lock
│   readme.md
│
├───accounts
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───migrations
│   │       __init__.py
│   │
│   ├───static
│   │   ├───css
│   │   │       all.min.css
│   │   │       bootstrap.min.css
│   │   │
│   │   ├───javascript
│   │   │       bootstrap-stackpath.min.js
│   │   │       bootstrap.min.js
│   │   │       jquery.min.js
│   │   │       popper-core.min.js
│   │   │       popper.min.js
│   │   │       qrious.min.js
│   │   │
│   │   └───webfonts
│   │           fa-solid-900.ttf
│   │           fa-solid-900.woff
│   │           fa-solid-900.woff2
│   │
│   └───templates
│           login.html
│           signup.html
│
├───media
│   └───temp
├───QuickConnect
│       asgi.py
│       settings.py
│       urls.py
│       wsgi.py
│       __init__.py
│
└───rooms
    │   admin.py
    │   apps.py
    │   consumers.py
    │   models.py
    │   routing.py
    │   tests.py
    │   views.py
    │   __init__.py
    │
    ├───migrations
    │       __init__.py
    │
    └───templates
            base.html
            Home.html
            room.html


```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Quick Connect** – Instant connections, anywhere, anytime.

Feel free to modify the structure or the content based on your specific project details.
