# Cat Voting - Vote for Awesome Cats!

This was a simple way of experimenting with SQL databases, APIs and jQuery.

To run do either: 
`bash main.sh` or `chmod +x main.sh && ./main.sh`

## What does this do?

This is a simple web application that allows for users to vote on whether they think a
cat is awesome or extra-awesome. It uses jQuery so send a request to a Python Flask 
web server, which then updates values in an SQL database.

The cats API is provided by [cataas](https://cataas.com/) which is used to get random
images of cats.
