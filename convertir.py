import pymysql

def ejecutar_sql(instruccion):
    try:
        cursor.execute(alter)
        conexion.commit()
    except Exception as e:
        print ('INSTRUCCION SQL :', alter)
        print ('ERROR: ' + str(e)+'\n')
        return False

    return True




# Seteo los valores de conexión
host          = input ('Host [localhost]           : ') or 'localhost'
user          = input ('User [root]                : ') or 'root'
password      = input('Password                    : ')
database      = input('Database                    : ')
charactet_set = input('Character Set [utf8mb4]     : ') or 'utf8mb4'
collate       = input('Collate [utf8mb4_unicode_ci]: ') or 'utf8mb4_unicode_ci'



# Creo conexión a la DB
try:
    conexion = pymysql.connect(
        host     = host,
        user     = user, 
        password = password)
except Exception as e:
    print('Error de conexión')
    print(str(e))
    exit()

    
# Cambio charset DB
cursor = conexion.cursor()
alter = f"""ALTER DATABASE
    {database}
    CHARACTER SET = {charactet_set} 
    COLLATE = {collate};
    """
if ejecutar_sql(alter) == False:
    print ('Cancelado')
    exit()


# Copio nombre tablas a lista
cursor = conexion.cursor()
cursor.execute(f'use {database}')
cursor.execute("show full tables where Table_Type = 'BASE TABLE'")
tablas = [tbl[0] for tbl in cursor.fetchall()]


# Para cada tabla de la DB
for tbl in tablas:
    print(tbl)
    alter = f"""
            ALTER TABLE
            {tbl}
            CONVERT TO CHARACTER SET {charactet_set} 
            COLLATE {collate};
            """

    if ejecutar_sql(alter)== False:
        continue
    


    # Para cada columna de la tabla
    cursor.execute(f'DESCRIBE {tbl}')
    for col in cursor.fetchall():
        col_nombre, col_tipo = col [:2]
        if 'VARCHAR' in col_tipo.upper():

            alter = f'''ALTER TABLE
                {tbl}
                CHANGE {col_nombre} {col_nombre} 
                {col_tipo}
                CHARACTER SET {charactet_set} 
                COLLATE {collate}
                '''
            ejecutar_sql(alter)

conexion.close()




