// Fizz Buzz
import java.io.*;

public class p1 {
	public static void main(String[] args) {
		// Prints "Hello, World" to the terminal window.
		if (args.length == 1) {
			try (FileReader file = new FileReader(args[0])) {
				try (BufferedReader br = new BufferedReader(file)) {
					String line;
					while ((line = br.readLine()) != null) {
						// line format: F B count
						String[] parts = line.split(" ");
						int f = Integer.parseInt(parts[0]);
						int b = Integer.parseInt(parts[1]);
						int c = Integer.parseInt(parts[2]);
						String buffer = new String("");
						for (int i = 1; i <= c; i++) {
							if (i%f == 0) {
								if (i%b == 0) {
									buffer += "FB";
								} else {
									buffer += "F";
								}
							} else if (i%b == 0) {
								buffer += "B";
							} else {
								buffer += Integer.toString(i);
							}
							if (i < c) {
								buffer += " ";
							}
						}
						System.out.println(buffer);
					}
				}
			} catch (Exception e) {
				throw new RuntimeException(e.getMessage());
			}
		} else {
			throw new RuntimeException("This program must take filename as input");
		}
	}
}
