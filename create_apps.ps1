$python = '.venv/Scripts/python.exe'

& $python manage.py startapp core
& $python manage.py startapp products
& $python manage.py startapp bookings
& $python manage.py startapp payments
& $python manage.py startapp contracts
& $python manage.py startapp inventory
& $python manage.py startapp reservations
& $python manage.py startapp accounts
& $python manage.py startapp dashboard
& $python manage.py startapp contacts

Write-Host "All apps created successfully!"
