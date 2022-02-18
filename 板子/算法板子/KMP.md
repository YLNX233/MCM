# π函数和kmp

求得pi函数

pi函数表示以i为长度的子串最长相等真前后缀的长度

```cpp
int pi[MAXN];
char s[MAXN];

void get_pi()
{
	int len = strlen(s);
	for(int l=1;l<len;l++)
	{
		int j = pi[l-1];
		while(s[l]!=s[j] && j
0)
		{
			j = pi[j-1];
		}
		if(s[l]==s[j])
		{
			j++;			
		}
		pi[l] = j;
	}
}
```

KMP算法朴素的实现就是在 目标串+‘#’+源串的字符串上求pi函数，
位点pi = len(t)就是在源串中出现t的末尾

```cpp
vector<int
 ans;
void KMP()
{
	int lens = strlen(s);
	int lent = strlen(t);
	t[lent] ='*';
	strcat(t,s);
	//cout<<t;
	get_pi(t);
	
	int tmax = strlen(t);
	
	for(int i=lent-1;i<lens;i++)
	{
		if(i+lent+1 
= tmax) break;
		if(pi[i+lent+1] == lent)
		{
			ans.push_back(i-lent+1);
		}
	}
}

```