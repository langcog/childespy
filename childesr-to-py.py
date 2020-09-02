import pandas as pd
import json
import requests
import MySQLdb
import sqlalchemy

# translate version
    # takes in a version, arg, and info and returns the correct db version
        # db_info is is a dictionary from the json
        # db_args is a dictionary w/ host and name
def translate_version(db_version, db_args, db_info):

    #if using childes-db hosted server
    if db_args['host'] == db_info['host']:

        #if current version
        if db_version == "current":
            db_to_use = db_info["current"]
            print(f"Using current database version: '{db_to_use}'.")
            return db_to_use

        # if supported version
        elif db_version in db_info['supported']:
            db_to_use = db_version
            print("Using supported database version: ", db_to_use)
            return db_to_use

        #if historical/unsupported version
        elif db_version in db_info['historical']:
            print(f"Version '{db_version}'is no longer hosted by \
            childes-db.stanford.edu; either specify a more recent version or \
            install MySQL Server locally and update db_args.")

    # if not using the hosted server (ie local)
    else:
        return db_args['db_name']

# resolve connection
# if no connection was provided, connect to the most recent version of childes-db
def resolve_connection(connection, db_version=None, db_args=None):
    if connection == None:
        return connect_to_childes(db_version, db_args)
    else:
        return connection

# get db info from the hosted json
def get_db_info():
    url = "https://childes-db.stanford.edu/childes-db.json"
    database_dict = requests.get(url).json()
    return database_dict

# connect to childes
def connect_to_childes(db_version = 'current', db_args = None):
    """Connects to childes-db

    Args:
        db_version: String of the name of the database version to use
        db_args: Dict with host, user, and password defined

    Returns:
        A MySQLdb connection object for the CHILDES database
    """
    db_info = get_db_info()
    if db_args == None:
        db_args = db_info
    childes_con = MySQLdb.connect(
                    host = db_args['host'],
                    #port = db_args['port'], #no port specified in json?
                    user = db_args['user'],
                    passwd = db_args['password'],
                    db = translate_version(db_version, db_args, db_info),
        charset='utf8')
    return childes_con

# check connection
#this isnt the same as the tryCatch from Mika's...
def check_connection(db_version = "current", db_args = None):
    try:
        con = connect_to_childes(db_version, db_args)
        return True
    except:
        con = None
        return False
    return False

# clear connections
#can't figure this one out using MySQLdb but its not used anywhere...

# get table
def get_table(connection, name):
    '''gets a table from the CHILDES database
    Args:
        connection: A connection to the CHILDES database
        name: String of a table name

    Returns:
        A pandas dataframe
    '''
    return(pd.read_sql(f'SELECT * FROM {name}', con=connection))

# get collections
def get_collections(connection=None,
                    db_version= "current",
                    db_args = None):
    connection = resolve_connection(connection, db_version, db_args)
    collections = pd.read_sql(f'SELECT * FROM {"collection"}', con=connection)
    #collections = collections.rename(columns={"id":"collection_id","name":"collection_name"})
    if connection == None:
        # Mika's code is collections %<>% dplyr::collect()
        # DBI::dbDisconnect(con)
        # not sure what to do in python?
        None
    return collections

# get corpora

# get transcripts

# get particpants

# get speaker statistics

# get content

# get tokens

# get types

# get utterances

# get contexts

# get database version
