package org.paumard.async;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Supplier;

public class CompletableFutureSupplier {
    public static void main(String[] args) {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        Supplier<String> supplier = () -> {
            try {
                Thread.sleep(500);
            } catch (InterruptedException ignored) {
            }
            return Thread.currentThread().getName();
        };
        CompletableFuture<String> completableFuture = CompletableFuture.supplyAsync(supplier, executor);
        completableFuture.obtrudeValue("Too loing");
        String string = completableFuture.join();
        System.out.println("string = " + string);
         string = completableFuture.join();
        System.out.println("string = " + string);
        executor.shutdown();
    }
}
