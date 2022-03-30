import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='1234', host='localhost', port=3306)

# COMANDO PARA DAR DROP
#conn.cursor().execute("DROP DATABASE `bikelibrary`;")
#conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `bikelibrary` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `bikelibrary`;
    CREATE TABLE `bike` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `modelo` varchar(50) COLLATE utf8_bin NOT NULL,
      `marca` varchar(40) COLLATE utf8_bin NOT NULL,
      `modalidade` varchar(40) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `usuario` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `usuario` varchar(20) COLLATE utf8_bin NOT NULL,
      `senha` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO bikelibrary.usuario (usuario, senha) VALUES (%s, %s)',
      [
            ('bruno', '123'),
            ('admin', 'admin')
      ])

cursor.execute('select * from bikelibrary.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo bikes
cursor.executemany(
      'INSERT INTO bikelibrary.bike (modelo, marca, modalidade) VALUES (%s, %s, %s)',
      [
            ('Chisel', 'Specialized', 'MTB'),
      ])

cursor.execute('select * from bikelibrary.bike')
print(' -------------  Bikes:  -------------')
for bike in cursor.fetchall():
    print(bike[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()