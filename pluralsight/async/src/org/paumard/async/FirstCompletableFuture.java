package org.paumard.async;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class FirstCompletableFuture {
    public static void main(String[] args) throws InterruptedException {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        Runnable task = () -> System.out.println("I am running aync in thread " + Thread.currentThread().getName());
        CompletableFuture.runAsync(task);
        Thread.sleep(100);
        executor.shutdown();
    }
}
