def testComplex(complex):
    print ('......................')
    for s in complex:
        p0 = s[0]
        p1 = s[1]
        print ('\nVistas:')
        print ('p0.view={}\np1.view={}'.format(p0.view,p1.view))


def testEdges(edges):
    print ('test edges')
    for e in edges:
        print(e)

def testDict(d):
    for k in d:
        print ("{}:{}".format(k,d[k]))
