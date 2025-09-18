from itertools import product

# ==============================
# PROGRAMA DE CONJUNTOS Y CARDINALIDAD
# ==============================

def conjuntos_y_cardinalidad():
    print("\n PROGRAMA DE CONJUNTOS Y CARDINALIDAD \n")
    
    #a)extencion: consiste en listar explicitamente los elementos dentro de llaves.
    #Ejemplo:{1,2,3,4}
    #Ejercicio:
    A = set([1, 2, 3, 4])
    print("conjunto A:", A)

    # Método de verificación:
    def verificar_extencion(A, esperado):
        return A == esperado
    print(verificar_extencion(A, set([1, 2, 3, 4])))

    # Comprensión
    #Ejemplo:B=x∈N|x es par
    B = {x for x in range(1, 21) if x % 2 == 0}
    print("conjunto B:", B)

    esperado = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20}
    print(B == esperado)

    #Cardinalidad:la cardinalidad de un conjunto es el numero de elementos que contiene.
    #Ejemplo: A=1,2,3,4, entonces|A|=4.
    #Ejercicio:
    A = {1, 2, 3, 4}
    print("cardinalidad de A:", len(A))

    def verificar_cardinalidad(A, esperado):
        return len(A) == esperado
    print(verificar_cardinalidad(A, 4))

    #conjuntos infinitos(Simulacion con cortes finitos):un conjunto infinito no se puede escribir por completo,pero se simula con un rango limitado.
    #Ejemplo:
    N100 = {x for x in range(1, 101)}
    print("primeros 100 numeros naturales: ", N100)
    print("Cardinalidad:", len(N100))
    print("Verifica si el tamaño es 100:", len(N100) == 100)
    
    #Ejercicio:
    N500 = {x for x in range(1, 501)}
    print("Primeros 500 numeros naturales:", N500)
    print("cardinalidad:", len(N500))
    print("Verifica si el tamaño es 500:", len(N500) == 500)

    # Operaciones con conjuntos
    A = {1, 2, 3}
    B = {3, 4, 5}
    
    #Union:
    union = A.union(B)
    print("union:", union)
    print("verifica la Union:", union == {1, 2, 3, 4, 5})
    
    # Interseccion
    interseccion = A.intersection(B)
    print("Intersección:", interseccion)
    print("Verifica la interseccion:", interseccion == {3})
    
    #diferencia:
    diferencia = A.difference(B)
    print("Diferencia A-B:", diferencia)
    print("Verifica la diferencia A - B:", diferencia == {1, 2})
    
    #Diferencia Simetrica:
    diferencia_simetrica = A.symmetric_difference(B)
    print("Diferencia simetrica:", diferencia_simetrica)
    print("Verifica la diferencia simetrica:", diferencia_simetrica == {1, 2, 4, 5})

    #Complemento
    #si el universo U esta definido,el complemento es:
    #A elevado c es igual a U-A
    U = {1, 2, 3, 4, 5}
    complemento = U.difference(A)
    print("complemento de A en U:", complemento)

    #producto cartesiano
    #AxB={(a,b)|a∈A,b∈B}
    A = {1, 2}
    B = {3, 4}
    producto = {(a, b) for a in A for b in B}
    print("producto cartesiano:", producto)
    print("Verifica cardinalidad producto cartesiano:", len(producto) == len(A) * len(B))

    print("\n--- Final del programa de carnalidad  ---\n")


# =====================================
# Programa de la relaciones y funciones 
# =====================================

