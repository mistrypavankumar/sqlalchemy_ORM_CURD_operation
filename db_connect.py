
# This function is used to connect to mysql database
def connectDB(host, database, user, password, port):
    connection_string = f"mysql+mysqlconnector://{
        user}:{password}@{host}:{port}/{database}"

    return connection_string
