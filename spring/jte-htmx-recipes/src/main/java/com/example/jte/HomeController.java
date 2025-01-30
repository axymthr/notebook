package com.example.jte;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
public class HomeController {

    @GetMapping
    public String home(Model model) {
        var page = new Page("Hello, Java Template Engine", "This is my first home page!");
        var items = List.of("Item 1","Item 2","Item 3");
        model.addAttribute("name", "Aksh");
        model.addAttribute("page", page);
        model.addAttribute("items", items );
        return "index";
    }
}
