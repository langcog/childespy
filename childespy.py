#python connector for childes db
import MySQLdb
import sqlalchemy

params = {
	'hostname' : 'ec2-54-68-171-132.us-west-2.compute.amazonaws.com',
	'db_name' : 'childesdb',
	'username' : 'childesdb',
	'pw' : 'uy5z4hf7ihBjf',
	'port':3306
}	

def connect(params=params):
	childes_con = MySQLdb.connect(
				host = params['hostname'], 
                port = params['port'],
                user = params['username'], 
                passwd = params['pw'], 
                db = params['db_name'])
	return(childes_con)

#[ ] replace with a call to the most recent .json on the static site	
