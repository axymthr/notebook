@import java.util.List
@import com.example.jte.Person

@param int count

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>People directory</title>
    <script src="https://unpkg.com/htmx.org@1.9.5" integrity="sha384-xcuj3WpfgjlKF+FXhSQFQ0ZNr39ln+hwjN3npfM9VBnUskLolQAcN80McRIVOPuO" crossorigin="anonymous"></script>
</head>
<body id="container">

<h3>
    <span class="htmx-indicator">
      ...
   </span>
</h3>

<form>

    <input class="form-control" type="search"
           name="search" placeholder="Begin Typing To Search Users..."
           hx-get="/search/results"
           hx-trigger="keyup changed, search"
           hx-target="#search-results"
           hx-indicator=".htmx-indicator">
</form>

<div id="search-results">
    @template.search_results(people = List.<Person>of(), count = count)
</div>
<style>
    #container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    h3 {
        font-size: 24px;
        margin-bottom: 20px;
    }
    .htmx-indicator {
        display: inline-block;
        margin-left: 10px;
    }
    form {
        position: relative;
    }
    .form-control {
        width: 100%;
        padding: 10px;
        font-size: 18px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    #search-results {
        margin-top: 20px;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    .highlight {
        background-color: #46ffb3;
    }
</style>
</body>
</html>