from packagetree import Package,PackageDirectory,PackageFile
import shutil
if __name__ == '__main__':
    a = PackageDirectory('a')
    b = PackageDirectory('b')
    c= PackageDirectory('c')
    d= PackageDirectory('d')
    binit = PackageFile('__init__')
    dinit = PackageFile('__init__')
    cinit = PackageFile('__init__')
    a.add(b)
    a.add(c)
    b.add(d)
    b.add(binit)
    c.add(cinit)
    d.add(dinit)
    my_package = Package('my_package')
    my_package.add(a)
    package_bytes = my_package.to_zip()
    print(package_bytes)
    shutil.rmtree('outputs/teste', ignore_errors=True)
    