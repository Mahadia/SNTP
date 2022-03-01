<!DOCTYPE html>
<html>

<head>
    <link href="css/getting-started.module.css" rel="stylesheet" />
</head>

<body>
    <div>
       
            <div class="getting-started-container">
                <span class="getting-started-text">Add REVIEW</span>
                <input type="text" placeholder="write your review" class="getting-started-textinput input" />
                <button class="getting-started-button button" onclick="myFunction()">ADD</button>
                <img src="img//logo.png" alt="logo" class="getting-started-logo">
        <div class="getting-started-container-orange">
            <div class="getting-started-container1">
                <form action="admin.php">
                    <button class="getting-started-button1 button" >Add reviews</button>
                    <button class="getting-started-button2 button" type="submit" href="admin.php">Admin</button>
                </form>
            </div>
            <img src="img/Capture reviews.PNG" alt="image" class="getting-started-image" />
                   
        </div>
    </div>
    </div>
    <p id="demo"></p>

    <script>
         function myFunction() {
             if(getting-started-textinput=="non"){ 
            document.getElementById("demo").innerHTML = "Hello World";
}}
    </script>

</body>

</html>