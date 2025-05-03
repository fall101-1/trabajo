import java.util.Random;

public class SimuladorDados {
    public static void main(String[] args) {
        int[] frecuencias = new int[13]; 

        Random rand = new Random();

        // Lanzamientos
        for (int i = 0; i < 30; i++) {
            int dado1 = rand.nextInt(6) + 1;
            int dado2 = rand.nextInt(6) + 1;
            int suma = dado1 + dado2;
            frecuencias[suma]++;
        }

        // Tabla de frecuencias
        System.out.println("Suma\tFrecuencia");
        for (int i = 2; i <= 12; i++) {
            System.out.println(i + "\t" + frecuencias[i]);
        }

        // Gráfica de barras
        System.out.println("\nGráfica de barras:");
        for (int i = 2; i <= 12; i++) {
            System.out.printf("%2d | ", i);
            for (int j = 0; j < frecuencias[i]; j++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}
