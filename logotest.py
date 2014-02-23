#!/usr/bin/env py

import bpy
import bmesh
import math

class Tetrahedron:
    sqrt3 = 1.7320508075688772
    sin30ds3 = 0.28867513459481287
    a = 0
    b = (2*math.pi)/3
    c = (4*math.pi)/3

    def __init__(self, x, y, z, length, theta):
        self.x = x
        self.y = y
        self.z = z
        self.length = length
        # Create mesh 
        me = bpy.data.meshes.new('myMesh') 
        # Create object
        ob = bpy.data.objects.new('myObject', me) 
        #ob.location = origin
        ob.show_name = True
        # Link object to scene
        bpy.context.scene.objects.link(ob)
        # Get a BMesh representation
        bm = bmesh.new() # create an empty BMesh
        bm.from_mesh(me) # fill it in from a Mesh

        vert_d = bm.verts.new( (x, y, z) )
        vert_a = bm.verts.new( get_vert((x, y, z), length, theta, a) )
        vert_b = bm.verts.new( get_vert((x, y, z), length, theta, b) )
        vert_c = bm.verts.new( get_vert((x, y, z), length, theta, c) )

        bm.verts.index_update()

        bm.faces.new( (vert_a, vert_b, vert_c) )
        bm.faces.new( (vert_a, vert_b, vert_d) )
        bm.faces.new( (vert_b, vert_c, vert_d) )
        bm.faces.new( (vert_c, vert_a, vert_d) )

        bm.to_mesh(me)

    def get_vert(point, length, theta, offset):
        (x1, y1, z1) = point
        x2 = x1 + (math.cos(offset + theta) * length)
        y2 = y1 + (math.sin(offset + theta) * length)
        z2 = z1 - ((1/sqrt3) * length)
        return (x2, y2, z2)

t = Tetrahedron(0,0,0,1,0)
