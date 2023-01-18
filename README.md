# Raftaar
Raftaar is a project to manage vehicle(s), including gas transactions, loan
payments, and maintenance.

# Update site
## Create whl package
```
make whl
```
## Copy whl to Server
```
scp <WHL> <USER>@<HOST>:<PATH>
```
## Active Raftaar venv
## Install whl package
```
pip install <WHL_PATH>
```
## Reload Site
```
sudo systemctl reload apache2
```
## Recreate db
```
flask --app raftaar init-db
```

# Virtual environments
## Create an environment
```
python3 -m venv venv
```
## Activate the environment
```
. venv/bin/activate
```
## Deactivate the environment
```
deactivate
```
