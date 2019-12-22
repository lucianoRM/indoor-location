package com.example.location.internal.async;

import android.os.AsyncTask;

import com.example.location.api.system.async.AsyncCallback;
import com.example.location.api.system.async.AsyncOperation;

public class DefaultAsyncTask<T> extends AsyncTask<Void, Void, T> {

    private AsyncOperation<T> executable;
    private AsyncCallback<T> callback;
    private Throwable exception;

    public DefaultAsyncTask(AsyncOperation<T> executable, AsyncCallback<T> callback) {
        this.executable = executable;
        this.callback = callback;
    }

    @Override
    protected T doInBackground(Void... voids) {
        try {
            return executable.execute();
        }catch (Exception e) {
            this.exception = e;
        }
        return null;
    }

    @Override
    protected void onPostExecute(T t) {
        if(this.exception != null) {
            callback.onFailure(new DefaultAsyncOpFailure(exception.getMessage()));
        }else {
            callback.onSuccess(new DefaultAsyncOpSuccess<>(t));
        }
    }
}
