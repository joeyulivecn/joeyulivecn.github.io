### Debug Flask in visual stuido code

#### Environment
* OS: Windows 10
* Python Version: 3.6.2
* VS Code Version: 1.18.1
* App Path: c:\flask_app

#### Folder Structure
```markdown
C:\FLASK_APP
│  flask.code-workspace
│  run.py
│
├─.vscode
│      launch.json
│      settings.json
│
├─app
│  │  views.py
│  │  __init__.py
│  │
│  ├─static
│  ├─templates
│
├─tmp
└─venv
```

#### Create python virtual environment
> cd c:\flask_app

> python -m venv venv

#### Install Flask
> pip install Flask


#### Create a simple Flask app
views.py
```markdown python
from app import app

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World!'
```

__init__.py
```markdown python
from flask import Flask

app = Flask(__name__)
from app import views
```

run.py
```markdown python
#!venv/bin/python
from app import app
app.run(debug=False)
```
* Make sure the debug=False not True

#### Workspace Settings 
> Select File > Preferences > Settings


.vscode\settings.json
```markdown json
{
    "python.pythonPath": "${workspaceRoot}\\venv\\Scripts\\python.exe"
}
```

#### launch.json
> 
Create launch.json under .vscode folder
```markdown json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask",
            "type": "python",
            "request": "launch",
            "stopOnEntry": false,
            "pythonPath": "${config:python.pythonPath}",
            "program": "${workspaceRoot}/run.py",
            "env": {
                "FLASK_APP": "${workspaceRoot}/app.py"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "debugOptions": [
                "WaitOnAbnormalExit",
                "WaitOnNormalExit",
                "RedirectOutput"
            ]
        }
    ]
}
```

##### Now set some breakpoints and start debugging!

