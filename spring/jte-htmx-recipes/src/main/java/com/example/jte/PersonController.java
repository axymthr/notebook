package com.example.jte;

import gg.jte.TemplateEngine;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.util.HtmlUtils;

import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

@Controller
public class PersonController {
    @Autowired
    TemplateEngine templateEngine;


    List<Person> allPeople = List.of(new Person("James Smith", "Always has more expressions than an emoji keyboard."),
            new Person("Mary Johnson", "Could turn any conversation into a monologue about coffee beans."),
            new Person("John Williams", "Once sent a text to a microwave by accident."),
            new Person("Patricia Brown", "Turns every situation into a groan-worthy pun fest."),
            new Person("Robert Jones", "Owns more gadgets than Batman's utility belt."),
            new Person("Linda Davis", "Can make a dance party happen in a library."),
            new Person("Michael Miller", "Treats snack bags and dip jars like a science experiment."),
            new Person("Jennifer Garcia", "Conversation is basically a meme showcase."),
            new Person("William Martinez", "Crafting attempts end up looking like modern art."),
            new Person("Elizabeth Robinson", "Joint pains predict the weather better than meteorologists."));

    @GetMapping("/search")
    public String personSearch(Model model) {
        model.addAttribute("count", allPeople.size());
        return "search";
    }

    @GetMapping("/search/results")
    public String personSearchResults(
            @RequestParam(value = "search", required = false, defaultValue = "") String search,
            Model model) {

        List<Person> people;
        if (!search.isEmpty()) {
            people = allPeople.stream()
                    .filter(person -> person.name().toLowerCase().contains(search.toLowerCase()))
                    .map(person -> new Person(highlightMatchedText(person.name(), search), person.description()))
                    .collect(Collectors.toList());
        } else {
            people = Collections.emptyList();
        }

        model.addAttribute("people", people);
        model.addAttribute("count", allPeople.size());
        return "search_results";
    }

    public String highlightMatchedText(String text, String query) {
        if (text == null || query == null || query.isEmpty()) {
            return text;
        }

        String lowerText = text.toLowerCase();
        String lowerQuery = query.toLowerCase();

        int start = lowerText.indexOf(lowerQuery);
        if (start == -1) {
            return HtmlUtils.htmlEscape(text); // Escape HTML to prevent XSS
        }

        int end = start + query.length();
        String highlighted = String.format("<span class=\"highlight\">%s</span>",
                HtmlUtils.htmlEscape(text.substring(start, end)));

        return HtmlUtils.htmlEscape(text.substring(0, start))
                + highlighted
                + HtmlUtils.htmlEscape(text.substring(end));
    }

}
