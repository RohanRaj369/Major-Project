#pragma GCC optimize("Ofast")
#pragma GCC optimize("unroll-loops")
#pragma GCC optimize("inline")
#include<bits/stdc++.h>
using namespace std;
void*wmem;
char memarr[96000000];
template<class S, class T> inline S chmax(S &a, T b){
  if(a<b){
    a=b;
  }
  return a;
}
template<class T> inline void walloc1d(T **arr, int x, void **mem = &wmem){
  static int skip[16] = {0, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
  (*mem) = (void*)( ((char*)(*mem)) + skip[((unsigned long long)(*mem)) & 15] );
  (*arr)=(T*)(*mem);
  (*mem)=((*arr)+x);
}
template<class T> inline void walloc1d(T **arr, int x1, int x2, void **mem = &wmem){
  walloc1d(arr, x2-x1, mem);
  (*arr) -= x1;
}
struct graph{
  int N;
  int*es;
  int**edge;
  void setEdge(int N__, int M, int A[], int B[], void **mem = &wmem){
    int i;
    N = N__;
    walloc1d(&es, N, mem);
    walloc1d(&edge, N, mem);
    for(i=(0);i<(N);i++){
      es[i] = 0;
    }
    for(i=(0);i<(M);i++){
      es[A[i]]++;
      es[B[i]]++;
    }
    for(i=(0);i<(N);i++){
      walloc1d(&edge[i], es[i], mem);
    }
    for(i=(0);i<(N);i++){
      es[i] = 0;
    }
    for(i=(0);i<(M);i++){
      edge[A[i]][es[A[i]]++] = B[i];
      edge[B[i]][es[B[i]]++] = A[i];
    }
  }
  void getDist(int root, int res[], void *mem = wmem){
    int i;
    int j;
    int k;
    int*q;
    int s;
    int z;
    walloc1d(&q, N, &mem);
    for(i=(0);i<(N);i++){
      res[i]=-1;
    }
    res[root]=0;
    s=0;
    z=1;
    q[0]=root;
    while(z){
      i=q[s++];
      z--;
      for(j=(0);j<(es[i]);j++){
        k=edge[i][j];
        if(res[k]>=0){
          continue;
        }
        res[k]=res[i]+1;
        q[s+z++]=k;
      }
    }
  }
  int getDist(int a, int b, void *mem = wmem){
    int i;
    int j;
    int k;
    int*q;
    int s;
    int z;
    int*d;
    if(a==b){
      return 0;
    }
    walloc1d(&d, N, &mem);
    walloc1d(&q, N, &mem);
    for(i=(0);i<(N);i++){
      d[i] = -1;
    }
    d[a] = 0;
    s = 0;
    z = 1;
    q[0] = a;
    while(z){
      i = q[s++];
      z--;
      for(j=(0);j<(es[i]);j++){
        k = edge[i][j];
        if(d[k] >= 0){
          continue;
        }
        d[k] = d[i] + 1;
        if(k==b){
          return d[k];
        }
        q[s+z++] = k;
      }
    }
    return -1;
  }
}
;
template<class T, class S> inline int vec2arr(vector<T> &v, S arr[]){
  int i;
  int N = v.size();
  for(i=(0);i<(N);i++){
    arr[i] = v[i];
  }
  return N;
}
template<class T, class S1, class S2> inline int vec2arr(vector<vector<T>> &v, S1 arr1[], S2 arr2[]){
  int i;
  int N = v.size();
  for(i=(0);i<(N);i++){
    arr1[i] = v[i][0];
    arr2[i] = v[i][1];
  }
  return N;
}
template<class T, class S1, class S2, class S3> inline int vec2arr(vector<vector<T>> &v, S1 arr1[], S2 arr2[], S3 arr3[]){
  int i;
  int N = v.size();
  for(i=(0);i<(N);i++){
    arr1[i] = v[i][0];
    arr2[i] = v[i][1];
    arr3[i] = v[i][2];
  }
  return N;
}
#define main dummy_main
int main(){
  wmem = memarr;
  return 0;
}
#undef main
class Solution{
  public:
  vector<int> maxTargetNodes(vector<vector<int>>& edges1, vector<vector<int>>& edges2){
    dummy_main();
    int i;
    int j;
    int N = edges1.size()+1;
    int M = edges2.size() + 1;
    static int a[1000000];
    static int b[1000000];
    static int d[1000000];
    static int dd1;
    static int dd2;
    graph g1;
    graph g2;
    vector<int> res;
    vec2arr(edges1, a, b);
    g1.setEdge(N, N-1, a, b);
    vec2arr(edges2, a, b);
    g2.setEdge(M, M-1, a, b);
    dd1 = dd2 = 0;
    g2.getDist(0,d);
    for(i=(0);i<(M);i++){
      if(d[i]%2==0){
        dd2++;
      }
    }
    chmax(dd2, M-dd2);
    g1.getDist(0,d);
    for(i=(0);i<(N);i++){
      if(d[i]%2==0){
        dd1++;
      }
    }
    for(i=(0);i<(N);i++){
      if(d[i]%2==0){
        res.push_back(dd1 + dd2);
      }
      if(d[i]%2==1){
        res.push_back(N-dd1 + dd2);
      }
    }
    return res;
  }
}
;
// cLay version 20241019-1

// --- original code ---
// #define main dummy_main
// {}
// #undef main
// 
// class Solution {
// public:
//   vector<int> maxTargetNodes(vector<vector<int>>& edges1, vector<vector<int>>& edges2) {
//     dummy_main();
//     int i, j;
//     int N = edges1.size()+1, M = edges2.size() + 1;
//     static int a[1d6], b[1d6];
//     static int d[1d6], dd1, dd2;
//     graph g1, g2;
//     VI res;
// 
//     vec2arr(edges1, a, b);
//     g1.setEdge(N, N-1, a, b);
//     vec2arr(edges2, a, b);
//     g2.setEdge(M, M-1, a, b);
// 
//     dd1 = dd2 = 0;
// 
//     g2.getDist(0,d);
//     rep(i,M) if(d[i]%2==0) dd2++;
//     dd2 >?= M-dd2;
// 
//     g1.getDist(0,d);
//     rep(i,N) if(d[i]%2==0) dd1++;
// 
//     rep(i,N){
//       if(d[i]%2==0) res.push_back(dd1 + dd2);
//       if(d[i]%2==1) res.push_back(N-dd1 + dd2);
//     }
// 
//     return res;
//   }
// };