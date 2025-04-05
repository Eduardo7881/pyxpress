# PyXpress
A Basic HTTP-SERVER Module using Socket on Python Language.

# Contribuitons
Contribuitons are very welcome! 

If you'd like this project, consider doing a contribution on fixing bugs and make a pull request.

# Known Bugs:
- HTML Non-Supported Redirecting. For some reason, i don't know why redirecting to HTML files lead to this error:
```py
Server listening in: http://localhost:3000/
Error: slice indices must be integers or None or have an __index__ method
```
- Static function. Seriously, i don't know why the
```py
app.static("/", "./public")
```
DOES NOT WORK!!

# License
This project is licensed under MIT License. Feel free to explore it and make pull requests!
