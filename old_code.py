

#=====================================================
def read_from_file_write(file_path,file_type):
    if file_type == 'csv':
        df = pd.read_csv(file_path)
        logger.info(f'CSV read from file: {file_path}')
    elif file_type == 'json':
        df = pd.read_json(file_path)
        logger.info(f'JSON read from file: {file_path}')
    elif file_type == 'xml':
        df = pd.read_xml(file_path,xpath='.//item')
        logger.info(f'xml read from file: {file_path}')
    else:
        raise ValueError(f'unsupported file type passed: {file_type}')
        logger.info(f'Failed to read from file: {file_path}')
    return df

def read_from_db(df,db_type,table_name):
    if db_type == 'postgress':
        #dc1 = DatabaseConnection()
        connect_to_postgress(df)
        df.read_sql_table(db_type, table_name)
        logger.info(f'Data read from db: {table_name}')
    elif db_type == 'oracle':
        #dc2 = DatabaseConnection()
        oracle_conn
        df.read_sql_table(table_name,db_type)
        logger.info(f'Data read from db: {table_name}')
    else:
        raise ValueError(f'unsupported database type passed: {db_type}')
    return df

def write_to_db(df,table_name,db_type):
    if db_type == 'postgress':
        df.to_sql(table_name,pggress_conn,index=False,if_exists='replace')
        logger.info(f'Data written to db: {table_name}')
    elif db_type == 'oracle':
        df.to_sql(table_name,oracle_conn,index=False,if_exists='replace')
        logger.info(f'Data written to db: {table_name}')
    else:
        raise ValueError(f'unsupported database type passed: {db_type}')
    return df

def download_file_from_linux_server():
    logger.info("File download from linux server has started....")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(LINUX_HOSTNAME,username=LINUX_USERNAME,password=LINUX_PASSWORD)
    sftp = ssh_client.open_sftp()
    sftp.get(REMOTE_FILE_PATH,LOCAL_FILE_PATH)
    sftp.close()
    logger.info("File download from linux server has completed....")



#=================TO LOOK AT THIS LATER=====================#
'''def read_from_db(df,db_type,table_name):
    if db_type == 'postgress':
        #dc1 = DatabaseConnection()
        connect_to_postgress(df)
        df.read_sql_table(db_type, table_name)
        logger.info(f'Data read from db: {table_name}')
    elif db_type == 'oracle':
        #dc2 = DatabaseConnection()
        connect_to_oracle(df)
        df.read_sql_table(table_name,db_type)
        logger.info(f'Data read from db: {table_name}')
    else:
        raise ValueError(f'unsupported database type passed: {db_type}')
    return df'''