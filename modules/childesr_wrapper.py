# a wrapper for the childesr package

#import rpy2 objects and interface
from rpy2 import rinterface
from rpy2 import rinterface_lib as r_lib
from rpy2.robjects.vectors import StrVector, FloatVector, BoolVector

#activate r dataframe to pandas conversion
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
### function conversion ###

#translate_version - not a callable function in the R script, not needed here?
def translate_version(db_version, db_args, db_info):
    return(childesr.translate_version(db_version, db_args, db_info))

#resolve connection - not a callable function in the R script, not needed here?
def resolve_connection(connection, db_version = None, db_args = None):
    db_version = convert_null(db_version)
    db_args = convert_null(db_args)
    r_connection = childesr.resolve_connection(connection, db_version, db_args)
    return(r_connection)

#get db info
def get_db_info():
    r_db_info = childesr.get_db_info()
    db_dict = dict(zip(r_db_info.names, map(list,list(r_db_info))))
    return db_dict

#connect to childes
# note: this returns an R 'MySQLConnection' object, no python equivalent
def connect_to_childes(db_version = "current", db_args = None):
    db_args = convert_null(db_args)
    return(childesr.connect_to_childes(db_version, db_args))

#check_connection
def check_connection(db_version = "current", db_args = None):
    db_args = convert_null(db_args)
    return(childesr.check_connection(db_version, db_args)[0])

#clear_connections
def clear_connections():
    return(childesr.clear_connections())

#get_table - not callable from chilesr, not needed here?
def get_table(connection, name):
    return(childesr.get_table(connection, name))

#get_collections
def get_collections(connection = None, db_version = "current",
                            db_args = None):
    connection = convert_null(connection)
    db_args = convert_null(db_args)
    collections = childesr.get_collections(connection, db_version, db_args)
    collections = collections.apply(np.vectorize(convert_r_to_py))
    return(collections)

#get_corpora
def get_corpora(connection = None, db_version = "current", db_args = None):
    #convert arguments
    connection = convert_null(connection)
    db_args = convert_null(db_args)
    r_corpora = childesr.get_corpora(connection, db_version, db_args)
    r_corpora = r_corpora.apply(np.vectorize(convert_r_to_py))

    return(r_corpora)

#get_transcripts
def get_transcripts(collection = None, corpus= None, target_child=None,
connection= None, db_version = "current", db_args = None):
    # convert base
    connection = convert_null(connection)
    db_args = convert_null(db_args)

    # convert optional args
    collection = convert_r_vector(collection)
    corpus = convert_r_vector(corpus)
    target_child = convert_r_vector(target_child)

    r_transcripts = childesr.get_transcripts(collection, corpus, target_child, connection, db_version,db_args)
    r_transcripts = r_transcripts.apply(np.vectorize(convert_r_to_py))

    return(r_transcripts)

#get_participants
def get_participants(collection = None, corpus = None, target_child = None,
                    role = None, role_exclude = None, age = None, sex = None,
                    connection = None, db_version = "current", db_args = None):
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
    r_participants = r_participants.apply(np.vectorize(convert_r_to_py))

    return(r_participants)

#get_speaker_statistics
def get_speaker_statistics(collection = None, corpus = None, target_child = None,
                            role = None, role_exclude = None, age = None, sex = None,
                            connection = None, db_version = "current", db_args = None):
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
    r_speaker_statistics = r_speaker_statistics.apply(np.vectorize(convert_r_to_py))

    return(r_speaker_statistics)

#get_content - not in the package

#get_tokens
def get_tokens(token, collection = None, language = None, corpus = None,
                target_child = None, role = None, role_exclude = None,
                age = None, sex = None, stem = None,
                part_of_speech = None, replace = True, connection = None,
                db_version = "current", db_args = None):

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

    r_get_tokens = r_get_tokens.apply(np.vectorize(convert_r_to_py))
    return(r_get_tokens)
#get_types
def get_types(collection = None, language = None, corpus = None,
                           role = None, role_exclude = None, age = None,
                           sex = None, target_child = None, type = None, connection = None,
                           db_version = "current", db_args = None):

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
    r_types = r_types.apply(np.vectorize(convert_r_to_py))

    return(r_types)

#get_utterances
def get_utterances(collection = None, language = None, corpus = None,
                           role = None, role_exclude = None, age = None,
                           sex = None, target_child = None, connection = None,
                           db_version = "current", db_args = None):
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
    r_utterances = r_utterances.apply(np.vectorize(convert_r_to_py))

    return(r_utterances)
#get_contexts
def get_contexts(token = None, collection=None, language=None, corpus=None,
                        role=None, role_exclude=None, age=None,
                        sex=None, target_child=None,
                        window = [0,0], remove_duplicates = True,
                        connection=None, db_version = "current",
                        db_args=None):

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

    r_contexts = r_contexts.apply(np.vectorize(convert_r_to_py))

    return(r_contexts)
#get_database_version
def get_database_version(connection = None, db_version = "current", db_args = None):
    connection = convert_null(connection)
    db_args = convert_null(db_args)
    return(childesr.get_database_version(connection, db_version,db_args)[0])
