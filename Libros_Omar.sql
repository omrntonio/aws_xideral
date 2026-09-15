USE libreria

CREATE table libros_omar (
	libro_id INT AUTO_INCREMENT PRIMARY KEY,
	Titulo VARCHAR(100) NOT NULL,
	Autor VARCHAR(50) NOT NULL,
	Genero VARCHAR(50) NOT NULL,
	Anio_publicacion INT NOT NULL,
	Numero_paginas INT NOT NULL,
	Calificacion DECIMAL NOT NULL,
	Disponible ENUM('Disponible','No Disponible') NOT NULL
	);

#INSERT INTO libros_omar (
		Titulo,
		Autor,
		Genero,
		Anio_publicacion,
		Numero_paginas,
		Calificacion,
		Disponible) 
VALUES  ('Pride and Prejudice','Jane Austen','Romance',1998,367,9.4,'Disponible'),
		('Moby Dick','Herman Melville','Adventure',1851,816,7.0,'Disponible'),
		('The Adventures of Sherlock Holmes','Arthur Conan Doyle','Detective Fiction',1892,328,9.6,'No Disponible'),
		('Crime and Punishment','Fyodor Dostoyevsky','Crime Fiction',1866,689,9.5,'No Disponible'),
		('Dracula','Bram Stoker','Horror',1897,556,8.9,'Disponible'),
		('The strange case of Dr. Jekyll and Mr. Hyde','Robert Louis Stevenson','Mystery',1886,188,9.1,'No Disponible'),
		('The Count of Monte Cristo','Alexandre Dumas and Auguste Maquet','Adventure',1844,1321,9.2,'Disponible'),
		('The Enchanted April','Elizabeth Von Arnim','Love stories',1922,171,8.3,'Disponible'),
		('The Expedition of Humphry Clinker','T. Smollett','Historical Fiction',1771,456,8.9,'No Disponible'),
		('The Wonderful Wizard of Oz','L. Frank Baum','Fantasy',1901,255,9.3,'Disponible');

SELECT * FROM libros_omar;

SELECT Titulo, Autor, Genero FROM libros_omar;

SELECT * FROM libros_omar WHERE Disponible LIKE 'Disponible';

SELECT * FROM libros_omar WHERE Genero LIKE 'Adventure';

SELECT * FROM libros_omar WHERE Anio_publicacion >2000;

SELECT * FROM libros_omar WHERE Calificacion > 8;

SELECT * FROM libros_omar ORDER BY Anio_publicacion DESC;

SELECT Titulo, MAX(Calificacion) as Califacion FROM libros_omar;

SELECT AVG(Numero_paginas) as 'Paginas promedio' FROM libros_omar;

SELECT Genero, count(Genero) as 'Numero de Libros' FROM libros_omar GROUP BY Genero;

SELECT * FROM libros_omar where Titulo LIKE 'THE%';

UPDATE libros_omar
SET Disponible = 'No Disponible'
WHERE libro_id = 17;