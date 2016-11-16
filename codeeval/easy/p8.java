import java.io.*;
public class p8 {
    public static void main (String[] args) throws IOException {
        File file = new File(args[0]);
        BufferedReader buffer = new BufferedReader(new FileReader(file));
        String line;
        while ((line = buffer.readLine()) != null) {
            line = line.trim();
            // Process line of input Here
            if (!line.isEmpty()) {
                String[] words = line.split(" ");
                String output = "";
                for (int i = 0; i < words.length; i++) {
                    output += words[words.length-i-1] + " ";
                }
                output = output.trim();
                System.out.println(output);
            }
        }
    }
}
