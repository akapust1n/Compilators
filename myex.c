int main()
{
    int n;
	int	i;
	int	j;
    n = 5;
    int a[5];
    a[0] = 1;
    a[1] = 2;
    a[2] = 3;
    a[3] = 4;
    a[4] = 6;

    for (i = 0; i < n - 1; i = i + 1)
    {
        for (j = 0; j < n - i - 1; j = j + 1)
        {
			int j1 = j + 1;
            if (a[j] > a[j1])
            {
                int tmp = a[j];
                a[j] = a[j1];
                a[j1] = tmp;
            }
        }
    }
    return 0;
}