# a wrapper for the childesr package

#import rpy2 objects and interface
from rpy2 import rinterface
from rpy2 import rinterface_lib as r_lib
from rpy2.robjects.vectors import StrVector, FloatVector, BoolVector
from rpy2.robjects.conversion import localconverter
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
import numpy as np
pandas2ri.activate()

#install childesr if not installed and then import
from rpy2.robjects.packages import importr

utils = importr('utils')
def importr_tryhard(packname):
    try:
        rpack = importr(packname)
    except:
        utils.install_packages(packname)
        rpack = importr(packname)
    return rpack
childesr = importr_tryhard('childesr')

### helper functions ###
def convert_null(conv_arg):
    return(rinterface.NULL if conv_arg == None else conv_arg)

def convert_r_vector(python_input):
    #need to do gross returns in each if - better option?
    if python_input == None:
        #if none return null
        return(rinterface.NULL)
    if isinstance(python_input, bool):
        r_vec = BoolVector([python_input])
    if isinstance(python_input, list):
        if all(isinstance(x, str) for x in python_input):
            r_vec = StrVector(python_input)
        elif all(isinstance(x, int) for x in python_input):
            r_vec = FloatVector(python_input)
        elif all(isinstance(x, float) for x in python_input):
            r_vec = FloatVector(python_input)
    elif isinstance(python_input, str):
        r_vec = StrVector([python_input])
    elif isinstance(python_input, float) or isinstance(python_input, int):
        r_vec = FloatVector([python_input])
    return(r_vec)

def convert_r_to_py(r_input):
    if isinstance(r_input, r_lib.sexp.NACharacterType):
        return(None)
    else:
        return(r_input)

def r_df_to_pandas(r_df):
    with localconverter(ro.default_converter + pandas2ri.converter):
        pd_from_r_df = ro.conversion.rpy2py(r_df)
    return(pd_from_r_df)
### function conversion ###


#get db info
def get_db_info():
    '''
    Returns a dictionary with the most recent database info from childes
    '''
    r_db_info = childesr.get_db_info()
    db_dict = dict(zip(r_db_info.names, map(list,list(r_db_info))))
    return db_dict

#connect to childes
# note: this returns an R 'MySQLConnection' object, no python equivalent
def connect_to_childes(db_version = "current", db_args = None):
    """Connects to childes-db

    Args:
        db_version: String of the name of the database version to use (default "current")
        db_args: Dict with host, user, and password defined (default None)

    Returns:
        An R MySQLConnection object connection
    """
    db_args = convert_null(db_args)
    return(childesr.connect_to_childes(db_version, db_args))

#check_connection
def check_connection(db_version = "current", db_args = None):
    '''
    Check if connecting to childes db is possible

    Args:
        db_version: String of the name of the database version to use (default "current")
        db_args: Dict with host, user, and password defined (default None)

    Returns:
        Boolean indicating whether a connection was successfully formed
    '''
    db_args = convert_null(db_args)
    return(childesr.check_connection(db_version, db_args)[0])

#clear_connections
def clear_connections():
    '''
    Clear all MySQL connections
    '''
    return(childesr.clear_connections())

def get_collections(connection = None, db_version = "current", db_args = None):
    '''
    Get the collections from childesdb

    Args:
        connection: A connection to the CHILDES database (default None)
        db_version: String of the name of the database version to use (default "current")
        db_args: Dict with host, user, and password defined (default None)

    Returns:
        A pandas dataframe of Collection data. If `connection` is supplied, the result remains a remote query, otherwise it is retrieved locally.
    '''
    connection = convert_null(connection)
    db_args = convert_null(db_args)
    collections = childesr.get_collections(connection, db_version, db_args)
    collections = r_df_to_pandas(collections)
    collections = collections.apply(np.vectorize(convert_r_to_py))
    return(collections)

