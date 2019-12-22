package com.example.location.activity;

import android.os.Handler;
import android.os.Looper;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.TextView;

import com.example.location.adapter.AvailableActivitiesAdapter;
import com.example.location.api.data.Position;
import com.example.location.api.entity.sensor.Sensor;
import com.example.location.api.system.async.AsyncCallback;
import com.example.location.api.system.async.AsyncOpFailure;
import com.example.location.api.system.async.AsyncOpSuccess;
import com.example.location.impl.ble.ibeacon.IBeaconSensorFeed;
import com.example.location.R;
import com.example.location.impl.ble.ibeacon.transfomers.DefaultMediumTransformer;
import com.example.location.impl.ble.ibeacon.transfomers.OptimizationBasedSensorDataTransformer;
import com.example.location.task.AsyncTaskException;

import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicLong;
import java.util.function.BiConsumer;

import static android.graphics.Color.GREEN;
import static android.graphics.Color.RED;
import static android.util.Log.getStackTraceString;
import static com.example.location.api.entity.sensor.SensorConfiguration.sensorConfigurationBuilder;
import static com.example.location.api.system.async.AsyncCallback.newCallback;
import static com.example.location.api.system.async.AsyncUtils.executeAsync;
import static com.example.location.Utils.showError;
import static com.example.location.api.utils.SensingUtils.bestValueFrom;
import static com.example.location.impl.ble.ibeacon.transfomers.BasePowerOptimizationBasedValueResolver.basePowerOptimizationValueResolver;
import static com.example.location.impl.ble.ibeacon.transfomers.CoeffAndBasePowerOptimizationBasedValueResolver.coeffAndBasePowerValueResolver;
import static com.example.location.impl.ble.ibeacon.transfomers.CoeffOptimizationValueResolver.coeffOptimizationValueResolver;
import static com.example.location.task.CreateSensorAsyncTask.createSensor;
import static com.google.common.primitives.Floats.asList;
import static java.lang.String.format;
import static java.lang.System.currentTimeMillis;
import static java.util.concurrent.Executors.newScheduledThreadPool;
import static java.util.concurrent.TimeUnit.MILLISECONDS;

public class UserPositionActivity extends ConnectedUserActivity {

    private static final int PERIOD_MS = 1000;

    private Sensor defaultCoeffSensor;
    private Sensor opCoeffSensor;
    private Sensor opBPSensor;
    private Sensor opBPCoeffSensor;

    private PositionHolder defaultCoeffPositionHolder;
    private PositionHolder opCoeffPositionHolder;
    private PositionHolder opBPPositionHolder;
    private PositionHolder opBPCoeffPositionHolder;

    private IBeaconSensorFeed iBeaconSensorFeed;

    private Handler uiHandler;

    private final Object modLock = new Object();
    private Sensor currentSensor;
    private AsyncCallback<Position> onSense;
    private ScheduledExecutorService scanningExecutor;
    private AtomicBoolean lastTaskExecuted = new AtomicBoolean(true);

    private RecyclerView.Adapter logAdapter;
    private List<String> logLines = new LinkedList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        this.iBeaconSensorFeed = new IBeaconSensorFeed(locationSystem.getServerLogger());
        this.uiHandler = new Handler(Looper.getMainLooper());

        setContentView(R.layout.user_position);

        startBluetoothSensor();

        logAdapter = new AvailableActivitiesAdapter(logLines);
        RecyclerView recyclerView = findViewById(R.id.infoView);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(logAdapter);

        currentSensor = null;

