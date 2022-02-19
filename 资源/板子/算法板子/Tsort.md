# 拓扑排序

答案存储在ans中，ans_i记录排出的节点个数

若答案个数与n不相等则有环

```cpp
int count = 0;
int Topo_node[MAXN],ans[MAXN],ans_i=0;
void Topological_Sort_max()
{
	//《序号，拓扑序》
	priority_queue<int
 indeg_0;
	int* ans = new int[n + 1]; int ans_i = 0;
	//这里决定优先输出编号大的节点
	for (int i = 0;i<nod.size();i++)
	{
        it = nod[i];
		int i = it.first;
		Topo_node[i] = nod[i].in_deg;
		if (nod[i].in_deg == 0)	indeg_0.push(i);
	}
	while (!indeg_0.empty())
	{
		node p = nod[indeg_0.top()];
		ans[ans_i++] = indeg_0.top();
		indeg_0.pop();
		
		for (int i=0;i<p.e.size();i++)
		{
            e = p.e[i]
			if (--Topo_node[e.v] == 0)
			{
				count++;
				indeg_0.push(e.v);
			}

		}
	}
}
```