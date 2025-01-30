package com.example.jte;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
   class UsersConfigTest {

       @Autowired
       private UsersConfig usersConfig;

       @Test
       void testUsersConfigurationBinding() {
           assertNotNull(usersConfig);
           assertFalse(usersConfig.getResults().isEmpty());
           
           User firstUser = usersConfig.getResults().getFirst();
           assertEquals("John Doe", firstUser.name());
           assertEquals("john.doe@example.com", firstUser.email());
           assertEquals("john.png", firstUser.picture().large());
       }
   }