        this.scanningExecutor = newScheduledThreadPool(1);
        this.scanningExecutor.scheduleAtFixedRate(
                () -> {
                    synchronized (modLock) {
                        if(currentSensor != null && lastTaskExecuted.get()) {
                            lastTaskExecuted.set(false);
                            sense(currentSensor, onSense);
                        }
                    }
                },0,PERIOD_MS, MILLISECONDS);



    }

    @Override
    protected void onPause() {
        super.onPause();
        iBeaconSensorFeed.stop();
        this.scanningExecutor.shutdown();
    }

    private void onError(String message) {
        showError(message, UserPositionActivity.this);
        this.onPause();
    }

    public void senseDefaultCoeff(View view) {
        synchronized (modLock) {
            if(defaultCoeffSensor.equals(currentSensor)) {
                currentSensor = null;
                view.setBackgroundColor(RED);
            }else {
                currentSensor = defaultCoeffSensor;
                onSense = newCallback(
                        s -> updatePosition(this::updateDefaultCoeffPosition),
                        f -> onError(f.errorMessage())
                );
                view.setBackgroundColor(GREEN);
            }
        }
    }

    public void senseCoeff(View view) {
        synchronized (modLock) {
            if(opCoeffSensor.equals(currentSensor)) {
                currentSensor = null;
                view.setBackgroundColor(RED);
            }else {
                currentSensor = opCoeffSensor;
                onSense = newCallback(
                        s -> updatePosition(this::updateOpCoeffPosition),
                        f -> onError(f.errorMessage())
                );
                view.setBackgroundColor(GREEN);
            }
        }
    }

    public void senseBP(View view) {
        synchronized (modLock) {
            if(opBPSensor.equals(currentSensor)) {
                currentSensor = null;
                view.setBackgroundColor(RED);
            }else {
                currentSensor = opBPSensor;
                onSense = newCallback(
                        s -> updatePosition(this::updateOpBpPosition),
                        f -> onError(f.errorMessage())
                );
                view.setBackgroundColor(GREEN);
            }
        }
    }

    public void senseCoeffBP(View view) {
        synchronized (modLock) {
            if(opBPCoeffSensor.equals(currentSensor)) {
                currentSensor = null;
                view.setBackgroundColor(RED);
            }else {
                currentSensor = opBPCoeffSensor;
                onSense = newCallback(
                        s -> updatePosition(this::updateOpCoeffBpPosition),
                        f -> onError(f.errorMessage())
                );
                view.setBackgroundColor(GREEN);
            }
        }
    }

    private void sense(Sensor sensor, AsyncCallback<Position> callback) {
        AtomicLong init_time = new AtomicLong();
        if (sensor != null) {
            executeAsync(
                    () -> {
                        init_time.set(currentTimeMillis());
                        sensor.sense();
                        return null;
                    },
                    new AsyncCallback<Position>() {
                        @Override
                        public void onSuccess(AsyncOpSuccess<Position> success) {
                            callback.onSuccess(success);
                            logLines.add("TIME TAKEN: " + Long.toString(currentTimeMillis() - init_time.get()));
                            logAdapter.notifyDataSetChanged();
                        }

                        @Override
                        public void onFailure(AsyncOpFailure failure) {
                            callback.onFailure(failure);
                        }
                    }
            );
        } else {
            showError("SENSOR IS NULL", this);
        }
    }

    private void startBluetoothSensor() {
        try {
            this.defaultCoeffSensor = createSensor(locationSystem.getSensorManager(),
                    sensorConfigurationBuilder()
                            .withId("default_coeff_sensor")
                            .withFeed(iBeaconSensorFeed)
                            .withTransformer(new DefaultMediumTransformer("defCoeff", locationSystem.getServerLogger()))
                            .build());
            this.defaultCoeffPositionHolder = new PositionHolder();
            this.opCoeffSensor = createSensor(locationSystem.getSensorManager(),
                    sensorConfigurationBuilder()
                            .withId("op_coeff_sensor")
                            .withFeed(iBeaconSensorFeed)
                            .withTransformer(new OptimizationBasedSensorDataTransformer(coeffOptimizationValueResolver(), "opCoeff", locationSystem.getServerLogger()))
                            .build());
            this.opCoeffPositionHolder = new PositionHolder();
            this.opBPSensor = createSensor(locationSystem.getSensorManager(),
                    sensorConfigurationBuilder()
                            .withId("op_bp_sensor")
                            .withFeed(iBeaconSensorFeed)
                            .withTransformer(new OptimizationBasedSensorDataTransformer(basePowerOptimizationValueResolver(), "opBp", locationSystem.getServerLogger()))
                            .build());
            this.opBPPositionHolder = new PositionHolder();
            this.opBPCoeffSensor = createSensor(locationSystem.getSensorManager(),
                    sensorConfigurationBuilder()
                            .withId("op_bp_coeff_sensor")
                            .withFeed(iBeaconSensorFeed)
                            .withTransformer(new OptimizationBasedSensorDataTransformer( coeffAndBasePowerValueResolver(), "opCoeffBp", locationSystem.getServerLogger()))
                            .build());
            this.opBPCoeffPositionHolder = new PositionHolder();
        } catch (AsyncTaskException e) {
            terminate(getStackTraceString(e));
        }
        iBeaconSensorFeed.start();
    }

    private void updateDefaultCoeffPosition(float newX, float newY) {
        TextView x = findViewById(R.id.xValueTextView);
        TextView y = findViewById(R.id.yValueTextView);
        defaultCoeffPositionHolder.add(newX, newY);
        x.setText(defaultCoeffPositionHolder.getX());
        y.setText(defaultCoeffPositionHolder.getY());
    }

    private void updateOpCoeffPosition(float newX, float newY) {
        TextView x = findViewById(R.id.xValueTextView);
        TextView y = findViewById(R.id.yValueTextView);
        opCoeffPositionHolder.add(newX, newY);
        x.setText(opCoeffPositionHolder.getX());
        y.setText(opCoeffPositionHolder.getY());
    }

    private void updateOpBpPosition(float newX, float newY) {
        TextView x = findViewById(R.id.xValueTextView);
        TextView y = findViewById(R.id.yValueTextView);
        opBPPositionHolder.add(newX, newY);
        x.setText(opBPPositionHolder.getX());
        y.setText(opBPPositionHolder.getY());
    }

    private void updateOpCoeffBpPosition(float newX, float newY) {
        TextView x = findViewById(R.id.xValueTextView);
        TextView y = findViewById(R.id.yValueTextView);
        opBPCoeffPositionHolder.add(newX, newY);
        x.setText(opBPCoeffPositionHolder.getX());
        y.setText(opBPCoeffPositionHolder.getY());
    }

    private void updatePosition(BiConsumer<Float, Float> positionConsumer) {
        lastTaskExecuted.set(true);
        executeAsync(
                () -> locationSystem.getLocator().getPosition(),
                newCallback(
                        s -> {
                            Position position = s.getResult();
                            uiHandler.post(() -> positionConsumer.accept(position.getX(), position.getY()));
                        },
                        f -> showError(f.errorMessage(), UserPositionActivity.this)
        ));
    }


    private static class PositionHolder {


        private static final int MAX_POSITIONS = 20;

        private float[] xs = new float[MAX_POSITIONS];
        private float[] ys = new float[MAX_POSITIONS];

        private int index = 0;

        void add(float x, float y) {
            int index_mod = index % MAX_POSITIONS;
            xs[index_mod] = x;
            ys[index_mod] = y;
            index++;
        }

        String getX() {
            return format("%.1f", getAverage(xs));
        }

        String getY() {
            return format("%.1f", getAverage(ys));
        }

        private int getTotalValues() {
            return index > MAX_POSITIONS ? MAX_POSITIONS : index;
        }

        private float getAverage(float[] values) {
            int total = getTotalValues();
            return (float)bestValueFrom(asList(values).subList(0, total));
        }


    }

}


