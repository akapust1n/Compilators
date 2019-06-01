int main()
{
	int a, b;
	a = 1;
	b = a-1;
	while (b != 0)
		if (a > b)
			a = a - b;
		  else
			b = b - a;
	return a;
}
