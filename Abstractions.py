import pandas

class Abstractions:

    @classmethod
    def generate_call_list(cls):
        """Generate the Review Call List midway through the month
        """


        # loop through the names and get the aldIDs in a dictionary with the name as the key and value as the aldIDs, then go through the aldIDs and check the last review_date (simple timedelta and print the clients required for a review call)