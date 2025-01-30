// File: UserController.java
package com.example.jte;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping("/users")
    public String index(Model model) {
        model.addAttribute("users", userService.getAllUsers());
        return "users";
    }

    @PostMapping("/users/q")
    public String search(@RequestParam(name = "q", required = false) String query, Model model) {
        List<User> selectedUsers = userService.searchUsers(query);
        model.addAttribute("users", selectedUsers);
        return "results";
    }
}