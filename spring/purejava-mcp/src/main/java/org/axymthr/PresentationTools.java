package org.axymthr;

import java.util.ArrayList;
import java.util.List;

public class PresentationTools {
    private final List<Presentation> presentations =  new ArrayList<>();

    public PresentationTools() {
                var keynote = new Presentation("Keynote Talk", "Main Hall", 60);
                var workshop = new Presentation("Workshop", "Room A", 90);
                var lightning = new Presentation("Lightning Round", "Room B", 15);
                this.presentations.addAll(List.of(keynote, workshop, lightning));
    }

    public List<Presentation> getPresentations() {
        return presentations;
    }

    public List<Presentation> getPresentationsByYear(int year) {
        return presentations.stream().filter(p -> p.year() == year).toList();
    }


}
