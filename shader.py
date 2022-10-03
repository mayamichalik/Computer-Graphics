class shader:

    # Maya Michalik
    # April 9 2021
    # CS3388 asn 4
    # Helper method shadowed
    # input: object, I - intersection, S - vector to light source, object list
    # output: True if the ray intersects with an object from the scene, false if not

    def __shadowed(self,object,I,S,objectList):
        M = object.getT()
        #detatch intersection from its surface
        I = M*(I+0.001*S)
        # transform S to world coords
        S = M.__mul__(S)
        for obj in objectList:
            MI = obj.getT().inverse()
            # transform intersection point to generic coords
            I = MI*I
            # transforms vector to light source into generic coords
            S = (MI*S).normalize()
            if obj.minimumIntersection(I, S) != -1.0:
                return True
            return False

    #Constructor method
    # input: intersection, direction, camera, object list, light
    # output: computes shaded colour

    def __init__(self,intersection,direction,camera,objectList,light):
        for i in intersection:
            obj = objectList[i]
            t0 = obj.getT()
            M = t0.inverse()
            Ts = light.setPosition(M.getPosition())
            # transform ray
            te = M*camera
            td = M*direction
            I = te+td*t0
            # computes vetor from intersection point to light source
            S = Ts*I.__neg__
            N = obj.normalize()
            # specular reflection
            R = S.__neg__ + (S.__mul__(2).dotProduct(N)*N)
            # vector to center of projection
            V = (te-I).normalize()
            Id = max(N.dotProduct(S),0)
            Is = max(R.dotProduct(V),0)
            r = obj.getReflectance()
            c = obj.getColor()
            Li = light.getIntensoty()
            # if the intersection point is not shadowed by other objects
            if not __shadowed(obj, I, S, objectList):
                f = r[0]+r[1]*Id + (r[2]*Is)^r[3]
            else:
                f=r[0]
            self.__color = (f(c[0]*Li[0],c[1]*Li[1],c[2*Li[2]]))

    def getShade(self):
        return self.__color