#get_corpora
def get_corpora(connection = None, db_version = "current", db_args = None):
    '''
    Get the corpora data

    Args:
        connection: A connection to the CHILDES database (default None)
        db_version: String of the name of the database version to use (default "current")
        db_args: Dict with host, user, and password defined (default None)

    Returns:
        A pandas dataframe of Corpus data. If `connection` is supplied, the result remains a remote query, otherwise it is retrieved locally.
    '''
    #convert arguments
    connection = convert_null(connection)
    db_args = convert_null(db_args)
    r_corpora = childesr.get_corpora(connection, db_version, db_args)
    r_corpora = r_df_to_pandas(r_corpora)
    r_corpora = r_corpora.apply(np.vectorize(convert_r_to_py))

    return(r_corpora)

#get_transcripts
def get_transcripts(collection = None, corpus= None, target_child=None,
connection= None, db_version = "current", db_args = None):
    '''
    Gets the transcripts with supplied filters

    Args:
        collection: A string or list of strings of one or more names of collections (default None)
        corpus: A string or list of strings of one or more names of corpora (default None)
        target_child: A string or list of strings of one or more names of children (default None)
        connection: A connection to the CHILDES database (default None)
        db_version: String of the name of the database version to use (default "current")
        db_args: Dict with host, user, and password defined (default None)

    Returns:
    A pandas dataframe of Transcript data, filtered down by supplied arguments. If `connection` is supplied, the result remains a remote query, otherwise it is retrieved locally.
    '''
    # convert base
    connection = convert_null(connection)
    db_args = convert_null(db_args)

    # convert optional args
    collection = convert_r_vector(collection)
    corpus = convert_r_vector(corpus)
    target_child = convert_r_vector(target_child)

    r_transcripts = childesr.get_transcripts(collection, corpus, target_child, connection, db_version,db_args)
    r_transcripts = r_df_to_pandas(r_transcripts)
    r_transcripts = r_transcripts.apply(np.vectorize(convert_r_to_py))

    return(r_transcripts)

#get_participants
def get_participants(collection = None, corpus = None, target_child = None,
                    role = None, role_exclude = None, age = None, sex = None,
                    connection = None, db_version = "current", db_args = None):
    '''
    Gets the participant data filtered by the supplied arguments

    Args:
        collection: A string or list of strings of one or more names of collections (default None)
        corpus: A string or list of strings of one or more names of corpora (default None)
        target_child: A string or list of strings of one or more names of children (default None)
        role: A string or list of strings of one or more roles to include (default None)
        role_exclude: A string or list of strings of one or more roles to exclude (default None)
        age: An int or float of an single age value or a list of ints or floats with min age value (inclusive) and max age value (exclusive) in months. For a single age value, participants are returned for which that age is within their age range; for two ages, participants are returned for whose age overlaps with the interval between those two ages. (default None)
        sex: A string of values "male" and/or "female" (default None)
        connection: A connection to the CHILDES database (default None)
        db_version: String of the name of the database version to use (default "current")
        db_args: Dict with host, user, and password defined (default None)

    Returns:
    A pandas dataframe of Participant data, filtered down by supplied arguments. If `connection` is supplied, the result remains a remote query, otherwise it is retrieved locally.
    '''
    # convert base
    connection = convert_null(connection)
    db_args = convert_null(db_args)

    #convert optional args
    collection = convert_r_vector(collection)
    corpus = convert_r_vector(corpus)
    target_child = convert_r_vector(target_child)
    role = convert_r_vector(role)
    role_exclude = convert_r_vector(role_exclude)
    age = convert_r_vector(age)
    sex = convert_r_vector(sex)

    #get r table
    r_participants = childesr.get_participants(collection, corpus, target_child, role, role_exclude, age, sex, connection, db_version, db_args)
    r_participants = r_df_to_pandas(r_participants)
    r_participants = r_participants.apply(np.vectorize(convert_r_to_py))

    return(r_participants)

