import pandas as pd
from sqlalchemy import create_engine


#f=open("../twitter_credentials.txt","r")
f=open("../database_credentials.txt","r")
lines=f.readlines()
# your Twitter API key and API secret
my_host=lines[2].rstrip("\n")
my_user=lines[1].rstrip("\n")
my_db=lines[0].rstrip("\n")
my_password=lines[3].rstrip("\n")
f.close()


# Create dataframe
df = pd.DataFrame(data=[[111,'Thomas','35','United Kingdom'],
		[222,'Ben',42,'Australia'],
		[333,'Harry',28,'India']],
		columns=['id','name','age','country'])

# Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=my_host, db=my_db, user=my_user, pw=my_password))

# Convert dataframe to sql table                                   
df.to_sql('users', engine, index=False)