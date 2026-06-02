package com.example.vaadin;

import org.springframework.data.annotation.Id;

public record Post(@Id Integer postId, String title, String body) {
}
