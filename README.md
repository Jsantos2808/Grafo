La aplicación implementa una red social interactiva modelada como un grafo no dirigido, donde cada usuario representa un nodo y cada relación de amistad representa una arista bidireccional. La estructura del grafo se gestiona mediante un diccionario de listas de adyacencia (adjacency), optimizando el almacenamiento y la consulta de conexiones.

Se utiliza BFS (Breadth-First Search) para sugerir nuevas amistades, explorando nodos a una distancia de dos niveles, con el fin de identificar posibles amigos en común (amigos de amigos), excluyendo aquellos ya conectados.

La interfaz gráfica está desarrollada con Tkinter y estilizada con ttkbootstrap, proporcionando una experiencia visual moderna. Los usuarios pueden ser creados dinámicamente, posicionados aleatoriamente en un lienzo (Canvas) y conectados visualmente mediante líneas (aristas). Al seleccionar un usuario, se despliega información relevante: su lista de amigos y sugerencias de nuevas amistades, lo que simula el funcionamiento básico de una red social real.

Esta solución combina conceptos de estructuras de datos, algoritmos de grafos y diseño de interfaces gráficas para simular interacciones sociales de forma educativa y visualmente atractiva.

