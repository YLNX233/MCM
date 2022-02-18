# Floyd

```cpp
llint dist[MAXN][MAXN];
memset(dist, 0x3f, sizeof(dist));
for (int i = 1; i <= n; i++)	dist[i][i] = 0;

void Floyd()
{
	for (auto i : nod)
	{
		for (auto e : i.second.e)
		{
			dist[e.u][e.v] = min(dist[e.u][e.v], e.w);
		}
	}
	for (int t = 1; t <= n; t++)
	{
		for (int x = 1; x <= n; x++)
		{
			for (int y = 1; y <= n; y++)
			{
				//符合状态转移的思想
				dist[x][y] = min(dist[x][y], dist[x][t] + dist[t][y]);
			}
		}
	}
}
```