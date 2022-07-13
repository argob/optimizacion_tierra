# Minimización y distribución óptima de la tierra


## El documento de trabajo
El documento "Planificación productiva de alimentos básicos Modelización a partir de la Encuesta Nacional del Gasto de los Hogares y
el Censo Nacional Agropecuario" se propone contribuir a la planificación de la producción de alimentos en Argentina, mediante un análisis
de la alimentación de la población, de las características productivas de una canasta básica objetivo, y
mediante el uso de herramientas de optimización computada. La producción de alimentos y la manera en que se 
abastecen las sociedades de los alimentos necesarios han sido de los temas de mayor trayectoria en las discusiones económicas.
Esto se debe fundamentalmente a que la producción de alimentos es la actividad económica primaria fundamental. 
El fin último de este trabajo reside en aportar a la mejora alimentaria y nutricional de la población argentina.


El documento de trabajo se encuentra disponible en: (poner link)

## Objetivo del repositorio
El repositorio disponibiliza el código para la optimización y distribución óptima de tierra de modo que se puedan profundizar y sofisticar los análisis.
Al estar disponible el código, quines lo manipulen pueden incorporar nuevos cultivos, regiones (como departamentos en lugar de provincias), calcular los rindes de otra manera, actualizar la información, o agregar restricciones como distancias de transporte, emisiones de gases de efecto invernadero, entre otras.


## La optimización
El ejercicio propone dos tipos de matrices de rendimientos cuyos promedios por cultivo son consistentes con los rindes medios.

Matriz de rendimientos A:

![](https://github.com/CEProduccionXXI/optimizacion_tierra/blob/main/intuitivo/Matriz%20de%20rendimientos%20A.PNG?raw=true)

Matriz de rendimientos B:

![](https://github.com/CEProduccionXXI/optimizacion_tierra/blob/main/intuitivo/Matriz%20de%20rendimientos%20B.png?raw=true)

El problema de optimización está planteado del siguiente modo:
![](https://github.com/CEProduccionXXI/optimizacion_tierra/blob/main/intuitivo/Problema%20de%20minimización.png?raw=true)

Las resticciones implmentadas son:
![](https://github.com/CEProduccionXXI/optimizacion_tierra/blob/main/intuitivo/Restricciones.png?raw=true)

Formalmente:

En el problema que estamos analizando existen 23 provincias y 48 cultivos. Por lo tanto existen 1.104 incógnitas $T_{ij}$ para hallar. Entonces, el problema de optimización consiste en encontrar la asignación más eficiente para producir los 48 cultivos en las 23 provincias cuya suma sea la mínima posible, es decir minimizar la expresión:
 
![](https://github.com/CEProduccionXXI/optimizacion_tierra/blob/main/intuitivo/optimo.png?raw=true)

sujeto a:
1. Producto total por cultivo. Este valor se desprende de la canasta de consumo elaborada en el presente trabajo para cada cultivo. Representa el nivel de producción estimado para abastecer a toda la población para que todas las personas puedan consumir en la misma magnitud que el promedio del decil 10.

![](https://github.com/CEProduccionXXI/optimizacion_tierra/blob/main/intuitivo/restriccion1.png?raw=true)

2. Tierras disponibles. Es el límite estimado de disponibilidad de tierras aptas para cultivo en cada provincia. Esta restricción tiene como finalidad que la asignación de tierras resultante a cada provincia no supere el nivel de disponibilidad existente.

![](https://github.com/CEProduccionXXI/optimizacion_tierra/blob/main/intuitivo/restriccion2.png?raw=true)

3. Producir en proporción a la población. Representa una restricción que implica que la
provincia debe producir –siempre que pueda– un porcentaje según su población. Este
porcentaje es controlado por el coeficiente (alfa): cuando vale 0 no debe respetar la
proporción de la población local, por lo que se produce donde es más eficiente; cuando vale
1 se debe producir de todos los cultivos posibles en proporción a la población de la provincia.
Dados los rendimientos en una provincia, la tierra podría no alcanzar por lo que el parámetro
θ (theta) garantiza que una vez ocupado el 100% de la tierra disponible se siga produciendo
el remanente en las restantes que aún cuentan con tierras para alcanzar la producción
objetivo. El dominio de θ se encuentra acotado entre 0 y 1, de modo que no genera un efecto
incremental sobre el límite superior de la restricción.

![](https://github.com/CEProduccionXXI/optimizacion_tierra/blob/main/intuitivo/restriccion3.png?raw=true)

- siendo:

![](https://github.com/CEProduccionXXI/optimizacion_tierra/blob/main/intuitivo/siendo.png?raw=true)


4. No negatividad de las variables. Finalmente, se restringe la posibilidad de que la producción, el rinde o la tierra variables adquieran valores negativos. 

![](https://github.com/CEProduccionXXI/optimizacion_tierra/blob/main/intuitivo/noneg.png?raw=true)


## Links:
Centro de Estudios para la Producción (CEPXXI) - Ministerio de Desarrollo Productivo de la Nación (Argentina): https://www.argentina.gob.ar/produccion/cep

Redes sociales: https://twitter.com/CEPXXI


## Autoría:
* Igal Kejsefman (igalkej[a]gmail.com)
* Facundo Pesce (facundopesce[a]gmail.com)

##### Agradecimientos:
Agradecemos al Dr. Kevin Speyer (@kevo-speyer) por su apoyo en el manejo de las librerías



