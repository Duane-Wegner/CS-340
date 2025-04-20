from pymongo import MongoClient
from bson.objectid import ObjectId

class CRUD:
    """CRUD operations for MongoDB"""

    def __init__(self, username, password, host, port, db, collection):
        """
        Initializes the connection to MongoDB.
        This method sets up the connection to a specified MongoDB database and collection.
        """
        # Connection Variables
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db = db
        self.collection_name = collection
        
        # Initialize Connection
        try:
            # Added authSource parameter for authentication to the 'aac' database
            self.client = MongoClient(f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}?authSource=admin')
            self.database = self.client[self.db]
            self.collection = self.database[self.collection_name]
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def create(self, data):
        """
        Inserts a document into the MongoDB collection.

        Parameter:
         data: A dictionary containing the key/value pairs to be inserted into the collection.

        Return:
         True if the insert is successful, False if there is an issue.
        """
        if data is not None:
            try:
                result = self.collection.insert_one(data)
                if result.acknowledged:
                    return True
                else:
                    return False
            except Exception as e:
                print(f"Error inserting document: {e}")
                return False
        else:
            raise ValueError("Data parameter cannot be None.")

    def read(self, query):
        """
        Queries the MongoDB collection for documents matching the specified query.

        Parameter:
         query: A dictionary containing key/value pairs to query for.

        Return:
         A list of documents (as dictionaries) if the query is successful.
         An empty list if no documents are found or if there is an error.
        """
        if query is not None:
            try:
                # Use find() instead of find_one() to return a cursor
                cursor = self.collection.find(query)
                results = list(cursor)  # Convert cursor to list
                return results
            except Exception as e:
                print(f"Error querying documents: {e}")
                return []
        else:
            raise ValueError("Query parameter cannot be None.")
            
    def update(self, query, new_data, multiple=False):
        """
        Update documents in the MongoDB collection based on the query.

        Parameters:
            query : A dictionary of key-value pairs to match documents to be updated.
            new_data (dict): A dictionary containing the data to update the documents with.
            multiple (bool): Whether to update multiple documents (default is False).

        Returns:
            int: The number of documents modified.
        """
        if query is None or new_data is None:
            raise Exception("Query or new_data cannot be None")

        try:
            if multiple:
                result = self.collection.update_many(query, {'$set': new_data})
            else:
                result = self.collection.update_one(query, {'$set': new_data})
            
            return result.modified_count  # Returns the number of documents modified
        except Exception as e:
            print(f"Error updating documents: {e}")
            return 0

    def delete(self, query):
        """
        Delete documents from the MongoDB collection based on the query.

        Parameters:
            query: A dictionary of key-value pairs to match documents to be deleted.

        Returns:
            int: The number of documents removed.
        """
        if query is None:
            raise Exception("Query cannot be None")

        try:
            result = self.collection.delete_many(query)  # Delete multiple documents
            return result.deleted_count  # Returns the number of documents deleted
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return 0
        else:
            raise ValueError("Query parameter cannot be None.")


# Example usage:
if __name__ == "__main__":
    crud = CRUD()

    # Insert a document
    data = {"name": "Gizzmo", "species": "dog", "age": 2}
    insert_result = crud.create(data)
    print(f"Insert successful: {insert_result}")

    # Query documents
    query = {"species": "dog"}
    query_results = crud.read(query)
    print(f"Query results: {query_results}")
