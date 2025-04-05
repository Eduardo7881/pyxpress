# PyXpress
A basic HTTP server module using raw Python sockets.

## Contributions
Contributions are very welcome!  
If you like this project, consider helping fix bugs and opening a pull request.

## Known Bugs
- **HTML redirect not supported**  
  For some reason, redirecting to `.html` or files causes this error:
  ```py
  Server listening in: http://localhost:3000/
  Error: slice indices must be integers or None or have an __index__ method
  ```

- **Static function doesn't work**  
  Seriously, I don’t know why the following doesn’t work:
  ```py
  app.static("/", "./public")
  ```

## TODO
- HTML support  
- XML support  
- Image support  
- More MIME types...
- and more!

## License
This project is licensed under the **MIT License**.  
Feel free to explore, modify, and send pull requests!