#get_speaker_statistics
def get_speaker_statistics(collection = None, corpus = None, target_child = None,
                            role = None, role_exclude = None, age = None, sex = None,
                            connection = None, db_version = "current", db_args = None):
    '''
    Gets the speaker data filtered by the supplied arguments

    Args:
        collection: A string or list of strings of one or more names of collections (default None)
        corpus: A string or list of strings of one or more names of corpora (default None)
        target_child: A string or list of strings of one or more names of children (default None)
        role: A string or list of strings of one or more roles to include (default None)
        role_exclude: A string or list of strings of one or more roles to exclude (default None)
        age: An int or float of an single age value or a list of ints or floats with min age value (inclusive) and max age value (exclusive) in months. For a single age value, participants are returned for which that age is within their age range; for two ages, participants are returned for whose age overlaps with the interval between those two ages. (default None)
        sex: A string of values "male" and/or "female" (default None)
        connection: A connection to the CHILDES database (default None)
        db_version: String of the name of the database version to use (default "current")
        db_args: Dict with host, user, and password defined (default None)

    Returns:
    A pandas dataframe of Speaker statistics data, filtered down by supplied arguments. If `connection` is supplied, the result remains a remote query, otherwise it is retrieved locally.
    '''
    # convert base
    connection = convert_null(connection)
    db_args = convert_null(db_args)

    #convert optional args
    collection = convert_r_vector(collection)
    corpus = convert_r_vector(corpus)
    target_child = convert_r_vector(target_child)
    role = convert_r_vector(role)
    role_exclude = convert_r_vector(role_exclude)
    age = convert_r_vector(age)
    sex = convert_r_vector(sex)

    #get r table
    r_speaker_statistics = childesr.get_speaker_statistics(collection, corpus, target_child, role, role_exclude, age, sex, connection, db_version, db_args)
    r_speaker_statistics = r_df_to_pandas(r_speaker_statistics)
    r_speaker_statistics = r_speaker_statistics.apply(np.vectorize(convert_r_to_py))

    return(r_speaker_statistics)

#get_content - not in the package

#get_tokens
def get_tokens(token, collection = None, language = None, corpus = None,
                target_child = None, role = None, role_exclude = None,
                age = None, sex = None, stem = None,
                part_of_speech = None, replace = True, connection = None,
                db_version = "current", db_args = None):
    '''
    Gets the token data filtered by the supplied arguments

    Args:
        token: A string or list of strings of one or more token patterns (`\%` matches any number of wildcard characters, `_` matches exactly one wildcard character)
        collection: A string or list of strings of one or more names of collections (default None)
        language: A string or list of strings of one or more languages (default None)
        corpus: A string or list of strings of one or more names of corpora (default None)
        target_child: A string or list of strings of one or more names of children (default None)
        role: A string or list of strings of one or more roles to include (default None)
        role_exclude: A string or list of strings of one or more roles to exclude (default None)
        age: An int or float of an single age value or a list of ints or floats with min age value (inclusive) and max age value (exclusive) in months. For a single age value, participants are returned for which that age is within their age range; for two ages, participants are returned for whose age overlaps with the interval between those two ages. (default None)
        sex: A string of values "male" and/or "female" (default None)
        part_of_speech: A string or list of strings of one or more parts of speech (default None)
        replace: A boolean indicating whether to replace "gloss" with "replacement" (i.e. phonologically assimilated form), when available (default True)
        connection: A connection to the CHILDES database (default None)
        db_version: String of the name of the database version to use (default "current")
        db_args: Dict with host, user, and password defined (default None)

    Returns:
    A pandas dataframe of Token data, filtered down by supplied arguments. If `connection` is supplied, the result remains a remote query, otherwise it is retrieved locally.
    '''

    connection = convert_null(connection)
    db_args = convert_null(db_args)

    collection = convert_r_vector(collection)
    language = convert_r_vector(language)
    corpus = convert_r_vector(corpus)
    target_child = convert_r_vector(target_child)
    role = convert_r_vector(role)
    role_exclude = convert_r_vector(role_exclude)
    age = convert_r_vector(age)
    sex = convert_r_vector(sex)
    token = convert_r_vector(token)
    stem = convert_r_vector(stem)
    part_of_speech = convert_r_vector(part_of_speech)
    replace = convert_r_vector(replace)

    r_get_tokens = childesr.get_tokens(collection, language, corpus,
                    target_child, role, role_exclude,
                    age, sex, token, stem,
                    part_of_speech, replace, connection,
                    db_version, db_args)
    r_get_tokens = r_df_to_pandas(r_get_tokens)
    r_get_tokens = r_get_tokens.apply(np.vectorize(convert_r_to_py))
    return(r_get_tokens)
