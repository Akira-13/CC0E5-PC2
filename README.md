# PC2 - Hashing por tabulación k-independiente

## Descripción

Este proyecto implementa algoritmos de hashing de tabulación y muestra el funcionamiento del algoritmo de hashing de tabulación simple en la estructura de datos de filtro de Bloom y del algoritmo de tabulación "curvado" en la estructura Cuckoo Hashing. Además, muestra pruebas de uniformidad, tasas de falso positivos y máxima carga en las estructuras y algoritmos implementados.

### Algoritmos de hashing

#### Tabulation Hashing

Este algoritmo de hashing es simple en funcionamiento pero bastante eficiente cuando se requieren hashes independientes y uniformes. Esencialmente, cada clave se divide en un conjunto de *chunks* o "trozos" de un tamaño específico. Se generan tablas de números aleatorios para cada *chunk* y cada *chunk* se mapea a uno de estos números. Estos números, finalmente, se combinan mediante operaciones XOR para obtener el hash final.

Este hash es altamente eficiente porque solo se limita a recuperar valores de tablas y realizar operaciones XOR. Además, mantiene una alta uniformidad por su universalidad y 3-independencia. En otras palabras, sus resultados son  aleatorios en práctica.

#### Twisted Tabulation

Este algoritmo es una mejora sobre el hashing por tabulación que introduce más aleatoriedad en los hashes. Además de las operaciones XOR del hashing por tabulación, se realiza un XOR final con un valor aleatorio específico para esa clave, lo cual reduce aun más posibles dependencias en el hashing por tabulación simple. Aunque todavía es una función de hash 3-independiente, tiene mayores garantías de aleatoriedad que el hashing simple sin aumentar considerablemente el número de operaciones.

#### Double Tabulation

Este algoritmo, esencialmente, aplica la función de hash dos veces: Una sobre el valor original y una segunda sobre el resultado de la primera. Este hashing doble aumenta la aleatoriedad (es similar a aplicar un hash a un valor ya aleatorio) y actúa similarmente a una función de hash con 4-independencia a cambio de un mayor número de operaciones y espacio requerido.

### Estructuras

#### Bloom Filter

Esta estructura de datos resuelve el problema de verificar si un elemento pertenece o no a un conjunto de forma eficiente a cambio de la posibilidad de falsos positivos.

El filtro de Bloom mantiene un arreglo de bits. Para almacenar un elemento en esta estructura, se aplican funciones de hash independientes que indexan al arreglo de bits. Cada hash establece como 1 al bit en la posición a la que indexa. Cuando se verifica si un elemento pertenece o no a la estructura, se le aplica las funciones hash y se verifica el valor de los bits en las posiciones indexadas. Si todos los bits son 1, entonces el elemento **posiblemente** se encuentre en la estructura. Caso contrario, si al menos un bit es 0, entonces el elemento **definitivamente** no se encuentra en la estructura.

Esta estructura es altamente eficiente para verificar la presencia de elementos en un conjunto, ya que no almacena directamente los elementos, sino simplemente un conjunto de bits. Esto permite ahorrar espacio y aumentar la velocidad de búsqueda de un elemento, la cual solo dependerá del número de funciones de hash usados.

#### Cuckoo Hashing

Esta estructura cumple la misma función de una tabla hash: verifica la existencia o no de un elemento en un conjunto. Sin embargo, hace esto manteniendo dos tablas distintas y dos funciones hash.

Cuando se inserta un elemento, se le aplica una función hash que indexa una tabla. Si la posición en la primera tabla está disponible, se agrega directamente. Sin embargo, si no está libre, se remueve el elemento de esta posición y se inserta. Se aplica una función hash distinta al elemento removido para verificar si puede ser agregado a la segunda tabla y se repite este proceso (similar a como algunas especies de aves "cuckoo" patean huevos entre nidos cuando no tiene espacio).

Esta estructura resuelve el problema de usar listas enlazadas (*buckets*) o un sondeo lineal en una tabla hash cuando ocurren colisiones. Es decir, tiene un mejor uso de memoria y menor número de operaciones frente a colisiones, puesto que solo requiere revisar en dos tablas para verificar la existencia de un elemento 

## Ejecución

### Requerimientos

- Python 3.0+
- pip
- git (opcional)

### Instrucciones

1. Clonar o descargar el repositorio.

```bash
git clone https://github.com/Akira-13/CC0E5-PC2.git
```

2. Instalar los paquetes necesarios en `requirements.txt` (Recomendable usar un ambiente virtual).

```bash
pip install -r requirements.txt
```

3. Para ejecutar los scripts drivers o profilers, se llaman como aplicación de Python de la siguiente forma:

```bash
python -m driver.<script a ejecutar sin extensión>
```

```bash
python -m profilers.<script a ejecutar sin extensión>
```

Los resultados estadísticos, como los de los profilers, se guardan en `statistics/`

## Proyecto desarrollado

### Estructura

