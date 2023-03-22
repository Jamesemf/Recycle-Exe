# Testing Strategy

- The testing strategy that we applied to test our code was to check each url sequentially and test the views associated with them.
We first tested the response codes returned by get and post request to each view for the case where a user wasn't logged in, and the case where a user was logged in.
We also tested the case that a user was logged in as a superuser for the gamekeeper page.

- We also used Django's response.redirect_chain to check that views redirected to the correct URLs, depending on the session variables and post request parameters we parsed in.

- After these tests were complete, we then tested for data modification in each view. This was done using using Django's response.context function to access values returned by data dictionaries from views. It was also done by checking that the fields of test Objects that we had created were modified appropriately.