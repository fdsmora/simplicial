def testComplex(complex):
    print '......................'
    for s in complex:
        p0 = s[0]
        p1 = s[1]
        print '\nVistas:'
        print 'p0.view={}\np1.view={}'.format(p0.view,p1.view)

def testMerge(d):
    for k in d:
        s = '';
        for v in d[k]:  
            s += ' ' + str(v) 
        print '{}:[{}]\n'.format(k,s)

def testAssignColors(c):
    for k in c:
        s = '';
        for v in c[k]:  
            s += ' ' + str(v) 
        print '{}:[{}]\n'.format(k,s)