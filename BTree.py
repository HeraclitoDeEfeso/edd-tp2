
class Btree():

    def __init__(self, orden):
        self.orden = orden
             
    '''PROCEDURE B-TREE-SEARCH (x , k)
begin
i=1
while ( i <= n[x] and k > keyi[x] )
do ( i <- i + 1);
if ( i <= n[x] and k = keyi[x] )
then return (x, i)
if ( leaf[x] ) then return NIL;
else Disk-Read(ci[x])
return B-Tree-Search(ci[x], k);
end;'''

  ''' PROCEDURE B-TREE-INSERT(T, k)
begin
r = root[T]
if ( n[r] == 2t – 1){
s <- Allocate-Node()
root[T] = s
leaf[s] = FALSE
n[s] = 0
c1[s] = r
B-Tree-Split-Child(s, 1, r)
B-Tree-Insert-Nonfull(s, k)
} else
B-Tree-Insert-Nonfull(r, k)
end;'''

  
'''PROCEDURE B-TREE-SPLIT-CHILD (x, i, y)
begin
z = Allocate-Node()
leaf[z] = leaf[y]
n[z] = t - 1
for ( j = 1 to t – 1)
do keyj[z] = keyj+t[y]
if ( not leaf[y] ){
for ( j = 1 to t )
do cj[z] = cj+t[y]
}//end if
n[y] = t - 1
for( j = n[x] + 1 downto i + 1)'''
