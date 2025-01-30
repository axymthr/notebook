@import java.util.List
@import com.example.jte.Person

@param List<Person> people
@param int count

Matches ${people.size()} / ${count} people in the directory.
@for(Person person : people)
    <p>$unsafe{person.name()}</p>
    <p>${person.description()}</p>
@endfor