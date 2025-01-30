<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto-complete user search</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <script src="https://unpkg.com/htmx.org@1.6.1"></script>
    <!-- Add your custom CSS here -->
    <style>
        .highlight {
            background-color: #f3f4f6; /* Light-gray background to indicate selection */
            font-weight: bold;        /* Bold text for better visibility of selection */
        }
    </style>

</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center">
<div id="form-container" class="bg-white p-8 rounded-lg shadow-md w-full max-w-3xl">
    <div class="mb-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-700 border-b pb-2">User Search</h2>

        <form hx-post="/register" hx-target="#form-container" hx-swap="innerHTML" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-4">
                <div class="relative">
                    <input type="text"
                           id="userSearch"
                           name="query"
                           placeholder="Search"
                           hx-get="/search-users"
                           hx-trigger="keyup changed delay:300ms"
                           hx-target="#userSuggestions"
                           hx-swap="outerHTML"
                           class="w-full px-3 py-2 pl-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                           hx-include="#userSearch">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <i class="fas fa-search text-gray-400"></i>
                    </div>

                    <div id="userSuggestions"
                         class="absolute bg-white shadow-md w-full mt-1 rounded-md z-10"
                         hx-on="mouseleave: this.style.display='none';"
                         class="hover:bg-gray-100">
                        <!-- Dynamically generated suggestions -->
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>

<script>
    document.addEventListener("htmx:configRequest", (event) => {
    const triggeringEvent = event.detail.elt?.getAttribute("hx-trigger");
    const keyEvent = event.detail.triggeringEvent;

    // Prevent HTMX from sending the request if Enter key is pressed
    if (keyEvent?.type === "keyup" && keyEvent.key === "Enter") {
        event.preventDefault(); // Stop HTMX from triggering the request
    }
});
    document.body.addEventListener("htmx:beforeRequest", (event) => {
        const input = document.getElementById("userSearch");
        const suggestionBox = document.getElementById("userSuggestions");

        // Prevent requests if the input is empty and hide the dropdown
        if (input.value.trim() === "") {
            event.preventDefault(); // Stop the request
            if (suggestionBox) suggestionBox.style.display = "none"; // Hide dropdown
        }
    });

    document.body.addEventListener("htmx:afterSwap", (event) => {
        const targetId = event.target.getAttribute("id");
        if (targetId === "userSuggestions") {
            const suggestionBox = document.getElementById("userSuggestions");
            const suggestions = suggestionBox.querySelectorAll("li");

            // Reattach event listeners for dynamically generated suggestions
            suggestions.forEach((item) => {
                item.addEventListener("click", () => {
                    const searchBox = document.getElementById("userSearch");
                    searchBox.value = item.textContent.trim(); // Update input with selection

                    suggestionBox.innerHTML = ""; // Clear suggestions
                    suggestionBox.style.display = "none"; // Hide dropdown
                });
            });

            // Manage dropdown visibility based on the presence of suggestions
            if (suggestions.length === 0) {
                suggestionBox.style.display = "none"; // Hide if no suggestions exist
            } else {
                suggestionBox.style.display = "block"; // Show if suggestions exist
            }
        }
    });

    document.body.addEventListener("htmx:beforeSwap", (event) => {
        const targetId = event.target.getAttribute("id");
        if (targetId === "userSuggestions") {
            const triggeringEvent = event.detail.requestConfig.triggeringEvent;

            // Immediately hide the dropdown on a click event
            if (triggeringEvent && triggeringEvent.type === "click") {
                const suggestionBox = document.getElementById("userSuggestions");
                suggestionBox.style.display = "none";
            }
        }
    });

    const searchBox = document.getElementById("userSearch");
    searchBox.addEventListener("keydown", (event) => {
        const suggestionBox = document.getElementById("userSuggestions");
        if (!suggestionBox || suggestionBox.children.length === 0) return; // Exit if no suggestions

        const suggestions = suggestionBox.querySelectorAll("li");
        let current = suggestionBox.querySelector(".highlight");

        switch (event.key) {
            case "ArrowDown":
                event.preventDefault();
                if (!current) {
                    suggestions[0].classList.add("highlight");
                } else {
                    current.classList.remove("highlight");
                    (current.nextElementSibling || suggestions[0]).classList.add("highlight");
                }
                break;

            case "ArrowUp":
                event.preventDefault();
                if (!current) {
                    suggestions[suggestions.length - 1].classList.add("highlight");
                } else {
                    current.classList.remove("highlight");
                    (current.previousElementSibling || suggestions[suggestions.length - 1]).classList.add("highlight");
                }
                break;

            case "Enter":
                event.preventDefault(); // Stop default behavior (form submission, etc.)
                if (current) {
                    searchBox.value = current.textContent.trim(); // Update input with selection
                    suggestionBox.innerHTML = ""; // Clear suggestions
                    suggestionBox.style.display = "none"; // Hide dropdown
                }
                break;

            case "Escape":
                event.preventDefault();
                suggestionBox.innerHTML = ""; // Clear suggestions
                suggestionBox.style.display = "none"; // Hide dropdown
                break;
        }
    });
</script>


</body>
</html>
