public class MethodaCall{
		
	public static int mult1(int a, int b){
		return a*b;
	}

	public static int add1(int a, int b){
		int z;
		z = mult1(a, b);
		return z + a + b;
	}
	
	public static void main(String[] args) {
		int x = 0;
		x = add1(10, 5);
		System.out.println(x);
   }
	
}