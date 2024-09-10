# Instructions
## Workflow

We would query a REST API which would give us the Sprints data. Refer to the SprintsDump.json

- From SprintsDump –
    - We would have to list down all the available sprints in a dropdown with the current ongoing sprint selected.
    - To select the ongoing sprint refer to the startDate & finishDate from the SprintsDump.

- From Sprint86Dump –
    - Suppose the ongoing sprint is Sprint86, so you would have to get the respective url from the tag “url” and navigate to it.
    - In Sprint86Dump, you will multiple workitems listed.
    - Each workitem has an ID.
    - Some workitem are parent workitem. For ex "id": 2539400. You can find this out by looking for "rel": null, "source": null and also you will find "id": 2539400 linked to other child tasks like 3582541, 3582868 etc.
    - You need to get the url for the parent task by looking at the “url” tag and navigating to the listed url.

- From ParentTask1Sprint86Dump –
    - This would list all the details about the parent task "id": 2539400.
    - Display System.Title, System.State, AssignedTo(displayName), Custom.TargetVersion
