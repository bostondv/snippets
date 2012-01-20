# Create database
CREATE DATABASE demo;

# Create and grant access to user
GRANT ALL ON demo.* TO user1@localhost IDENTIFIED BY 'mypassword';