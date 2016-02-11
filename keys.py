development = True

def get_mysql_uri():
	if development:
		return "mysql://root:@localhost/njtransit"
	else:
		return os.environ.get("NJTRANSIT_MYSQL_URI")
