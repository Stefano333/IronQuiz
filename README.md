# IronQuiz

This is one Quiz web application.

# How to play

There are two roles:
* Host: the person who generates questions and decides wheter answers are right or wrong.
* Player: the person who answers the questions generated by host.

At login page, enter your username. Any username is valid(like in any other input SQL injection is allowed).  
Who enters with **admin** username, can act as host. Who enters with any other usernames, will be treated as player.  

### Play routine
This is how game works:
1. At first, host makes a new question.
1. Each player books the possibility to answer the posted question.
1. Host allows the first player in queue to answer the question.
1. The player allowed to answer answers to the question.
1. Host validates the answer.  
If it is right, question gets closed and a new question can be posted.  
If it is wrong, host needs to let next person who booked the answer to have its try.
