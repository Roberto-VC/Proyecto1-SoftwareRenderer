from pickle import NONE
from vector import *
from gl import *
from texture import *
import random


def bounding_box(A, B, C):
    # Mira cual es la bounding box
    xs = [A.x, B.x, C.x]
    ys = [A.y, B.y, C.y]

    xs.sort()
    ys.sort()

    return xs[0], xs[-1], ys[0], ys[-1]


def cross(V1, V2):
    # Producto cruz
    return (
        V1.y * V2.z - V1.z * V2.y,
        V1.z * V2.x - V1.x * V2.z,
        V1.x * V2.y - V1.y * V2.x,
    )


def barycentric(A, B, C, P):
    # Se calculan las baricentricas
    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x), V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )

    u = cx / cz
    v = cy / cz
    w = 1 - (cx + cy) / cz

    return (w, v, u)


print()


def main():

    d = 0
    side = 1000
    b = Bitmap(side, side)
    print("Bienvenido al renderizador!\n")
    """while True:
        print("1. Renderizar sin textura")
        print("2. Renderizar con textura")
        g = int(input())
        if g == 2:
            
            break
        elif g == 1:
            break
        else:
            print("Opción  no válida")
            continue"""
    nombre = "Pokemon.bmp"
    b.lookAt(V3(0, 10, 20), V3(0, 0, 0), V3(0, 10, 0))
    """while True:
        print("¿Como quiere que sea la foto a tomar?")
        print("1. Medium Shot\n2. Low Angle\n3. High Angle\n4. Dutch Angle")
        angle = int(input())
        if angle == 1:
            b.lookAt(V3(0, 0, 20), V3(0, 0, 0), V3(0, 10, 0))
            nombre = "Medium.bmp"
            break
        elif angle == 2:
            b.lookAt(V3(0, -10, 20), V3(0, 0, 0), V3(0, 10, 0))
            nombre = "Low.bmp"
            break
        elif angle == 3:
            b.lookAt(V3(0, 10, 20), V3(0, 0, 0), V3(0, 10, 0))
            nombre = "High.bmp"
            break
        elif angle == 4:
            roation_factor = (0, 0, pi / 6)
            scale_factor = (0.4, 0.4, 0.4)
            transform_factor = (0.25, -0.3, 0)
            b.lookAt(V3(0, 0, 20), V3(0, 0, 0), V3(0, 10, 0))
            nombre = "Dutch.bmp"
            break
        else:
            print("Opción  no válida")
            continue"""

    b.clearColor(200, 0, 225)

    # Todos los shaders
    def shader(render, **kwargs):
        w, v, u = kwargs["bar"]
        A, B, C = kwargs["vertices"]
        if b._texture:
            tA, tB, tC = kwargs["texture_coords"]
        nA, nB, nC = kwargs["normals"]
        L = V3(0, 0, 1)
        iA = nA.normalize() @ L.normalize()
        iB = nB.normalize() @ L.normalize()
        iC = nC.normalize() @ L.normalize()

        i = iA * w + iB * u + iC * v

        if b._texture:
            tx = tA.x * w + tB.x * u + tC.x * v
            ty = tA.y * w + tB.y * u + tC.y * v
            return t.getColori(tx, ty, i)

    def pokeball(render, **kwargs):
        w, v, u = kwargs["bar"]
        A, B, C = kwargs["vertices"]
        y = kwargs["aaa"]
        x = kwargs["bbb"]
        nA, nB, nC = kwargs["normals"]
        L = V3(0, 0, 1)
        iA = nA.normalize() @ L.normalize()
        iB = nB.normalize() @ L.normalize()
        iC = nC.normalize() @ L.normalize()

        i = iA * w + iB * u + iC * v
        if y < (565):
            return (int(255 * i), int(255 * i), int(255 * i))
        elif y < (575):
            return (0, 0, 0)
        elif y < (615):
            return (0, 0, int(255 * i))
        else:
            return (75, 105, 246)

    def grass(render, **kwargs):
        w, v, u = kwargs["bar"]
        A, B, C = kwargs["vertices"]
        y = kwargs["aaa"]
        x = kwargs["bbb"]

        m = random.randint(0, 10)
        if m == 10:
            return (20, 100, 0)
        return (0, 125, 0)

    def bush(render, **kwargs):
        w, v, u = kwargs["bar"]
        A, B, C = kwargs["vertices"]
        y = kwargs["aaa"]
        x = kwargs["bbb"]

        m = random.randint(0, 50)
        if m == 50:
            return (0, 20, 255)
        return (43, 100, 0)

    def tree(render, **kwargs):
        w, v, u = kwargs["bar"]
        A, B, C = kwargs["vertices"]
        y = kwargs["aaa"]
        x = kwargs["bbb"]

        if y < (615):
            m = random.randint(0, 50)
            if m == 50:
                return
            return (0, 56, 111)
        else:
            m = random.randint(0, 50)
            if m == 50:
                return (32, 111, 0)
            return (0, 154, 26)

    def transform_vertex(vertex):
        # Transforma el vertice
        augmented_vertex = Matrix([[vertex[0]], [vertex[1]], [vertex[2]], [1]])
        transformed_vertex = (
            b.Viewport * b.Projection * b.View * b.Model * augmented_vertex
        )

        transformed_vertex = V3(
            transformed_vertex.List[0][0],
            transformed_vertex.List[1][0],
            transformed_vertex.List[2][0],
            transformed_vertex.List[3][0],
        )
        return V3(
            transformed_vertex.x / transformed_vertex.w,
            transformed_vertex.y / transformed_vertex.w,
            transformed_vertex.z / transformed_vertex.w,
        )

    print()

    def triangle(A, B, C, verticest=[], verticesn=[]):

        # "Se crea la normal del triangulo para sacar la intensidad")

        # Escalas de grises y se crea el bounding box
        p, q, r, s = bounding_box(A, B, C)
        for x in range(round(p), round(q) + 1):
            for y in range(round(r), round(s) + 1):
                # Mira las baricentras del bounding
                try:
                    w, v, u = barycentric(A, B, C, V3(x, y))
                except:
                    continue
                if w < 0 or v < 0 or u < 0:
                    continue
                z = A.z * w + B.z * v + C.z * u
                # "Usa el z bugger para mostrar que esta adelante o atras"
                if (
                    x >= 0
                    and y >= 0
                    and x < len(b._zbuffer)
                    and y < len(b._zbuffer[0])
                    and b._zbuffer[x][y] < z
                ):
                    b._zbuffer[x][y] = z
                    # Hay un atributo vació del método en caso que no haya textura.

                    if b.active_shader and len(verticesn) == 3 and b._texture:
                        b._color = b.active_shader(
                            b,
                            aaa=y,
                            bbb=x,
                            bar=(w, v, u),
                            vertices=(A, B, C),
                            texture_coords=(verticest[0], verticest[1], verticest[2]),
                            normals=(verticesn[0], verticesn[1], verticesn[2]),
                        )
                    else:
                        b._color = b.active_shader(
                            b,
                            aaa=y,
                            bbb=x,
                            bar=(w, v, u),
                            vertices=(A, B, C),
                        )
                    # "En vez de escalas de grises, utiliza los colores de la textura")
                    # "Se pinta el punto"
                    if b._color == None:
                        continue
                    b.Vertex(x, y)

    def load_model(zubat, transform_factor, scale_factor, roation_factor):
        b.loadModelMatrix(transform_factor, scale_factor, roation_factor)
        vertext = []
        vertextt = []
        vertexn = []
        vertexnn = []
        d = 0
        for face in zubat.faces:
            d = d + 1
            # Mira los poligonos y cuantos veritces tiene
            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                # Se obtienen los vertices de la figura y los transforma.
                v1 = transform_vertex(zubat.vertices[f1])
                v2 = transform_vertex(zubat.vertices[f2])
                v3 = transform_vertex(zubat.vertices[f3])
                v4 = transform_vertex(zubat.vertices[f4])

                # Si hay texuta. Saca de la textura las caras y vertices respectivos
                if b._texture:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1
                    ft4 = face[3][1] - 1

                    vt1 = V3(
                        zubat.tvertices[ft1][0] * t.width,
                        zubat.tvertices[ft1][1] * t.height,
                    )
                    vt2 = V3(
                        zubat.tvertices[ft2][0] * t.width,
                        zubat.tvertices[ft2][1] * t.height,
                    )
                    vt3 = V3(
                        zubat.tvertices[ft3][0] * t.width,
                        zubat.tvertices[ft3][1] * t.height,
                    )
                    vt4 = V3(
                        zubat.tvertices[ft4][0] * t.width,
                        zubat.tvertices[ft4][1] * t.height,
                    )
                    vertext = [vt1, vt2, vt3]
                    vertextt = [vt1, vt4, vt3]
                if len(face[0]) == 3:
                    fn1 = face[0][2] - 1
                    fn2 = face[1][2] - 1
                    fn3 = face[2][2] - 1
                    fn4 = face[3][2] - 1
                    vn1 = V3(
                        zubat.nvertices[fn1][0],
                        zubat.nvertices[fn1][1],
                        zubat.nvertices[fn1][2],
                    )
                    vn2 = V3(
                        zubat.nvertices[fn2][0],
                        zubat.nvertices[fn2][1],
                        zubat.nvertices[fn2][2],
                    )
                    vn3 = V3(
                        zubat.nvertices[fn3][0],
                        zubat.nvertices[fn3][1],
                        zubat.nvertices[fn3][2],
                    )
                    vn4 = V3(
                        zubat.nvertices[fn4][0],
                        zubat.nvertices[fn4][1],
                        zubat.nvertices[fn4][2],
                    )

                    vertexn = [vn1, vn2, vn3]
                    vertexnn = [vn1, vn4, vn3]
                    # Para los los de cuatro poligonos, utiliza don traingulos
                triangle(
                    V3(v1.x, v1.y, v1.z),
                    V3(v2.x, v2.y, v2.z),
                    V3(v3.x, v3.y, v3.z),
                    vertext,
                    vertexn,
                )
                triangle(
                    V3(v1.x, v1.y, v1.z),
                    V3(v4.x, v4.y, v4.z),
                    V3(v3.x, v3.y, v3.z),
                    vertextt,
                    vertexnn,
                )
            else:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                # Se obtienen los vertices de la figura y los transforma.
                v1 = transform_vertex(zubat.vertices[f1])
                v2 = transform_vertex(zubat.vertices[f2])
                v3 = transform_vertex(zubat.vertices[f3])

                # Si hay texuta. Saca de la textura las caras y vertices respectivos
                if b._texture:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1

                    vt1 = V3(
                        zubat.tvertices[ft1][0] * t.width,
                        zubat.tvertices[ft1][1] * t.height,
                    )
                    vt2 = V3(
                        zubat.tvertices[ft2][0] * t.width,
                        zubat.tvertices[ft2][1] * t.height,
                    )
                    vt3 = V3(
                        zubat.tvertices[ft3][0] * t.width,
                        zubat.tvertices[ft3][1] * t.height,
                    )
                    vertext = [vt1, vt2, vt3]

                if len(face[0]) == 3:
                    fn1 = face[0][2] - 1
                    fn2 = face[1][2] - 1
                    fn3 = face[2][2] - 1
                    vn1 = V3(
                        zubat.nvertices[fn1][0],
                        zubat.nvertices[fn1][1],
                        zubat.nvertices[fn1][2],
                    )
                    vn2 = V3(
                        zubat.nvertices[fn2][0],
                        zubat.nvertices[fn2][1],
                        zubat.nvertices[fn2][2],
                    )
                    vn3 = V3(
                        zubat.nvertices[fn3][0],
                        zubat.nvertices[fn3][1],
                        zubat.nvertices[fn3][2],
                    )

                    vertexn = [vn1, vn2, vn3]
                    # Para los los de cuatro poligonos, utiliza don traingulos
                triangle(
                    V3(v1.x, v1.y, v1.z),
                    V3(v2.x, v2.y, v2.z),
                    V3(v3.x, v3.y, v3.z),
                    vertext,
                    vertexn,
                )

    Zubat = Obj("Leaf.obj")
    t = Texture("Leaf.bmp")
    b._texture = t
    b.active_shader = shader
    load_model(Zubat, (-0.60, -0.10, 0), (0.65, 0.65, 0.65), (0, 5 * pi / 4, 0))
    t = Texture("Ivysaur.bmp")
    b._texture = t
    load_model(Obj("Ivysaur.obj"), (-0.2, -0.25, 0), (0.25, 0.25, 0.25), (0, pi / 4, 0))
    t = Texture("Zubat.bmp")
    b._texture = t
    load_model(Obj("Zubat.obj"), (0.5, 0.5, 0), (0.075, 0.075, 0.075), (0, pi / 4, 0))
    b.active_shader = pokeball
    load_model(Obj("sphere.obj"), (0.2, 0.6, 0), (0.10, 0.10, 0.10), (0, 3 * pi / 4, 0))
    b._texture = None
    b.active_shader = grass
    load_model(Obj("Cube.obj"), (0.0, -2.5, -5), (0.85, 0.01, 0.85), (0, 3 * pi / 4, 0))
    b.active_shader = bush
    load_model(Obj("Bush.obj"), (0.65, -1.00, -2), (0.3, 0.3, 0.3), (0, pi / 4, 0))
    b.active_shader = tree
    load_model(Obj("Tree.obj"), (0, -1.5, -4), (0.3, 0.3, 0.3), (0, 0, 0))
    b.write(nombre)


if __name__ == "__main__":
    main()
