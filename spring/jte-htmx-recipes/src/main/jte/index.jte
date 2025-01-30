@import com.example.jte.Page
@import java.util.List

@param String name
@param Page page
@param List<String> items

<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>${page.title()}</title>
    <meta name="description" content="${page.description()}"/>
</head>
<body>

<h1>Hello, ${name}!</h1>

<%--This is a comment not rendered--%>

@if(items.isEmpty())
<p>You have no items</p>
@else
<ul>
    @for(String item: items)
        <li>${item}</li>
    @endfor
</ul>
@endif

@if(!items.isEmpty())
    <p>You have ${items.size()} items</p>
@endif

</body>
</html>