#get_types
def get_types(collection = None, language = None, corpus = None,
                           role = None, role_exclude = None, age = None,
                           sex = None, target_child = None, type = None, connection = None,
                           db_version = "current", db_args = None):
    '''
    Gets the token data filtered by the supplied arguments

    Args:
        type: A string or list of strings of one or more type patterns (`%` matches any number of wildcard characters, `_` matches exactly one wildcard character)
        collection: A string or list of strings of one or more names of collections (default None)
        language: A string or list of strings of one or more languages (default None)
        corpus: A string or list of strings of one or more names of corpora (default None)
        target_child: A string or list of strings of one or more names of children (default None)
        role: A string or list of strings of one or more roles to include (default None)
        role_exclude: A string or list of strings of one or more roles to exclude (default None)
        age: An int or float of an single age value or a list of ints or floats with min age value (inclusive) and max age value (exclusive) in months. For a single age value, participants are returned for which that age is within their age range; for two ages, participants are returned for whose age overlaps with the interval between those two ages. (default None)
        sex: A string of values "male" and/or "female" (default None)
        connection: A connection to the CHILDES database (default None)
        db_version: String of the name of the database version to use (default "current")
        db_args: Dict with host, user, and password defined (default None)

    Returns:
    A pandas dataframe of Type data, filtered down by supplied arguments. If `connection` is supplied, the result remains a remote query, otherwise it is retrieved locally.
    '''

    connection = convert_null(connection)
    db_args = convert_null(db_args)

    collection = convert_r_vector(collection)
    language = convert_r_vector(language)
    corpus = convert_r_vector(corpus)
    target_child = convert_r_vector(target_child)
    role = convert_r_vector(role)
    role_exclude = convert_r_vector(role_exclude)
    age = convert_r_vector(age)
    sex = convert_r_vector(sex)
    type = convert_r_vector(token)

    r_types = childesr.get_types(collection, language, corpus,
                               role, role_exclude, age,
                               sex, target_child, type, connection,
                               db_version, db_args)
    r_types = r_df_to_pandas(r_types)
    r_types = r_types.apply(np.vectorize(convert_r_to_py))

    return(r_types)

#get_utterances
def get_utterances(collection = None, language = None, corpus = None,
                           role = None, role_exclude = None, age = None,
                           sex = None, target_child = None, connection = None,
                           db_version = "current", db_args = None):
    '''
    Gets the utterance data filtered by the supplied arguments

    Args:
        collection: A string or list of strings of one or more names of collections (default None)
        language: A string or list of strings of one or more languages (default None)
        corpus: A string or list of strings of one or more names of corpora (default None)
        target_child: A string or list of strings of one or more names of children (default None)
        role: A string or list of strings of one or more roles to include (default None)
        role_exclude: A string or list of strings of one or more roles to exclude (default None)
        age: An int or float of an single age value or a list of ints or floats with min age value (inclusive) and max age value (exclusive) in months. For a single age value, participants are returned for which that age is within their age range; for two ages, participants are returned for whose age overlaps with the interval between those two ages. (default None)
        sex: A string of values "male" and/or "female" (default None)
        connection: A connection to the CHILDES database (default None)
        db_version: String of the name of the database version to use (default "current")
        db_args: Dict with host, user, and password defined (default None)

    Returns:
    A pandas dataframe of Type data, filtered down by supplied arguments. If `connection` is supplied, the result remains a remote query, otherwise it is retrieved locally.
    '''
    connection = convert_null(connection)
    db_args = convert_null(db_args)

    collection = convert_r_vector(collection)
    language = convert_r_vector(language)
    corpus = convert_r_vector(corpus)
    target_child = convert_r_vector(target_child)
    role = convert_r_vector(role)
    role_exclude = convert_r_vector(role_exclude)
    age = convert_r_vector(age)
    sex = convert_r_vector(sex)

    r_utterances = childesr.get_utterances(collection, language, corpus,
                               role, role_exclude, age,
                               sex, target_child, connection,
                               db_version, db_args)
    r_utterances = r_df_to_pandas(r_utterances)
    r_utterances = r_utterances.apply(np.vectorize(convert_r_to_py))

    return(r_utterances)
