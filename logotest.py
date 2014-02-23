#!/usr/bin/env python

import bpy
import bmesh
import math

class Tetrahedron:
    sqrt3 = 1.7320508075688772
    sin30ds3 = 0.28867513459481287
    sqrt6d3 = 0.8164965809277259
    height = 0.8660254037844386
    a = 0
    b = (2*math.pi)/3
    c = (4*math.pi)/3

    def __init__(self, x, y, z, length, theta):
        self.x = x
        self.y = y
        self.z = z
        self.length = length
        self.theta = theta

    def draw():
        # Create mesh 
        me = bpy.data.meshes.new('mesh') 
        # Create object
        ob = bpy.data.objects.new('tetrahedron', me) 
        #ob.location = origin
        ob.show_name = True
        # Link object to scene
        bpy.context.scene.objects.link(ob)
        # Get a BMesh representation
        bm = bmesh.new() # create an empty BMesh
        bm.from_mesh(me) # fill it in from a Mesh
        x = self.x
        y = self.y
        z = self.z
        length = self.length
        theta = self.theta

        vert_d = bm.verts.new( (x, y, z) )

        vert_a = bm.verts.new( \
            self.get_vert((x, y, z), length, theta, self.a) )

        vert_b = bm.verts.new( \
            self.get_vert((x, y, z), length, theta, self.b) )

        vert_c = bm.verts.new( \
            self.get_vert((x, y, z), length, theta, self.c) )

        bm.verts.index_update()

        bm.faces.new( (vert_a, vert_b, vert_c) )
        bm.faces.new( (vert_a, vert_b, vert_d) )
        bm.faces.new( (vert_b, vert_c, vert_d) )
        bm.faces.new( (vert_c, vert_a, vert_d) )

        bm.to_mesh(me)

    @staticmethod
    def get_vert(point, length, theta, offset):
        (x1, y1, z1) = point
        x2 = x1 + (math.cos(offset + theta) * length)
        y2 = y1 + (math.sin(offset + theta) * length)
        z2 = z1 - (Tetrahedron.sqrt3 * Tetrahedron.height * length)
        return (x2, y2, z2)

def get_tetra(tetra, length, offset):
    (x, y, z) = Tetrahedron.get_vert( \
        (tetra.x, tetra.y, tetra.z), \
        length, tetra.theta, offset)
    return Tetrahedron(x, y, z, length, tetra.theta)

def quad(tetra):
    tet_list = []
    tet_list.append(Tetrahedron(tetra.x, tetra.y, tetra.z, tetra.length/4, tetra.theta))
    tet_list.append(get_tetra(tetra, tetra.length/4, 0))
    tet_list.append(get_tetra(tetra, tetra.length/4, Tetrahedron.b))
    tet_list.append(get_tetra(tetra, tetra.length/4, Tetrahedron.c))
    return tet_list

def iterate(tetra, tetra_list, count):
    if count == 0:
        return tetra_list.append( \
            Tetrahedron(tetra.x, tetra.y, tetra.z, tetra.length, tetra.theta))
    else:
        tetra_list.extend(quad(tetra))
        [tetra_list.append(n) for n in iterate(get_tetra(tetra, tetra.length/2, 0), tetra_list, count - 1)]
        [tetra_list.append(n) for n in iterate(get_tetra(tetra, tetra.length/2, Tetrahedron.b), tetra_list, count - 1)]
        [tetra_list.append(n) for n in iterate(get_tetra(tetra, tetra.length/2, Tetrahedron.c), tetra_list, count - 1)]
        return tetra_list

t = Tetrahedron(0,0,0,100,0)
l = []
tetra_list = iterate(t, l, 1)

for tetra in tet_list:
    tetra.draw()
