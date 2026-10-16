TEMPLATE FOR RETROSPECTIVE (Team 13)
=====================================

The retrospective should include _at least_ the following
sections:

- [process measures](#process-measures)
- [quality measures](#quality-measures)
- [general assessment](#assessment)

## PROCESS MEASURES 

### Macro statistics

- Number of stories committed vs done: **2 vs 2**
- Total points committed vs done: **7 vs 7**
- Nr of hours planned vs spent (as a team): **38h vs 47h**


### Detailed statistics

| Story  | # Tasks | Points | Hours est. | Hours actual |
|--------|---------|--------|------------|--------------|
| _#0 technical detail_   |     7    |    -   |     16h       |21h              |
| _#1 Get ticket_   |     7    |    2   |     12h       |15h 25m              |
| _#2 Next customer_   |     5    |    5   |     10h       |10h 35m              |
   

- Hours per task average, standard deviation (estimate and actual), over 19 tasks (stories #0, 1 and 2)

|            | Mean | StDev |
|------------|------|-------|
| Estimation | 2h     |1h 43m       | 
| Actual     |    2h 28m  |2h 10m       |

- Total estimation error ratio: sum of total hours spent / sum of total hours effort - 1

    $$\frac{\sum_i spent_{task_i}}{\sum_i estimation_{task_i}} - 1$$

    <br>47h / 38h - 1 = **0.24**, we spent 24% more than we estimated
    
- Absolute relative task estimation error: sum( abs( spent-task-i / estimation-task-i - 1))/n

    $$\frac{1}{n}\sum_i^n \left| \frac{spent_{task_i}}{estimation_task_i}-1 \right| $$

    <br>**0.36**, on average a single task was off by about 36%

  
## QUALITY MEASURES 

- Unit Testing:
  - Total hours estimated
    <br>4h
  - Total hours spent
    <br>6h
  - Nr of automated unit test cases
    <br>12
  - Coverage
    <br>92% of the backend code, measured with pytest-cov 
- E2E testing:
  - Total hours estimated
    <br>4h
  - Total hours spent
    <br>2h 30m
  - Nr of test cases
    <br>4 E2E tests with Playwright
- Code review 
  - Total hours estimated
    <br>2h
  - Total hours spent
    <br>3h

## ASSESSMENT

- What did go wrong in the sprint?
  - Almost all the integration happened on the review day. Six pull requests were merged in about one hour, and the burndown stayed flat and dropped on the last day.
  - The cards on the board were moved by one person at the end of the sprint, instead of by each member while working on them.
  - At the demo the interface was too minimal, and some data of the backend, such as the services of each counter, was not shown. The feedback we received asked us to separate the customer menu from the other roles, add CSS styling, display the services of each counter, and add QR code generation and a way to print the ticket.

- What caused your errors in estimation (if any)?
  - Our estimates covered only 38h of the 50h budget of the team (5 members for 10h each), so part of the work was never planned as a task.
  - Agreeing on the tech stack and the workflow (OQM-27) took 8h instead of 4h, because the discussions were long in a team with very different experience.
  - The totem UI (OQM-23) took 3h 50m instead of 2h. It was first built on fake data and connected to the real backend only late.
  - The unit tests (OQM-16, OQM-22) took 3h each instead of 2h, because mocking the database session was new for us and the first version had to be fixed.
  - The code reviews took longer than planned because they found real bugs, such as ticket codes that could repeat and Next customer returning the same ticket every time, and the fixes were done inside the review.
  - Integration and E2E tests took less than estimated (2h 30m instead of 4h), because the setup of the first story was reused for the second.

- What lessons did you learn (both positive and negative) in this sprint?
  - Positive: tests at three levels and code review caught real bugs before the demo. The branch rules with one approval worked once everyone followed them. At the review we were honest about what was missing.
  - Negative: frontend and backend met late, and almost everything was merged in the last hours before the demo, with no rehearsal. Some work skipped the agreed process (direct pushes to `main`, branches without a pull request, merges into the wrong branch). Questions and review requests often stayed unanswered for hours, and a decision taken in the chat (call a ticket only if it is still waiting) never reached the code. Quality depended on one person checking and fixing at the end of the sprint. Splitting the work by layer instead of by story made integration late.

- Which improvement goals set in the previous retrospective were you able to achieve? 

  - This was our first sprint, so there were no goals from a previous retrospective.
  
  
- Which ones you were not able to achieve? Why?
  - Not applicable, for the same reason.

- Improvement goals for the next sprint and how to achieve them (technical tasks, team coordination, etc.)
  1. **Integrate early and rehearse the demo.** Every story has a thin working version merged into `dev` by the middle of the sprint, and nothing big is merged in the last 24 hours. Each sprint has a demo owner, a different person each time, who tries the whole product as a user two days before the demo. Mid-sprint integration and the rehearsal are tasks on the board, with an estimate.
  2. **A written working agreement on communication.** A three-line check-in in the chat every working day (what I did, what I will do, what blocks me), and an answer to every question or review request within 24 hours. Stories are owned by mixed pairs, a more experienced and a less experienced member, so that experience spreads. At the next retrospective we check the number of check-ins and how long pull requests waited for a review.

- One thing you are proud of as a Team!!
  Both stories really met the Definition of Done, with all the tests passing at three levels, and the code review stopped real bugs before they reached the demo.
