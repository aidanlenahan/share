// sample code for ArrayList
// 1.3.2025

import java.io.*;
import java.util.*;

class ArrayListFun
{
	public static void main(String [] args)
	{
		ArrayList <Integer> list = new ArrayList<>();
		list.add(4);
		list.add(2);
		list.add(9);
		list.add(10);

		for (int i = 0; i < list.size(); i++)
		{
			System.out.println(list.get(i));
		}

		list.remove(1); //removes second item in list

		for(int value: list) //enhanced for loop or foreach loop; is equivalent to (int i = 0; i < list.size(); i++)
		{
			System.out.println(value);
		}
	}
}