```
├── README.md
├── requirements.txt
├── Informe Técnico.ipynb
├── driver
│   ├── driver_cuckoo_hashing.py
│   ├── driver_false_positive_bf.py
│   ├── driver_tabulation_bloom_filter.py
│   ├── driver_uniformity_analysis.py
├── profilers
│   ├── profiler_bloom_filter.py
│   ├── profiler_cuckoo_hashing.py
├── statistics
│   ├── cuckoo_failure_vs_load.py
│   ├── profile_average_bf_plot.py
│   ├── simple_tabulation_uniformity_analysis.py
│   ├── ...
├── structures
│   ├── __init__.py
│   ├── cuckoo_hashing.py
│   └── tabulated_bloom_filter.py
├── tabulation_hashes
│   ├── __init__.py
│   ├── double_tabulation_hash.py
│   ├── tabulation_hash.py
│   └── twisted_tabulation_hash.py
└── tests
    ├── test_cuckoo_hashing.py
    └── test_tabulated_bloom_filter.py
```

- `driver`: Scripts que utilizan las estructuras o algoritmos desarrollados pero no están destinados a perfilar su rendimiento.
  - `driver_cuckoo_hashing.py`: Demostración de la estructura Cuckoo Hashing con Tabulation Hashing.
  - `driver_tabulation_bloom_filter.py`: Demostración de la estructura Bloom Filter con Tabulation Hashing.
  - `driver_false_positive_bf.py`: Comparación de las tasas de falsos positivos real y teórica en Bloom Filter.
  - `driver_uniformity_analysis.py`: Análisis de la uniformidad de los algoritmos de hashing desarrollados.

- `profilers`: Scripts destinados a perfilar el rendimiento de las estructuras desarrolladas.

- `statistics`: Resultados estadísticos de los scripts en `driver` y `profilers`

- `structures`: Estructuras de datos desarrolladas basadas en Tabulation Hashing.
  - Cuckoo Hashing
  - Bloom Filter

- `tabulation_hashes`: Funciones de hashing basadas en tabulación.
  - Tabulation hash.
  - Double Tabulation Hash.
  - Twisted Tabulation Hash.

- `tests`: Pruebas para verificar la correctitud de las estructuras desarrolladas.
  - Tests de Cuckoo Hashing.
  - Tests de Bloom Filter.

### API

#### Hashes de tabulación

Todos los hashes de tabulación tienen los siguientes métodos públicos:

- `<Tipo>Hash(self, c: int = 4, r: int = 8, seed: int = None)`
  - `c`
    - Entero que representa el número de "chunks" o "trozos" a dividir el valor a hashear.
    - Por defecto se divide en 4 bits.
  - `r`
    - Entero que representa el número de bits que cada división en trozos posee.
    - Por defecto cada trozo tiene 8 bits o 1 byte.
    - Los valores por defecto aseguran que se hasheen valores de 32 bits o 4 bytes.
  - `seed`
    - La semilla aleatoria para generar los valores de las tablas.
    - Por defecto es `None`. Esto solo crea una semilla aleatoria.

- `hash(self, key: Union[int, bytes, str]) -> int`
  - `key`
    - El valor a hashear.
    - Puede ser un string, entero o bytes.
  - Retorna el hash de `key`.

#### Bloom Filter

- `BloomFilter(max_size: int, max_tolerance: float = 0.01, seed: int = None)`
  - `max_size`
    - Entero que representa el número máximo de elementos únicos recibidos.
    - Lanza `TypeError` si no es un entero positivo.
  - `max_tolerance`
    - Float que describe la tolerancia máxima a falsos positivos.
    - Por defecto `0.01` o 1%.
    - Lanza `TypeError` si no es un float entre 0 y 1.
  - `seed`
    - Entero usado como semilla de las funciones de hash.
    - Puede ser None, para lo cual se usa un entero aleatorio.
    - Lanza `TypeError` si no es None o entero.
  - Lanza `MemoryError` si la cantidad de bits requerida supera el millón.

- `add(self, value) -> "BloomFilter"`
  - Agrega el elemento `value` al Bloom Filter.
  - `value`
    - Puede ser `bytes`, `str`, `int` o cualquier objeto transformable a `bytes`.
    - Retorna la propia instancia `BloomFilter`

- `contains(self, value) -> bool`
  - Verifica si el elemento posiblemente se encuentre o no en la estructura.
  - `value`
    - Mismas entradas que `add()`.
    - Retorna un booleano.

- `size(self) -> int`
  - Retorna el número aproximado de elementos agregados.

- `max_remaining_capacity(self) -> int`
  - Retorna el máximo de elementos a agregar antes de alcanzar `max_size`.

- `false_positive_probability(self) -> float`
  - Retorna la probabilidad teórica de falsos positivos.

- `confidence(self) -> float`
  - Retorna `1 - false_positive_probability`.

#### Cuckoo Hashing

- `CuckooHashTable(size: int = 11, max_displacements: int = 10)`
  - `size`
    - Entero que representa el tamaño de la tabla hash.
    - Por defecto es 11.
    - Lanza `TypeError` si no es positivo.
  - `max_displacements`
    - Entero que representa el número máximo de desplazamientos al insertar antes de abortar.
    - Por defecto es 10.
    - Lanza `TypeError` si no es positivo.

- `insert(self, key: Union[int, str, bytes]) -> bool`
  - Inserta el elemento `key` en la estructura.
  - `key`
    - Clave a insertar.
    - Puede ser `int`, `str` o `bytes`.
    - Retorna un booleano que indica si la inserción fue exitosa o no.

      
