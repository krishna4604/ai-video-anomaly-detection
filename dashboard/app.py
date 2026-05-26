from flask import Flask, render_template_string
import webbrowser

app=Flask(__name__)

HTML="""
<!DOCTYPE html>
<html>

<head>

<title>AI Surveillance</title>

<style>

body{
background:#0f172a;
font-family:Arial;
color:white;
margin:0;
padding:0;
}

.header{
padding:20px;
font-size:28px;
text-align:center;
background:#111827;
}

.container{
display:flex;
justify-content:center;
margin-top:30px;
}

.video{

width:900px;
border-radius:20px;
border:3px solid #00ffcc;

}

</style>

</head>

<body>

<div class='header'>
AI SURVEILLANCE DASHBOARD
</div>

<div class='container'>

<img class='video'
src='http://127.0.0.1:5001/video'>

</div>

</body>

</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


if __name__=="__main__":
    webbrowser.open(
        "http://127.0.0.1:3000"
    )

    app.run(port=3000)