def relaciones_y_funciones():
    print("\n Programa de la relaciones y funciones  \n")

    def reflexiva(A, R):
        return all((a, a) in R for a in A)

    def simetrica(R):
        return all((b, a) in R for (a, b) in R)

    def antisimetrica(R):
        return all(a == b or (b, a) not in R for (a, b) in R)

    def transitiva(R):
        return all(((a, c) in R) for (a, b) in R for (x, c) in R if b == x)

    def equivalencia(A, R):
        return reflexiva(A, R) and simetrica(R) and transitiva(R)

    def orden(A, R):
        return reflexiva(A, R) and antisimetrica(R) and transitiva(R)

    def inyectiva(f, A, B):
        imagen = [f(a) for a in A]
        return len(imagen) == len(set(imagen))

    def sobreyectiva(f, A, B):
        imagen = set(f(a) for a in A)
        return imagen == set(B)

    def biyectiva(f, A, B):
        return inyectiva(f, A, B) and sobreyectiva(f, A, B)

    def clausura_reflexiva(A, R):
        return R.union({(a, a) for a in A})

    def clausura_simetrica(R):
        return R.union({(b, a) for (a, b) in R})

    def clausura_transitiva(R):
        clausura = set(R)
        cambio = True
        while cambio:
            cambio = False
            nuevos_pares = {(a, c) for (a, b) in clausura for (x, c) in clausura if b == x}
            if not nuevos_pares.issubset(clausura):
                clausura.update(nuevos_pares)
                cambio = True
        return clausura

    def clausura_equivalencia(A, R):
        return clausura_transitiva(clausura_simetrica(clausura_reflexiva(A, R)))

    # Datos iniciales
    A = {1, 2, 3}
    R = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)}

    while True:
        print("\n--- Opciones Relaciones y Funciones ---")
        print("1. Verificar propiedades de la relacion")
        print("2. Verificar propiedades de la funcion")
        print("3. Calcular clausuras de la relacion")
        print("4. Cambiar conjunto y relacion")
        print("0. Volver al menu principal")
        op = input("Elige una opción: ")

        if op == "1":
            print("\n--- Propiedades de la relación ---")
            print(f"Conjunto A = {A}")
            print(f"Relación R = {R}")
            print(f" Reflexiva: {reflexiva(A, R)}")
            print(f" Simetrica: {simetrica(R)}")
            print(f" Antisimetrica: {antisimetrica(R)}")
            print(f" Transitiva: {transitiva(R)}")
            print(f" Equivalencia: {equivalencia(A, R)}")
            print(f" Orden: {orden(A, R)}")

        elif op == "2":
            print("\n--- FUNCIONES ---")
            f1 = lambda x: 2 * x
            B1 = {2, 4, 6}
            print(f"Función f(x)=2x del conjunto {A} a {B1}")
            print(f" Inyectiva: {inyectiva(f1, A, B1)}")
            print(f" Sobreyectiva: {sobreyectiva(f1, A, B1)}")
            print(f" Biyectiva: {biyectiva(f1, A, B1)}")

        elif op == "3":
            print("\n--- CLAUSURAS ---")
            print(f"Clausura reflexiva: {clausura_reflexiva(A, R)}")
            print(f"Clausura simétrica: {clausura_simetrica(R)}")
            print(f"Clausura transitiva: {clausura_transitiva(R)}")
            print(f"Clausura de equivalencia: {clausura_equivalencia(A, R)}")

        elif op == "4":
            try:
                A_str = input("Conjunto A: ")
                R_str = input("Relación R: ")
                A = eval(A_str)
                R = eval(R_str)
                print("Conjunto y relacion actualizados.")
            except (SyntaxError, NameError) as e:
                print("Error en el formato:", e)

        elif op == "0":
            break
        else:
            print("Opcion no valida.")

# ==============================
# Menu general
# ==============================

def menu_general():
    while True:
        print("\n=== Menu general ===")
        print("1. Conjuntos y Cardinalidad")
        print("2. Relaciones y Funciones")
        print("0. Salir")
        op = input("Elige una opción: ")

        if op == "1":
            conjuntos_y_cardinalidad()
        elif op == "2":
            relaciones_y_funciones()
        elif op == "0":
            print("Fin del programa.")
            break
        else:
            print("Opcion no valida.")


# Ejecutar programa
menu_general()