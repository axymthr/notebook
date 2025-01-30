package com.example.jte.autocomplete;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.Arrays;
import java.util.List;

@Controller
public class SearchController {
    @GetMapping("/user-search")
    public String search() {
        return "autocomplete/search";
    }

    @GetMapping("/search-users")
    public String users(@RequestParam(value = "query", required = false) String query, Model model) {
        if (query == null || query.isEmpty()) {
            // Do not add anything to the model and return the view
            return "autocomplete/users";
        }

        List<String> users = Arrays.asList("Alice", "Bob", "Charlie", "Diana", "Edward");

        // Filter users if query is not null or empty
        users = users.stream()
                .filter(name -> name.toLowerCase().contains(query.toLowerCase()))
                .toList();
        // Add the filtered list to the model
        model.addAttribute("users", users);

        return "autocomplete/users";
    }
}
