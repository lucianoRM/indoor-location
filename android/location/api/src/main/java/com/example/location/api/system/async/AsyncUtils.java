package com.example.location.api.system.async;

import android.os.AsyncTask;

import com.example.location.internal.async.DefaultAsyncTask;

/**
 * Simple Utils class with methods to execute operations in an async manner
 */
public class AsyncUtils {

    /**
     * Execute the {@link AsyncOperation<T>} asynchronously. After that, execute the {@link AsyncCallback} with the result.
     * @param logic the operation to execute asynchronously
     * @param callback the callback to call when the operation execution is done.
     * @param <T>
     */
    public static <T> void executeAsync(AsyncOperation<T> logic, AsyncCallback<T> callback) {
        AsyncTask<Void, Void, T> task = new DefaultAsyncTask<>(logic, callback);
        task.execute();
    }


}
