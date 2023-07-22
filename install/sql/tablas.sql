#SQL Tables


#Tabla para usuarios 

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user VARCHAR(50) NOT NULL,
  password VARCHAR(128) NOT NULL,
  email VARCHAR(100) NOT NULL,
  telefono VARCHAR(20) NOT NULL,
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
