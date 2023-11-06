<!DOCTYPE html>
<html lang="de" dir="ltr">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> Registrieren </title> 
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='loginAndRegister.css') }}">
   </head>
<body>
  <div class="wrapper">
    <h2>Registrierung</h2>
    <form action="{{ url_for('registration.register') }}" method="POST">
      <div class="input-box">
        <input type="text" placeholder="Name eingeben" name="reg_username" id="reg_username" required>
      </div>
      <div class="input-box">
        <input type="text" placeholder="E-Mail eingeben" name="reg_email" id="reg_email" required>
      </div>
      <div class="input-box">
        <input type="password" placeholder="Passwort" name="reg_password" id="reg_password" required>
      </div>
      <h1 class="h3 mb-3" style="color:red" id="error" hidden="True">Passwörter stimmen nicht überein!</h1>
      <div class="input-box">
        <input type="password" placeholder="Passwort wiederholen" name="reg_password_repeat" id="reg_password_repeat" required>
      </div>
      
      <div class="policy">
        <input type="checkbox">
        <h3>Ich akzeptiere die Nutzerbedingungen</h3>
      
      </div>
      <div class="input-box button">
        <input type="Submit" value="Registrieren">
      </div>
      <div class="text">
        <h3>Haben Sie bereits einen Account? <a href="{{ url_for('login.login') }}">einloggen</a></h3>
      </div>      
    </form>
  </div>
  <script>
      try{
        var parts = window.location.search.substr(1).split("&");
        var $_GET = {};
        for (var i = 0; i < parts.length; i++) {
          var temp = parts[i].split("=");
          $_GET[decodeURIComponent(temp[0])] = decodeURIComponent(temp[1]);
        }
        var error = $_GET['error'];
        console.log(error);
        console.log(typeof(error)); 
        console.log("test2")
        if (error == "True"){
          console.log("if")
          var error_element = document.getElementById("error");
          error_element.removeAttribute("hidden");
        }
      } catch (err){
        console.log(err);
        console.log("test")
      }
    </script>
</body>
</html>