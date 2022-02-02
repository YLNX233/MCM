# 快排求第k大

```cpp
int kth(int k[], int l, int r,int th)
{
	int i, last;
	if (l < r) {
		last = l;
		for (i = l + 1; i <= r; i++)
			if (k[i] < k[l])
			{
				last++;
				swap(k[last],k[i])
			}
		swap(k[last],k[l])
        if(last == th)   return k[last];
        else if(last>th) return kth(k, l, last - 1,th);
		else return kth(k, last + 1, r,th);
	}
	return k[l];
}
```