#get_contexts
def get_contexts(token = None, collection=None, language=None, corpus=None,
                        role=None, role_exclude=None, age=None,
                        sex=None, target_child=None,
                        window = [0,0], remove_duplicates = True,
                        connection=None, db_version = "current",
                        db_args=None):
    '''
    Gets the contexts surrounding a token filtered by the supplied arguments

    Args:
        collection: A string or list of strings of one or more names of collections (default None)
        language: A string or list of strings of one or more languages (default None)
        corpus: A string or list of strings of one or more names of corpora (default None)
        target_child: A string or list of strings of one or more names of children (default None)
        role: A string or list of strings of one or more roles to include (default None)
        role_exclude: A string or list of strings of one or more roles to exclude (default None)
        age: An int or float of an single age value or a list of ints or floats with min age value (inclusive) and max age value (exclusive) in months. For a single age value, participants are returned for which that age is within their age range; for two ages, participants are returned for whose age overlaps with the interval between those two ages. (default None)
        sex: A string of values "male" and/or "female" (default None)
        window: A length 2 list of integers of how many utterances before and after each utterance containing the target token to retrieve (default [0,0])
        remove_duplicates A boolean indicating whether to remove duplicate utterances from the results (default True)
        connection: A connection to the CHILDES database (default None)
        db_version: String of the name of the database version to use (default "current")
        db_args: Dict with host, user, and password defined (default None)

    Returns:
    A pandas dataframe of Type data, filtered down by supplied arguments. If `connection` is supplied, the result remains a remote query, otherwise it is retrieved locally.
    '''
    connection = convert_null(connection)
    db_args = convert_null(db_args)

    token = convert_r_vector(token)
    collection = convert_r_vector(collection)
    language = convert_r_vector(language)
    corpus = convert_r_vector(corpus)
    target_child = convert_r_vector(target_child)
    role = convert_r_vector(role)
    role_exclude = convert_r_vector(role_exclude)
    age = convert_r_vector(age)
    sex = convert_r_vector(sex)
    window = convert_r_vector(window)
    remove_duplicates = convert_r_vector(remove_duplicates)

    r_contexts = childes.get_contexts(token, collection, language, corpus,
                            role, role_exclude, age,
                            sex, target_child,
                            window, remove_duplicates,
                            connection, db_version,
                            db_args)
    r_contexts = r_df_to_pandas(r_contexts)
    r_contexts = r_contexts.apply(np.vectorize(convert_r_to_py))

    return(r_contexts)

#get_database_version
def get_database_version(connection = None, db_version = "current", db_args = None):
    '''
    Gets the database version name as a string

    Args:
        connection: A connection to the CHILDES database (default None)
        db_version: String of the name of the database version to use (default "current")
        db_args: Dict with host, user, and password defined (default None)
    '''
    connection = convert_null(connection)
    db_args = convert_null(db_args)
    return(childesr.get_database_version(connection, db_version,db_args)[0])

# can impliment after childesr updated
#def get_sql_query(sql_query_string, connection = None, db_version = "current", db_args=None):
#    '''
#    Run a SQL Query string on the CHILDES #database
#    Args:
#        sql_query_string: a tring of a SQL query
#        connection: A connection to the CHILDES database (default None)
#        db_version: String of the name of the database version to use (default "current")
#        db_args: Dict with host, user, and password defined (default None)
#    '''
#    connection = convert_null(connection)
#    db_args = convert_null(db_args)
#
#    r_sql_query = childesr.get_sql_query(sql_query_string, connection, db_version, db_args)
#    r_sql_query = r_df_to_pandas(r_sql_query)
#    r_sql_query = r_sql_query.apply(np.vectorize(convert_r_to_py))
#    return(r_sql_query)
