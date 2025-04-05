from pyxpress import Pyxpress

app = Pyxpress()

# app.static("/", "./public")

@app.get("/")
def home(req, res):
    res.redirect("/index.html")

app.listen(3000)
