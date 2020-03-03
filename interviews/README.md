# Interviews
Interviews fall into 2 categories, coding and verbal.

## Coding
I've grouped coding examples into directories, grouped by difficulty (closely tied to time required to solve them).
- Easy problems can be solved in 30-60 mins, including all edge case + bonus questions.
- Hard problems usually take several days and are designed to be take-home.

## Verbal
Verbal interviews can be done over the phone or in person, possibly with assistance of online pair-programming tools.
My guide to verbal interviews can be found [here](https://github.com/atsepkov/puzzles/blob/master/interviews/guide.md).

Verbal interviews often introduce constraints favoring one type of programmer over another. It's important to understand
these constraints to avoid screening for a wrong candidate. As a candidate it's also important to understand these constraints.

### Common Gotchas

**Generalist vs Specialist:**
Generalists tend to do poorly on verbal coding interviews, and well on verbal design (brainstorming) interviews. They are often
able to solve the problem, but not within the time constraint that a specialist of a given field expects. An interviewee who
spent several years coding in one language using one framework will be able to ace the coding problem using that framework. An
interviewee with a larger breadth of knowledge will likely need more time to understand the context (those extra 5 mins can be
very significant). It's really no different from the concept of `breadth-first` vs `depth-first`, each has its benefits. You 
may want a programmer who is able to hit the ground running in a specialized field or one who has enough breadth to help out
multiple teams.

Be careful with junior interviewers, they may not be aware of above concept, expecting everyone to be a specialist. It's no
different than your 9-year old child doing long-division in his head faster than you can check his work on a calculator.

**Favoring One Language over Another:**
A good programmer is able to pick up new language in a matter of days, but getting proficient with it often requires months.
Basic concepts like loops and conditionals are often very similar between languages, design patterns are not. A best practice
in one language may be an anti-pattern in another. Many interviews today give programmers certain flexibility with language
choice, but it's not uncommon for a problem to favor dynamically-typed languages. This is typically not a problem for
experienced interviewee.

**Favoring Individuals Who Researched Specific Problem:**
Common interview questions revolve around data structures, graph theory, and trees. Most of your everyday work does not.
Most interviewees will need at least some preparation, as we tend to get rusty on these concepts with time if not dealing
with them in our day-to-day work. If your interview needs a couple hours of prep beforehand, that's expected. If your
interview needs a week of prep in specific subset of problems you give (common with Amazon interviews), you should
probably ask yourself if you're favoring a candidate who has free time over one who does not.

Also keep in mind that the only reason Google/Amazon interviews work is because of the fan club these companies built
around themselves. Each of these companies gives you a problem whose edge cases you're unlikely to address within the time
limit without preparaing beforehand. Preparation often involves researching specific types of problems this company likes
to give, not general programming concepts. This technically isn't testing programmer's proficiency, but how much the given
programmer is willing to "specialize" for your given use case, and their ability to pick up these concepts.
