# PROYECTO PROGRAMACION ISMAEL

# Main

En el main.py encontramos varios Edpoints, asi como unas funciones de ayuda para buscar productos.

El primer Endpoint se encaraga de crear productos con la url : **post/productos**, se ha de saber que no puede haber 2 productos con el mismo nomnbre y han de indicarse todos sus atrtibutos incluido el id, auqnue MongoDB se encaragará de darle uno propio.

El segundo Endpoint sirve para listar todos los productos, Url : **get/productos**.

El tercer Endpoint se utiliza para actualizar los productos, Url : **put/productos** al igual que en el post se han de indicar todos sus atributos.

El cuarto Endpoint se encarga de eliminar productos, Url: **delete/productos/{id}**, bastará con indicarle la id en la Url para que sea eliminado.

El quinto Endpoint busca los productos por su id, se utiliza igual que el delete, Url: **get/productos/{id}**.

El sexto Endpoint busca los productos por su nombre, Url : **/buscar**, debemos de indicarle medianre query el nombre del producto.

El septimo Endpoint lista los productos por su categoria, debemos de indicar la categopria en la Url, Url : **get/productos/categoria/{categoria}**.

El octavo Endpoint lista los productos en el orden indicado en base a su precio, debemos de indicar el orden mediante query, Url : **get/ordenar**.

El ultimo Endpoint elimina todos los productos de una categoria, indicada en la Url, Url : **delete/productos/categoria/{categoria}/eliminar**.

# Users

El archivo de Users solo contiene dos Endpoints que se deben de utilizar por el usuario, el get/users solo debería de utilizarlo el administrador.

El primer Endpoint es el encargado de registrar a los usuarios en la pagina, el email debe de ser único y la contraseña ha de pasarse encriptada, ya que así se guarda en la abse de datos. Url : **post/Use**.

El segundo Endpoint se encargará de logear al usuario en la pagina y dejarle utilizar todas las funciones que dependan de estar logeado, los parametros del login se han de escribir en el form del body. Url : **post/login**

En el archivo de users tambien encontramos todas las funciones encargadas de la autorización de usuarios, de la encriptacion de contraseñas y de busqueda de usuarios.

# Otros archivos

Los demas archivos no son utilizables por el usuario, sirven para que el proyecto funcione, encontramos el archivo donde indicamos la url de la base de datos y los schemas para la creación de objetos.
