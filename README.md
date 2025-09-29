To run the application with Docker, call:
```bash
    docker-compose up --build
```

To run it locally create a virtual environment:
```bash
    python3 -m venv .venv
```
activate it:
```bash
    . .venv/bin/activate
```
install the dependencies:
```bash
    pip install -r ./requirements.txt
```
and, finally, run the application:
```bash
    flask --app app run
```