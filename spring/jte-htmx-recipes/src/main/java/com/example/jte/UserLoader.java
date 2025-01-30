package com.example.jte;

import org.yaml.snakeyaml.LoaderOptions;
import org.yaml.snakeyaml.Yaml;
import org.yaml.snakeyaml.constructor.Constructor;

import java.io.InputStream;
import java.util.Comparator;
import java.util.List;
import java.util.Map;

public class UserLoader {
    public static List<Map<String, String>> loadUsers(String fileName) {
        // Load the YAML file into the UserData structure
        Yaml yaml = new Yaml(new Constructor(UserData.class, new LoaderOptions()));
        InputStream inputStream = UserLoader.class.getClassLoader().getResourceAsStream(fileName);
        UserData userData = yaml.load(inputStream);

        // Transform and sort the data
        return userData.results().stream()
                .map(user -> Map.of(
                        "name", user.name().first() + " " + user.name().last(),
                        "email", user.email(),
                        "avatar", user.picture().large()
                ))
                .sorted(Comparator.comparing(user -> user.get("name")))
                .toList();
    }
}